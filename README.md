# CSI-Hackathon-2025
CSI Hackathon - 2025.
1. This Python project has been designed to generate a generalized PDF newsletter, The AI Times, featuring trending news articles.

2. It will fetches news using the NewsAPI, categorizes articles by topic, and creates detailed summaries for each story. 

3. The script integrates with the Worqhat API to generate illustrative images for the articles, ensuring each story is visually engaging and adequately explained. 

4. The PDF is designed with a polished layout, including a dynamic header showing the date, titles, summaries, images, and clickable links for further reading.

5. Every morning at a designated time, the PDF will be mailed to a particular Email address, allowing for instantaneous distribution of news. 

6. The seamless integration of APIs, PDF generation, and image processing to create an aesthetically pleasing and informative document has been displayed here, along with the method of sending it to interested readers.

Brief Explanation
This project automates the generation of a personalized newsletter titled "The AI Times". It involves:

Fetching trending news articles using the NewsAPI.
Summarizing articles with concise descriptions for easy readability.
Generating unique images related to the article titles using Worqhat API.
Formatting the articles and images into a professional PDF using ReportLab.
Sending the generated newsletter as an email attachment via SMTP.
Tools and Technologies Used
Languages
Python: The primary programming language for implementing logic and automation.
APIs
NewsAPI: Fetches trending articles.
Worqhat API: Generates AI-based images for each article.
Libraries
requests: Makes API calls to fetch news and images.
hashlib: Creates unique filenames for downloaded images.
reportlab: Generates the formatted PDF newsletter.
smtplib: Sends emails with attachments.
pytz: Handles timezone-related functionalities.
email: Manages email formatting and attachments.
Utilities
Gmail App Password: Used for SMTP authentication to send emails.
Setup Instructions
1. Prerequisites
Ensure you have the following installed:

Python 3.8+
Pip (Python Package Manager)
2. Clone the Repository
bash
Copy
Edit
git clone <repository-url>
cd <repository-folder>
3. Install Dependencies
Run the following command to install required Python libraries:

bash
Copy
Edit
pip install -r requirements.txt
4. Configure API Keys
Obtain an API key from NewsAPI.
Obtain an API key from Worqhat AI for image generation.
Replace the placeholders in the script:
NEWSAPI_KEY = "enter your news api key"
WORQHAT_API_KEY = "enter your worqhat api key"
5. Configure Email Credentials
Replace the placeholders for the email configuration in the script:

python
Copy
Edit
EMAIL_ADDRESS = "example1@gmail.com"
EMAIL_PASSWORD = "enter your app password"
RECIPIENT_EMAIL = "example2@gmail.com"
6. Run the Project
Run the following command to start the newsletter generation process:

bash
Copy
Edit
python main.py
Commands and Execution
Run the Script
bash
Copy
Edit
python main.py
Output
A PDF named The AI Times - <timestamp>.pdf is generated in the working directory.
The newsletter is emailed to the recipient specified in the script.