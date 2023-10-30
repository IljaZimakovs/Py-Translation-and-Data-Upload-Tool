# Translation and Data Upload Tool

## Overview

This tool is designed to translate text data from a selected file, format the data, and upload it to an AWS DynamoDB table. The tool uses Google Cloud Translate API for translation and Boto3 library for AWS DynamoDB interaction.

## Prerequisites

Before using this tool, ensure you have the following:

- Python installed on your system
- Google Cloud Translate API credentials saved in a file named `credentials.json`
- AWS access credentials (access key ID and secret access key) saved in a `.env` file:
  ```
  AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY
  REGION=YOUR_AWS_REGION
  TABLE=YOUR_DYNAMODB_TABLE_NAME
  ```

## How to Use

1. **Select a File:**
   Run the script and a file dialog will prompt you to select a text file. Only `.txt` files are supported.

2. **Data Processing:**
   - The tool processes the selected file to identify and translate JSON objects.
   - It translates specified fields from English to Japanese using Google Cloud Translate API.
   - Fields to be translated: `headquarters`, `other_offices`, `segment`, `markets`, `company_name`, and `summary`.

3. **DynamoDB Upload:**
   - The translated data is uploaded to the specified DynamoDB table.
   - Uploaded fields: `info_type`, `net_loc`, `headquarters`, `headquarters_ja`, `other_offices`, `other_offices_ja`, `industry_segment`, `markets`, `name`, `name_ja`, `summary`, `summary_ja`, `website`.

4. **Output:**
   - The tool prints the translated data for each entry.
   - DynamoDB response (success or error) is printed for each upload attempt.

## Notes

- Make sure the AWS credentials in the `.env` file have the necessary permissions to access the DynamoDB table.
- Ensure the `credentials.json` file contains valid Google Cloud Translate API credentials.
- The tool assumes a specific structure in the input file (JSON objects) and specific fields to translate. Modify the code accordingly if your input data structure differs.
- Error handling and edge cases are minimal. Enhance the code as per your specific requirements and error scenarios.
