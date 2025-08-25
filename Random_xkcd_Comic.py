import smtplib
import random
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Get your email credentials from GitHub secrets (環境變數)
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS').split(',')

# Function to get random XKCD comic info from JSON API
def get_random_xkcd():
    latest = requests.get("https://xkcd.com/info.0.json").json()["num"]
    comic_number = random.randint(1, latest)
    comic_api = f"https://xkcd.com/{comic_number}/info.0.json"
    comic = requests.get(comic_api).json()
    return comic

# Function to send comic via email
def send_comic_email(comic):
    # Download image
    img_data = requests.get(comic["img"]).content

    # Create email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(RECIPIENT_EMAILS)
    msg['Subject'] = f"[Today's Random XKCD] 早八看漫畫 - {comic['safe_title']} (#{comic['num']})"

    # HTML body with inline image
    body = f"""
    <h2>{comic['safe_title']}</h2>
    <p><i>{comic['alt']}</i></p>
    <p><a href="https://xkcd.com/{comic['num']}/">原始連結</a></p>
    <br>
    <img src="cid:comic_image">
    """
    msg.attach(MIMEText(body, 'html'))

    # Attach image as inline
    image = MIMEImage(img_data, name=f"xkcd_{comic['num']}.png")
    image.add_header('Content-ID', '<comic_image>')
    msg.attach(image)

    # Send email
    try:
        print("Attempting to send email...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAILS, msg.as_string())
            print(f"✅ XKCD #{comic['num']} - '{comic['safe_title']}' 已寄出給 {', '.join(RECIPIENT_EMAILS)}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Main
def main():
    print("Fetching random XKCD comic...")
    comic = get_random_xkcd()
    send_comic_email(comic)

if __name__ == "__main__":
    main()
