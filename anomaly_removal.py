import duckdb


con = duckdb.connect('ecommerce_store.duckdb')

# first, let's create a copy of the dataset, which will contain corrected data:
con.execute('delete from user_event where user_id in (564068124, 568778435, 569335945)')
