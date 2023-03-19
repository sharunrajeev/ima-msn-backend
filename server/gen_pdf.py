from fastapi import APIRouter,Depends, HTTPException, status,responses
from pydantic import BaseModel
import jinja2
from .models import ParticipantModelOut
from .database import startup_db_client
import os
from dotenv import load_dotenv
from .users import decode_token
from io import BytesIO
from xhtml2pdf import pisa


load_dotenv()
router = APIRouter()


COLLECTION_NAME=os.environ.get("COLLECTION_NAME")


db_helper=startup_db_client()
user_collection=db_helper[COLLECTION_NAME]

@router.post("/generate/")
async def convert_to_pdf(token:str=Depends(decode_token)):
  # Convert the data to a dictionary
    user_dict = user_collection.find_one({"email_id": token})
    
    # Set the path to the HTML template
    template_path = "./template/pdf_template.html"

    # Load the HTML template and create a Jinja2 environment
    with open(template_path, "r") as f:
        html_template = f.read()
    jinja_env = jinja2.Environment(loader=jinja2.BaseLoader(), autoescape=True)

    # Render the HTML template with the data using Jinja2
    rendered_html = jinja_env.from_string(html_template).render(**user_dict)

    pdf_buffer = BytesIO()

    # Generate the PDF from the rendered HTML using pisa
    pisa_status = pisa.CreatePDF(
        rendered_html,
        dest=pdf_buffer,
        encoding="UTF-8"
    )

  # Check if the PDF was generated successfully
    if pisa_status.err:
        return {"error": "Failed to generate PDF"}

    # Get the PDF content from the buffer
    pdf_content = pdf_buffer.getvalue()

    # Set the content type and content disposition headers
    headers = {
        "Content-Type": "application/pdf",
        "Content-Disposition": "attachment;filename=document.pdf"
    }

    # Create a response object with the PDF as the content and the headers
    response = responses.Response(content=pdf_content, headers=headers)

    # Return the response
    return response