# Imported libraries
import os
import hashlib
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

images_dict = {}

# API Keys
NEWSAPI_KEY = "enter your news api key" 
WORQHAT_API_KEY = "enter your worqhat api key" 

# Email Configuration
EMAIL_ADDRESS = "example1@gmail.com"
EMAIL_PASSWORD = "enter your app passwird"
RECIPIENT_EMAIL = "example2@gmail.com"

# Function to fetch news from NewsAPI
def get_trending_news(api_url, api_key, max_articles=4): #getting 4 articles and 4 images in the final newspaper
    try:
        print("Fetching trending news...")
        params = {"apiKey": api_key, "language": "en", "country": "us"}
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if "status" in data and data["status"] != "ok":
            print(f"Error fetching news from {api_url}: {data.get('message', 'Unknown error')}")

        print(f"Fetched {len(data.get('articles', []))} articles.")
        return [
            (a.get("title", "No Title"), a.get("description", "No description"), a.get("url", "No URL"))
            for a in data.get("articles", [])[:max_articles]
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from {api_url}: {e}")
        return []


# Function to generate a detailed summary
def generate_summary(title, description):
    summary = (
        f"The article titled '{title}' delves into the following topic: {description}. "
        "This issue holds considerable significance due to its impact on society, businesses, or global events. "
        "The article explores critical developments, challenges, and potential solutions, offering a nuanced perspective."
    )

    words = summary.split()
    if len(words) > 100:
        return " ".join(words[:100]) + "..."
    while len(words) < 50:
        words.append("It elaborates on important details to provide an insightful overview.")
    return " ".join(words)

# Function to wrap text within a specific width
def wrap_text(text, max_line_length):
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        if len(' '.join(current_line + [word])) <= max_line_length:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# Function to generate image using Worqhat API
def generate_image(prompt):
    print(f"Generating image for prompt: {prompt}...")
    url = "https://api.worqhat.com/api/ai/images/generate/v2"
    headers = {
        "Authorization": f"Bearer {WORQHAT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": [prompt],
        "image_style": "Anime",
        "orientation": "Square",
        "output_type": "url"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200 and "image" in data:
            print(f"Image generated successfully for prompt: {prompt}")
            return data["image"]
        else:
            print(f"Error generating image: {data.get('message', 'Unknown error')}")  
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for prompt {prompt}: {e}")
        return None

# Function to download image from URL with unique filename
def download_image(image_url, title):
    print(f"Downloading image for title: {title}...")
    try:
        hash_object = hashlib.md5(title.encode())
        unique_filename = f"image_{hash_object.hexdigest()}.jpg"

        if os.path.exists(unique_filename):
            print(f"Image already downloaded for title: {title}")
            return unique_filename

        img_data = requests.get(image_url).content
        with open(unique_filename, 'wb') as f:
            f.write(img_data)
        print(f"Image downloaded and saved as {unique_filename}.")
        return unique_filename
    except Exception as e:
        print(f"Error downloading image for title {title}: {e}")
        return None

# Function to generate PDF
def generate_pdf(news_list, timestamp):
    pdf_filename = f"The AI Times - {timestamp}.pdf"
    print(f"Generating PDF: {pdf_filename}...")
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter

    # Get current IST date
    ist_timezone = pytz.timezone("Asia/Kolkata")
    current_date_ist = datetime.now(ist_timezone).strftime("%A, %d %B %Y")

    def draw_header():
        c.setFont("Times-Roman", 28)
        c.drawCentredString(width / 2, height - 50, "The AI Times")
        c.setFont("Times-Italic", 12)
        c.drawCentredString(width / 2, height - 70, current_date_ist)
        c.setLineWidth(0.5)
        c.line(50, height - 90, width - 50, height - 90)

    def draw_page_number(page_num):
        c.setFont("Helvetica", 10)
        c.drawString(50, 30, f"Page {page_num}")

    y = height - 120
    page_num = 1

    draw_header()

    for idx, (title, content, url) in enumerate(news_list):
        if idx > 0 and idx % 2 == 0:  # Start a new page after two articles
            c.showPage()
            page_num += 1
            draw_header()
            y = height - 100

        # Title
        c.setFont("Helvetica-Bold", 14)
        wrapped_title = wrap_text(title, 70)
        for line in wrapped_title:
            c.drawCentredString(width / 2, y, line)
            y -= 20

        # Image
        if title not in images_dict:
            image_url = generate_image(title)
            if image_url:
                image_path = download_image(image_url, title)
                if image_path:
                    images_dict[title] = image_path

        image_x = (width / 2) - 100
        if title in images_dict and os.path.exists(images_dict[title]):
            if y - 150 < 50:
                c.showPage()
                page_num += 1
                draw_header()
                y = height - 100
            c.drawImage(images_dict[title], image_x, y - 150, width=200, height=150)
            y -= 170

        # Summary
        summary = generate_summary(title, content)
        c.setFont("Helvetica", 10)
        wrapped_summary = wrap_text(summary, 60)

        for line in wrapped_summary:
            if y < 80:
                c.showPage()
                page_num += 1
                draw_header()
                y = height - 100
            c.drawCentredString(width / 2, y, line)
            y -= 15

        # URL(read me link)
        if y < 80:
            c.showPage()
            page_num += 1
            draw_header()
            y = height - 100
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(colors.blue)
        link_text = "Read More"
        link_width = c.stringWidth(link_text, "Helvetica-Bold", 10)
        link_x = (width / 2) - (link_width / 2)
        c.drawString(link_x, y, link_text)
        c.linkURL(url, (link_x, y - 2, link_x + link_width, y + 10), relative=0)
        c.setFillColor(colors.black)
        y -= 50  # Reduced gap for better flow

        draw_page_number(page_num)

    c.save()
    print(f"PDF generated: {pdf_filename}")
    return pdf_filename

# Function to send email with PDF attachment
def send_email_with_pdf(pdf_path):
    print(f"Sending email with PDF: {pdf_path}...")
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = "The AI Times Newsletter"

        body = "Please find the latest edition of 'The AI Times' attached."
        msg.attach(MIMEText(body, 'plain'))

        # Attach PDF
        with open(pdf_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f"attachment; filename={os.path.basename(pdf_path)}"
            )
            msg.attach(part)

        # Connect to SMTP server and send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main task function
def task():
    print("Starting the task...")
    api_url = "https://newsapi.org/v2/top-headlines"
    max_articles = 4
    news_articles = get_trending_news(api_url, NEWSAPI_KEY, max_articles=max_articles)

    if news_articles:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"Generating PDF with {len(news_articles)} articles...")
        pdf_path = generate_pdf(news_articles, timestamp)
        send_email_with_pdf(pdf_path)
    else:
        print("No news articles available.")

if __name__ == "__main__":
    task()