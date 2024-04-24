import base64
import urllib.parse
import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    if event["requestContext"]["http"]["method"] == "POST":
        name, sender_email, message = get_params(event)
        
        print(f'{name}, {sender_email} {message}')

        if name:
            html_content = get_html_with_image()
            html_content_with_success = html_content.replace('<script>', '<script> showSuccessMessage(true);')
            send_email(name, sender_email, message)

       # Return the HTML content
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": html_content_with_success
        }

        
        return response

    elif event["requestContext"]["http"]["method"] == "GET":
        
        html_content = get_html_with_image()

        # Return the HTML content
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": html_content
        }

def get_html_with_image():
    html_content = return_html()
    image_data = read_image()
        
    # Construct the image tag with the image data
    image_tag = '<img src="data:image/png;base64,{0}" alt="Xeomatic Logo" class="logo">'.format(image_data)

    # Replace the placeholder with the image tag
    html_content_with_image = html_content.replace('<img src="data:image/png;base64,""" + {image_data} + """ alt="Xeomatic Logo" class="logo">', image_tag)

    return html_content_with_image

def read_image():
    # Read the image file and encode it into base64
    with open("xeomatic_logo.png", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")
    return image_data

def return_html():

    # Construct the HTML content with the embedded image, increased size, and contact form
    with open("index.html", "r") as file:
        html_content = file.read()

    return html_content

def get_params(event):
    
    encoded_string = event["body"]

    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode("utf-8")
    
    decoded_url = urllib.parse.unquote_plus(decoded_string)
    
    form_fields = {}
    for field in decoded_url.split("&"):
        key, value = field.split("=")
        form_fields[key] = value

    # Get name, email, and message from form fields
    name = form_fields.get("name", "")
    email = form_fields.get("email", "")
    message = form_fields.get("message", "")

    return name, email, message
    
def send_email(name, customer_email, body_text):
    recipient_email = "info.xeomatic@gmail.com"
    # Initialize the SES client
    ses_client = boto3.client('ses')
    
    # Email parameters
    sender_email = "info@xeomatic.com"
    subject = f'Customer: {name}, email: {customer_email}'
    
    # Try to send the email
    try:
        # Send email using the SES send_email function
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [
                    recipient_email,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': subject,
                },
            },
            Source=sender_email
        )
        print("Email sent successfully! Message ID:", response['MessageId'])
        return {
            'statusCode': 200,
            'body': 'Email sent successfully!'
        }
    except ClientError as e:
        print("Error sending email:", e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': 'Error sending email: ' + e.response['Error']['Message']
        }