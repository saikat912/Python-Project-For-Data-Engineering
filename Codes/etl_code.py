import glob
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime


log_file = "log_file.txt"
target_file = "transformed_data.csv"


def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe


def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=True)
    return dataframe


def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=["name", "height", "weight"])

    tree = ET.parse(file_to_process)
    root = tree.getroot()

    for person in root:
        name = person.find("name").text
        height = float(person.find("height").text)
        weight = float(person.find("weight").text)

        dataframe = pd.concat(
            [
                dataframe,
                pd.DataFrame(
                    [{
                        "name": name,
                        "height": height,
                        "weight": weight
                    }]
                )
            ],
            ignore_index=True
        )

    return dataframe


def extract():
    extracted_data = pd.DataFrame(
        columns=["name", "height", "weight"]
    )

    # Process all CSV files except target file
    for csvfile in glob.glob("*.csv"):
        if csvfile != target_file:
            extracted_data = pd.concat(
                [
                    extracted_data,
                    extract_from_csv(csvfile)
                ],
                ignore_index=True
            )

    # Process all JSON files
    for jsonfile in glob.glob("*.json"):
        extracted_data = pd.concat(
            [
                extracted_data,
                extract_from_json(jsonfile)
            ],
            ignore_index=True
        )

    # Process all XML files
    for xmlfile in glob.glob("*.xml"):
        extracted_data = pd.concat(
            [
                extracted_data,
                extract_from_xml(xmlfile)
            ],
            ignore_index=True
        )

    return extracted_data


def transform(data):
    """
    Convert inches to meters
    1 inch = 0.0254 meters
    """

    data["height"] = round(
        data.height * 0.0254,
        2
    )

    """
    Convert pounds to kilograms
    1 pound = 0.45359237 kilograms
    """

    data["weight"] = round(
        data.weight * 0.45359237,
        2
    )

    return data


def load_data(target_file, transformed_data):
    transformed_data.to_csv(target_file)


def log_progress(message):

    timestamp_format = "%Y-%h-%d-%H:%M:%S"

    now = datetime.now()

    timestamp = now.strftime(timestamp_format)

    with open(log_file, "a") as f:
        f.write(timestamp + "," + message + "\n")


# ETL execution

log_progress("ETL Job Started")


log_progress("Extract phase Started")

extracted_data = extract()

log_progress("Extract phase Ended")


log_progress("Transform phase Started")

transformed_data = transform(extracted_data)

print("Transformed Data")
print(transformed_data)

log_progress("Transform phase Ended")


log_progress("Load phase Started")

load_data(
    target_file,
    transformed_data
)

log_progress("Load phase Ended")


log_progress("ETL Job Ended")