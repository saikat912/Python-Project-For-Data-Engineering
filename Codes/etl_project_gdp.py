import sqlite3
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup


# Required entities

url = "https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"

csv_path = "Countries_by_GDP.csv"

db_name = "World_Economies.db"

table_name = "Countries_by_GDP"

log_file = "etl_project_log.txt"


# Extract function

def extract(url, table_attribs):
    """
    Extract country GDP data from website
    """

    page = requests.get(url).text

    soup = BeautifulSoup(
        page,
        "html.parser"
    )


    df = pd.DataFrame(
        columns=table_attribs
    )


    tables = soup.find_all("tbody")

    rows = tables[2].find_all("tr")


    for row in rows:

        col = row.find_all("td")


        if len(col) != 0:

            if col[0].find("a") is not None:

                country = col[0].a.contents[0]

                gdp = col[2].contents[0]


                if gdp != "—":

                    data_dict = {
                        "Country": country,
                        "GDP_USD_million": gdp
                    }


                    df1 = pd.DataFrame(
                        data_dict,
                        index=[0]
                    )


                    df = pd.concat(
                        [df, df1],
                        ignore_index=True
                    )

    return df



# Transform function

def transform(df):
    """
    Convert GDP from Million USD
    to Billion USD
    """

    df["GDP_USD_million"] = (
        df["GDP_USD_million"]
        .str.replace(",", "")
        .astype(float)
    )


    df["GDP_USD_billion"] = round(
        df["GDP_USD_million"] / 1000,
        2
    )


    df.drop(
        "GDP_USD_million",
        axis=1,
        inplace=True
    )


    return df



# Load CSV

def load_to_csv(df, csv_path):
    """
    Save dataframe as CSV
    """

    df.to_csv(
        csv_path,
        index=False
    )



# Load Database

def load_to_db(
    df,
    sql_connection,
    table_name
):

    df.to_sql(
        table_name,
        sql_connection,
        if_exists="replace",
        index=False
    )



# Query database

def run_query(
    query_statement,
    sql_connection
):

    print(query_statement)

    query_output = pd.read_sql(
        query_statement,
        sql_connection
    )

    print(query_output)



# Logging

def log_progress(message):

    timestamp_format = "%Y-%m-%d %H:%M:%S"

    now = datetime.now()

    timestamp = now.strftime(
        timestamp_format
    )


    with open(
        log_file,
        "a"
    ) as f:

        f.write(
            timestamp
            + " : "
            + message
            + "\n"
        )



# ETL Execution


table_attribs = [
    "Country",
    "GDP_USD_million"
]


log_progress(
    "ETL Job Started"
)



log_progress(
    "Extract phase Started"
)

df = extract(
    url,
    table_attribs
)

log_progress(
    "Extract phase Ended"
)



log_progress(
    "Transform phase Started"
)

df = transform(df)

log_progress(
    "Transform phase Ended"
)



log_progress(
    "Load phase Started"
)

load_to_csv(
    df,
    csv_path
)


sql_connection = sqlite3.connect(
    db_name
)


load_to_db(
    df,
    sql_connection,
    table_name
)

log_progress(
    "Load phase Ended"
)



query_statement = """
SELECT *
FROM Countries_by_GDP
WHERE GDP_USD_billion >= 100
"""


run_query(
    query_statement,
    sql_connection
)


sql_connection.close()


log_progress(
    "ETL Job Completed"
)
