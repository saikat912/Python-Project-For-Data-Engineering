import sqlite3
import pandas as pd


# Connect to SQLite database
conn = sqlite3.connect("STAFF.db")


# Define table details
table_name = "INSTRUCTOR"

attribute_list = [
    "ID",
    "FNAME",
    "LNAME",
    "CITY",
    "CCODE"
]


file_path = "/home/project/INSTRUCTOR.csv"


# Read CSV file
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
# Query 2: View only FNAME column
# ------------------------------

query_statement = f"""
SELECT FNAME FROM {table_name}
"""

query_output = pd.read_sql(
    query_statement,
    conn
)

print(query_statement)
print(query_output)



# ------------------------------
# Query 3: Count records
# ------------------------------

query_statement = f"""
SELECT COUNT(*) FROM {table_name}
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
    "ID": [100],
    "FNAME": ["John"],
    "LNAME": ["Doe"],
    "CITY": ["Paris"],
    "CCODE": ["FR"]
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
