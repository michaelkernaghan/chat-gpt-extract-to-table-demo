# Chat GPT Extract to Table Demo

This repository demonstrates how to use OpenAI's GPT-4 model to extract structured data from emails and format it into a markdown table. The code processes a batch of emails, extracts shipment details, and generates a markdown table that includes all relevant information.

![Demo Screenshot](images/demo-screenshot.png)

## Features

- Extracts PO numbers, part numbers, quantities, tracking numbers, source, and type of email from emails.
- Processes multiple emails and ensures all are included in the final output.
- Generates a markdown table with the extracted information.
- Handles missing data and includes default values for consistency.
- Chat GPT 4 is asked to explain the Machine Learning techniques, if any, that it used to extract the entities from the emails.

## Requirements

- Python 3.7+
- `openai` library
- `python-dotenv` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/michaelkernaghan/chat-gpt-extract-to-table-demo.git
    cd chat-gpt-extract-to-table-demo
    ```

2. (Optional) Create and activate a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

## Usage

1. Prepare your email data in a plain text file (`test_emails.txt`), separating individual emails with `---EMAIL_SEPARATOR---`.

2. Run the script to process the emails and generate the markdown table:
    ```sh
    python3 chat-gpt-extract-to-table-demo.py
    ```

3. The script will output a markdown table with the extracted information to the console.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss any changes or improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- OpenAI for providing the GPT-4 model.
- All contributors who helped make this project better.

---
![Chat GPT Cat](images/chat_gpt_cat.png)