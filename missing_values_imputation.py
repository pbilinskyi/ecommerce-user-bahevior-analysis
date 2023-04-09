import duckdb


con = duckdb.connect('ecommerce_store.duckdb')

# first, let's create a copy of the dataset, which will contain corrected data:
con.execute('alter table user_event rename to user_event_raw')
con.execute('create table user_event as select * from user_event_raw')


# missing value inputation: category_code
query = """
update user_event
set category_code = 'undefined'
where category_code is null
"""
con.execute(query)


# missing value inputation: brand
query = """
update user_event
set brand = 'undefined'
where brand is null
"""
con.execute(query)


# missing value inputation: user_session
query = """
create table user_with_empty_session
as
select *
from user_event
    join (select distinct user_id
            from user_event
            where user_session is null) as users
    using (user_id);

create temp table user_session_missing_values_inputes
as
select  user_id,
        event_time,
        case 
            when time_from_prev_event < interval '30 min' and prev_user_session is not null then prev_user_session 
            when time_to_next_event < interval '30 min' and next_user_session is not null then next_user_session 
            else hash(event_time::text)::text
        end as user_session
from 
(
    select 
        user_session,
        user_id,
        event_time,
        event_time - lag(event_time) over (partition by user_id order by event_time) as time_from_prev_event,
        lead(event_time) over (partition by user_id order by event_time) - event_time as time_to_next_event,
        lead(user_session) over (partition by user_id order by event_time) as next_user_session,
        lag(user_session) over (partition by user_id order by event_time) as prev_user_session
    from user_with_empty_session
)
where user_session is null
order by user_id, event_time;

update user_event
set user_session = mvi.user_session
from user_session_missing_values_inputes mvi
where user_event.user_session is null
  and user_event.user_id = mvi.user_id
  and user_event.event_time = mvi.event_time;
  """
con.execute(query)
