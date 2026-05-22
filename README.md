PlacesBot
PlacesBot is a Python script that connects to the Apify platform to run actors, extract location data, and export results to CSV. The project is designed with security in mind and keeps your Apify API token out of source control.
---
Features
•	Direct integration with Apify via apify-client
•	CSV export of processed data
•	Secure API token handling using environment variables
---
Requirements
•	Python 3.8+
•	Apify account and API token (https://console.apify.com/account/integrations)
---
Setup
1.	Clone the repository git clone https://github.com/your-username/PlacesBot.git
cd PlacesBot
2.	(Optional) Create a virtual environment
Windows: python -m venv venv
venv\Scripts\activate
macOS/Linux: python3 -m venv venv
source venv/bin/activate
3.	Install dependencies
pip install apify-client python-dotenv
---
Configuration (Hide Your API Key)
Option A: .env file (recommended)
Create a .env file in the project root: APIFY_API_TOKEN=apify_api_your_secret_token_here
Ensure .env is listed in .gitignore.
Add this to the top of PlacesBot.py: from dotenv import load_dotenv
load_dotenv()
Option B: Environment variable
Windows (CMD):
set APIFY_API_TOKEN=your_token
Windows (PowerShell):
$env:APIFY_API_TOKEN="your_token"
macOS/Linux:
export APIFY_API_TOKEN="your_token"
---
Usage
python PlacesBot/PlacesBot.py
---
Project Structure PlacesBot/
├── .gitignore
├── README.md
├── .env                (User-created, not committed)
└── PlacesBot/
└── PlacesBot.py
