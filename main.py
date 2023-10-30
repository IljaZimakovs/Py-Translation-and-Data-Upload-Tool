import os
import re
import tkinter as tk
from tkinter import filedialog

import boto3
import dotenv
from google.cloud import translate_v2 as translate

# Load environment variables from the .env file
dotenv.load_dotenv()

# Retrieve AWS and Google Cloud credentials from environment variables
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
region_name = os.getenv("REGION")
table_name = os.getenv("TABLE")

# Initialize the tkinter root window and hide it
root = tk.Tk()
root.withdraw()

# Ask the user to select a text file through a file dialog
file_path = filedialog.askopenfilename(
    title="Select File", filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
)

# Continue with the rest of your code only if a file is selected
if file_path:
    # Set Google Cloud credentials environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

    # Initialize the Google Cloud Translator client
    translator = translate.Client()

    # Initialize AWS DynamoDB client
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    # Select DynamoDB table
    table = dynamodb.Table(table_name)

    # Read text data from the selected file
    with open(file_path, encoding="utf-8") as file:
        text_data = file.read()

    # Find and fix invalid list format in the text data
    invalide_list = re.findall(r"\'\[.*?\]\'", text_data)
    for item in invalide_list:
        new_str = item.replace("'", "")
        item_arr = new_str.replace("'", "")[1:-1].split(",")
        item_arr = [f"'{x}'" for x in item_arr]
        text_data = text_data.replace(item, "[" + ",".join(item_arr) + "]")

    # Extract company details from the text data
    company_detail_list = re.findall(r"\{.*?\}", text_data)
    new_company_list = []

    # Parse and evaluate JSON objects from the company details list
    for idx, item in enumerate(company_detail_list):
        if item[1] == '"':
            new_company_list.append(eval(item))
        else:
            new_company_list.append(eval(item))

    # Extract domain names from the text data
    domain_list = text_data.split("\n")[::2]

    # Translate text using Google Cloud Translate API
    def translate_text(data):
        """
        Translate text from English to Japanese using Google Cloud Translate API.

        Args:
            data (str): Text to be translated.

        Returns:
            str: Translated text.
        """
        if data:
            return translator.translate(
                data, source_language="en", target_language="ja", format_="text"
            )["translatedText"]
        else:
            return ""

    # Combine a list of strings into a comma-separated string
    def combine(data):
        """
        Combine a list of strings into a comma-separated string.

        Args:
            data (list): List of strings to be combined.

        Returns:
            str: Comma-separated string.
        """
        if data:
            combined_data = ",".join(data)
            return combined_data
        else:
            return ""

    # Upload company data to DynamoDB
    for i in range(0, len(new_company_list), 1):
        data_for_upload = {
            "info_type": "main",
            "net_loc": domain_list[i],
            "headquarters": new_company_list[i]["headquarters"]
            if "headquarters" in new_company_list[i]
            else "",
            "headquarters_ja": translate_text(new_company_list[i]["headquarters"])
            if "headquarters" in new_company_list[i]
            else "",
            "other_offices": combine(new_company_list[i]["other_offices"])
            if "other_offices" in new_company_list[i]
            else "",
            "other_offices_ja": translate_text(
                combine(new_company_list[i]["other_offices"])
            )
            if "other_offices" in new_company_list[i]
            else "",
            "industry_segment": combine(new_company_list[i]["segment"])
            if "segment" in new_company_list[i]
            else "",
            "markets": combine(new_company_list[i]["markets"])
            if "markets" in new_company_list[i]
            else "",
            "name": new_company_list[i]["company_name"]
            if "company_name" in new_company_list[i]
            else "",
            "name_ja": translate_text(new_company_list[i]["company_name"])
            if "company_name" in new_company_list[i]
            else "",
            "summary": new_company_list[i]["summary"]
            if "summary" in new_company_list[i]
            else "",
            "summary_ja": translate_text(new_company_list[i]["summary"])
            if "summary" in new_company_list[i]
            else "",
            "website": domain_list[i],
        }
        print(data_for_upload)

        # Upload translated data to DynamoDB
        response = table.put_item(Item=data_for_upload)

        # Print the response from DynamoDB
        print("DynamoDB Response:")
        print(response)
