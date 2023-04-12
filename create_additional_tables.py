import duckdb
import logging


logging.basicConfig(level='DEBUG', format='%(message)s')

con = duckdb.connect('ecommerce_store.duckdb')


# Create table user_stage_stat, used for calculating user funnel
logging.info('STARTED: computing table user_stage_stat')
query = """
create table user_stage_stat
as
select user_id,
       count(distinct user_session)                             as session_cnt,
       max(case when event_type = 'view' then 1 else 0 end)     as is_view,
       max(case when event_type = 'cart' then 1 else 0 end)     as is_cart,
       max(case when event_type = 'purchase' then 1 else 0 end) as is_purchase,
from user_event
group by user_id;

update user_stage_stat
set is_view = 1,
    is_cart = 1
where is_purchase = 1;

update user_stage_stat
set is_view = 1
where is_cart = 1;
"""
con.execute(query)
logging.info('SUCCESS')


# Create table session_stage_stat, used for calculating user funnel
logging.info('STARTED: computing table session_stage_stat')
query = """
create table session_stage_stat
as
select user_id,
       user_session,
       min(event_time)                                          as session_start_time,
       max(case when event_type = 'view' then 1 else 0 end)     as is_view,
       max(case when event_type = 'cart' then 1 else 0 end)     as is_cart,
       max(case when event_type = 'purchase' then 1 else 0 end) as is_purchase,
from user_event
group by user_id, user_session;

update session_stage_stat
set is_view = 1,
    is_cart = 1
where is_purchase = 1;

update session_stage_stat
set is_view = 1
where is_cart = 1;
"""
con.execute(query)
logging.info('SUCCESS')


# Create table user_visit_retention
logging.info('STARTED: computing table session_stage_stat')
query = """
create table user_retention
as
with user_daily_stat as (
    select user_id,
           event_time::date                                         as action_date,
           1                                                        as has_view,
           max(case when event_type = 'purchase' then 1 else 0 end) as has_purchase
    from user_event
    group by user_id, event_time::date
),
cohort_user_daily_stat as (
    select user_id,
           min(action_date) over (partition by user_id) as cohort_date,
           action_date,
           has_view,
           has_purchase
    from user_daily_stat
),
t as (
select cohort_date,
       action_date - cohort_date                          as period_num,
       count(case when has_view = 1 then user_id end)     as user_viewed_cnt,
       count(case when has_purchase = 1 then user_id end) as user_purchased_cnt
from cohort_user_daily_stat
group by cohort_date, action_date - cohort_date
)
select cohort_date,
       period_num,
       user_viewed_cnt,
       user_purchased_cnt,
       first_value(user_viewed_cnt)
            over (partition by cohort_date order by period_num) as cohort_total_user_viewed_cnt,
       first_value(user_purchased_cnt)
            over (partition by cohort_date order by period_num) as cohort_total_user_purchased_cnt
from t
order by cohort_date, period_num
"""
con.execute(query)
logging.info('SUCCESS')
