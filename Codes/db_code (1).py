import sqlite3
import pandas as pd


# # Connect to SQLite database
conn = sqlite3.connect("STAFF.db")


# # Define table details
table_name = "Departments"

attribute_list = [
    "DEPT_ID",
    "DEP_NAME",
    "MANAGER_ID",
    "LOC_ID"
  ]


file_path = "/home/project/Departments.csv"


# # Read CSV file
df = pd.read_csv(
    file_path,
   names=attribute_list
)

 # Load dataframe into SQLite table
df.to_sql(
    table_name,
    conn,
    if_exists="replace",
    index=False
)


print("Table is ready")


# ------------------------------
# Query 1: View complete table
# ------------------------------

query_statement = f"""
SELECT * FROM {table_name}
"""

query_output = pd.read_sql(
    query_statement,
    conn
)

print(query_statement)
print(query_output)




# ------------------------------
# Insert new instructor record
# ------------------------------

data_dict = {
    "DEPT_ID": [9],
    "DEP_NAME": ["Quality Assurance"],
    "MANAGER_ID": [30010],
    "LOC_ID": ["L0010"],
}


data_append = pd.DataFrame(
    data_dict
)


data_append.to_sql(
    table_name,
    conn,
    if_exists="append",
    index=False
)


print("Data appended successfully")



# ------------------------------
# Verify appended data
# ------------------------------

query_statement = f"""
SELECT * FROM {table_name}
"""

query_output = pd.read_sql(
    query_statement,
    conn
)

print(query_output)



# Close database connection
conn.close()
