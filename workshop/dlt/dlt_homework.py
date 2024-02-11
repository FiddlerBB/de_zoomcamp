import dlt
import duckdb

def people_1(): 
    for i in range(1, 6): 
        yield {"ID": i, "Name": f"Person_{i}", "Age": 25 + i, "City": "City_A"} 

def people_2(): 
    for i in range(3, 9): 
        yield {"ID": i, "Name": f"Person_{i}", "Age": 30 + i, "City": "City_B", "Occupation": f"Job_{i}"} 

generator_pipeline = dlt.pipeline(destination='duckdb', dataset_name='generators')

info = generator_pipeline.run(people_1(), table_name='testing_generator', write_disposition='replace')
info = generator_pipeline.run(people_2(), table_name='testing_generator', write_disposition='merge')

with duckdb.connect('dlt_dlt_homework.duckdb') as conn:
    data = conn.execute('select sum(Age) from generators.testing_generator')
    print(data.fetchall())