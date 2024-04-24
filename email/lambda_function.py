import base64

def lambda_handler(event, context):
    
    html_content = return_html()

    # Return the HTML content
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html_content
    }


def return_html():

    # Construct the HTML content with the embedded image, increased size, and contact form
    with open("index.html", "r") as file:
        html_content = file.read()

    return html_content

