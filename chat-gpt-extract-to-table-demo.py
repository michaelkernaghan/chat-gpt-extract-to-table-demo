import openai
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# This function interacts with the OpenAI GPT model to extract structured data from an email text.
# It sets up the API key, sends a formatted prompt to the GPT model, and returns the parsed response.
def call_openai_gpt(prompt):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts data from emails."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

# This function constructs a prompt for the GPT model to parse an email and extract specific shipment details.
# It processes the GPT response and converts it into a JSON object.
def parse_email_with_gpt(email_text):
    prompt = (
        "You will be given a shipment notification email. Extract the following details and provide them in JSON format:\n"
        "1. PO numbers (list of strings)\n"
        "2. Part numbers (list of strings)\n"
        "3. Quantities (list of integers)\n"
        "4. Tracking number (string)\n"
        "5. Source of the email (string)\n"
        "6. Type of email (string)\n\n"
        "Email:\n"
        f"{email_text}\n\n"
        "Provide the details in the following JSON format and ensure it is a valid JSON:\n"
        "{\n"
        "  \"po_numbers\": [\"PO1\", \"PO2\", ...],\n"
        "  \"part_numbers\": [\"Part1\", \"Part2\", ...],\n"
        "  \"quantities\": [Quantity1, Quantity2, ...],\n"
        "  \"tracking_number\": \"TrackingNumber\",\n"
        "  \"source\": \"Source\",\n"
        "  \"type_of_email\": \"TypeOfEmail\"\n"
        "}"
        "At the conclusion of the task explain the machine learning or NLP techniques you used."
    )
    response = call_openai_gpt(prompt)
    print(f"GPT raw response: {response}")  # Print the raw response for debugging
    
    # Attempt to clean and parse the JSON response
    try:
        # Ensure that the response is a valid JSON string
        response = response[response.find('{'):response.rfind('}')+1]  # Extract JSON part
        details = json.loads(response)
    except json.JSONDecodeError:
        print("Failed to parse JSON response from GPT.")
        details = {}
    return details

# This function processes a batch of test emails containing shipment notifications.
# It reads the emails from a plain text file, parses them, and prints the extracted details.
def process_test_emails_from_text(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
    
    # Split the text into individual emails using a delimiter
    emails = text.split("---EMAIL_SEPARATOR---")
    
    all_data = []

    for i, email in enumerate(emails):
        email = email.strip()  # Remove leading and trailing whitespace
        if email:
            print(f"Processing email {i+1}...")
            shipment_details = parse_email_with_gpt(email)
            print(f"Extracted Entities: {json.dumps(shipment_details, indent=2)}")
            
            po_numbers = shipment_details.get("po_numbers", [])
            part_numbers = shipment_details.get("part_numbers", [])
            quantities = shipment_details.get("quantities", [])
            tracking_number = shipment_details.get("tracking_number", "")
            source = shipment_details.get("source", "")
            type_of_email = shipment_details.get("type_of_email", "")

            # Ensure all lists have the same length
            max_len = max(len(po_numbers), len(part_numbers), len(quantities))
            po_numbers += [""] * (max_len - len(po_numbers))
            part_numbers += [""] * (max_len - len(part_numbers))
            quantities += [""] * (max_len - len(quantities))

            if max_len == 0:
                all_data.append({
                    "Email": i+1,
                    "Purchase Order Number": "",
                    "Part Number": "",
                    "Quantity": "",
                    "Shipping/Transaction Number": tracking_number,
                    "Source": source,
                    "Type of Email": type_of_email
                })
            else:
                for idx in range(max_len):
                    all_data.append({
                        "Email": i+1,
                        "Purchase Order Number": po_numbers[idx],
                        "Part Number": part_numbers[idx],
                        "Quantity": quantities[idx],
                        "Shipping/Transaction Number": tracking_number if idx == 0 else "",
                        "Source": source if idx == 0 else "",
                        "Type of Email": type_of_email if idx == 0 else ""
                    })
        else:
            # Ensure even empty emails are added to the table
            all_data.append({
                "Email": i+1,
                "Purchase Order Number": "",
                "Part Number": "",
                "Quantity": "",
                "Shipping/Transaction Number": "",
                "Source": "",
                "Type of Email": ""
            })
    
    # Generate and print the markdown table
    generate_markdown_table(all_data)

def generate_markdown_table(data):
    headers = ["Email", "Purchase Order Number", "Part Number", "Quantity", "Shipping/Transaction Number", "Source", "Type of Email"]
    table = [headers]
    
    for row in data:
        table.append([str(row[h]) for h in headers])
    
    # Format as markdown
    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(['---'] * len(headers)) + " |\n"
    for row in table[1:]:
        markdown_table += "| " + " | ".join(row) + " |\n"
    
    print(markdown_table)

# Start processing the test emails from the specified plain text file
process_test_emails_from_text('test_emails.txt')
