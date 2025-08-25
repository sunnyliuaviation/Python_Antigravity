import smtplib
import random
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS').split(',')

def get_random_xkcd():
    latest = requests.get("https://xkcd.com/info.0.json").json()["num"]
    comic_number = random.randint(1, latest)
    comic_api = f"https://xkcd.com/{comic_number}/info.0.json"
    comic = requests.get(comic_api).json()
    return comic

def send_comic_email(comic):
    # Download image
    img_data = requests.get(comic["img"]).content

    # Create email
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ', '.join(RECIPIENT_EMAILS)
    msg['Subject'] = f"Good Morning! Start your day with an XKCD comic - {comic['safe_title']} (#{comic['num']})"

    # HTML body: 標題 + alt文字 + 圖片 + URL
    comic_url = f"https://xkcd.com/{comic['num']}/"
    body = f"""
    <h2>{comic['safe_title']}</h2>
    <p><i>{comic['alt']}</i></p>
    <br>
    <img src="cid:comic_image"><br>
    <p>{comic_url}</p>
    """
    msg.attach(MIMEText(body, 'html'))

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
