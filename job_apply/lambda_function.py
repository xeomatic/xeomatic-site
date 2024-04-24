import json
import base64
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

ses = boto3.client('ses', region_name='eu-west-1')  # Replace 'YOUR_REGION' with your AWS region

def lambda_handler(event, context):
 
    if event["requestContext"]["http"]["method"] == "POST":

        print(event) 

        html_content = return_html()

        send_application(event)
        
       # Return the HTML content
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": html_content
        }

        
        return response

    elif event["requestContext"]["http"]["method"] == "GET":
        
        html_content = return_html()

        # Return the HTML content
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": html_content
        }


def send_application(event):
    try:
        print(event['body'])
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        subject = body['message']
        pdf_file = event['body']
        
        # Construct email
        msg = MIMEMultipart()
        msg['From'] = 'info@xeomatic.com'  # Replace with sender's email address
        msg['To'] = "info.xeomatic@gmail.com"
        msg['Subject'] = subject

        text_body = f"Dear {name},\n\nPlease find the attached PDF file.\n\nBest regards,\nYour Company"

        msg.attach(MIMEText(text_body, 'plain'))

        pdf_attachment = MIMEApplication(pdf_file, 'pdf')
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename='uploaded_file.pdf')
        msg.attach(pdf_attachment)

        # Send email
        response = ses.send_raw_email(
            Source=msg['From'],
            Destinations=[msg['To']],
            RawMessage={'Data': msg.as_string()}
        )

        print("Email sent:", response)

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully!'})
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Error sending email'})
        }


def return_html():

    # Construct the HTML content with the embedded image, increased size, and contact form
    with open("index.html", "r") as file:
        html_content = file.read()

    return html_content