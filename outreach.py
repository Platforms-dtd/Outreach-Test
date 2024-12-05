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
        
        # This prompt needs to be worked on sometimes it outputs the wrong format and that will error out in airtable
        prompt = f"Find the Principal of {name_value} in Prince George County and extract their title, first name, last name, email. If there is no principal, find the coordinating supervisor or assistant. I need this to be presented as csv row with the school name, school district, school type (high,middle,elementary), courtesy title (mr,dr,ms), first name, last name, email address, title (principal, coordinating supervisor, neither). If any of the values are not avaible the write NA for that field. Only output the csv string and nothing else. "
        prompt = eval(f"f'{prompt}'")

        messages = [
            {
                "role": "system",
                "content": (
                    "You are an artificial intelligence assistant and you need to"
                    "engage in a helpful, detailed, polite conversation with a user."
                ),
            },
            {   
                "role": "user",
                "content": (
                    prompt
                ),
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


with open("output_"+file_name, "w") as file:
    for str in csv_objects:
        file.write(str+"\n")





        