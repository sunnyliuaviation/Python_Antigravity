import smtplib
import random
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get your email credentials from GitHub secrets
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')  # Access from environment variables
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')  # Access from environment variables
RECIPIENT_EMAILS = os.getenv('RECIPIENT_EMAILS').split(',')  # Parse the list of recipients from a comma-separated string

# Function to generate a random xkcd comic URL
def get_random_xkcd_url():
    # Get a random comic number between 1 and 3009
    comic_number = random.randint(1, 3010)
    comic_url = f'https://xkcd.com/{comic_number}/'
    print(f"Generated comic URL: {comic_url}")  # Debugging line to show the URL
    return comic_url

# Function to send the comic URL via email to multiple recipients using To
def send_comic_url_email(comic_url):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['Subject'] = "[Today's Random XKCD Comic URL]早八看漫畫"
    
    # Add the URL in the body of the email
    body = f"Here is your random XKCD comic URL for today: {comic_url}"
    msg.attach(MIMEText(body, 'plain'))

    # Add Bcc field for all recipient emails
    msg['To'] = ', '.join(RECIPIENT_EMAILS)  # Bcc all recipients

    # Send the email to all recipients using Gmail's SMTP server
    try:
        print("Attempting to send email...")  # Debugging line
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAILS, msg.as_string())
            print(f"Comic URL '{comic_url}' sent to {', '.join(RECIPIENT_EMAILS)}")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main function to execute the process
def main():
    print("Fetching random XKCD comic URL...")
    comic_url = get_random_xkcd_url()  # Get a random comic URL
    send_comic_url_email(comic_url)    # Send the URL to your email

# Run the main function immediately
if __name__ == "__main__":
    main()
