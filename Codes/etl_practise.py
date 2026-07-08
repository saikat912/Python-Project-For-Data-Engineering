import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime


log_file = "log_file.txt"
target_file = "target_file.csv"


# Extract CSV files
def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe


# Extract JSON files
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe


# Extract XML files
def extract_from_xml(file_to_process):

    dataframe = pd.DataFrame(
        columns=[
            "car_model",
            "year_of_manufacture",
            "price",
            "fuel"
        ]
    )

    tree = ET.parse(file_to_process)
    root = tree.getroot()

    for i in root:

        car_model = i.find("car_model").text

        year_of_manufacture = int(
            i.find("year_of_manufacture").text
        )

        price = float(
            i.find("price").text
        )

        fuel = i.find("fuel").text


        dataframe = pd.concat(
            [
                dataframe,
                pd.DataFrame(
                    [{
                        "car_model": car_model,
                        "year_of_manufacture": year_of_manufacture,
                        "price": price,
                        "fuel": fuel
                    }]
                )
            ],
            ignore_index=True
        )

    return dataframe


# Extract all data
def extract():

    extracted_data = pd.DataFrame(
        columns=[
            "car_model",
            "year_of_manufacture",
            "price",
            "fuel"
        ]
    )


    # Process CSV files
    for csvfile in glob.glob("*.csv"):

        if csvfile != target_file:

            extracted_data = pd.concat(
                [
                    extracted_data,
                    extract_from_csv(csvfile)
                ],
                ignore_index=True
            )


    # Process JSON files
    for jsonfile in glob.glob("*.json"):

        extracted_data = pd.concat(
            [
                extracted_data,
                extract_from_json(jsonfile)
            ],
            ignore_index=True
        )


    # Process XML files
    for xmlfile in glob.glob("*.xml"):

        extracted_data = pd.concat(
            [
                extracted_data,
                extract_from_xml(xmlfile)
            ],
            ignore_index=True
        )


    return extracted_data



# Transform data
def transform(data):

    """
    Transform price values:
    Round price column to two decimal places
    """

    data["price"] = round(
        data["price"],
        2
    )

    return data



# Load transformed data
def load_data(target_file, transformed_data):

    transformed_data.to_csv(
        target_file,
        index=False
    )



# Logging function
def log_progress(message):

    timestamp_format = "%Y-%h-%d-%H:%M:%S"

    now = datetime.now()

    timestamp = now.strftime(
        timestamp_format
    )

    with open(log_file, "a") as f:

        f.write(
            timestamp + "," + message + "\n"
        )



# ETL Execution

log_progress("ETL Job Started")


# Extract

log_progress("Extract phase Started")

extracted_data = extract()

log_progress("Extract phase Ended")


# Transform

log_progress("Transform phase Started")

transformed_data = transform(
    extracted_data
)

print("Transformed Data")

print(
    transformed_data
)

log_progress("Transform phase Ended")


# Load

log_progress("Load phase Started")

load_data(
    target_file,
    transformed_data
)

log_progress("Load phase Ended")


log_progress("ETL Job Ended")