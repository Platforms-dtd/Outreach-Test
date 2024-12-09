from openai import OpenAI
import csv
import os
from dotenv import load_dotenv

load_dotenv()

# Access the variables
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

file_name = input("Input your CSV file name, make sure its in the same folder as this python script: ")

csv_objects = []

with open("testSchools.csv", mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        type_value = row["Type"]
        name_value = row["Name"]
        district=row['District']
        # This prompt needs to be worked on sometimes it outputs the wrong format and that will error out in airtable

        # Refined prompt to ensure correct and clean output
        prompt = f"""
        Find the principal of {name_value} in {district} and extract the following information: 
        their title, first name, last name, and email address. If there is no principal, locate the coordinating 
        supervisor or assistant and provide their details instead. Present the output as a single CSV row with 
        the following fields:

        - School name
        - School district
        - School type (High School, Middle School, Elementary School)
        - Courtesy title (e.g., Mr, Dr, Ms)
        - First name
        - Last name
        - Email address
        - Title (Principal, Assistant Principal, etc.)

        Guidelines:
        1. If a value is unavailable, write 'NA' for that field.
        2. Do not include any notes, explanations, or citations.
        3. Only provide the CSV row formatted as follows, with no additional information:

        Example Output:
        Largo High School, Prince George's County Public Schools, high, Mr, Albert, Lewis, Albert.Lewis@pgcps.org, Principal
        """

        # Prepare messages for API request
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly structured assistant. Only respond with clean CSV-formatted rows as requested."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]

        client = OpenAI(api_key=PERPLEXITY_API_KEY, 
        base_url="https://api.perplexity.ai")

        # chat completion without streaming
        response = client.chat.completions.create(
            model="llama-3.1-sonar-large-128k-online",
            messages=messages,
        )
        csv_objects.append(response.choices[0].message.content)


with open("output_"+file_name, mode='w', newline='') as out_file:
    csv_writer = csv.writer(out_file)
    csv_writer.writerow([
        "School Name", "School District", "School Type", "Courtesy Title",
        "First Name", "Last Name", "Email Address", "Title"
    ])  # Writing the header row

    for row in csv_objects:
        csv_writer.writerow(row.split(", "))





        
