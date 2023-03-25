from fastapi import APIRouter,Depends, HTTPException, status,responses
from pydantic import BaseModel
from jinja2 import Environment, FileSystemLoader
from .models import ParticipantModelOut
from .database import database
import os
from dotenv import load_dotenv
from .users import decode_token
from io import BytesIO
from xhtml2pdf import pisa
from fastapi.responses import StreamingResponse
from fpdf import FPDF



load_dotenv()
router = APIRouter()

COLLECTION_NAME=os.environ.get("COLLECTION_NAME")
user_collection=database[COLLECTION_NAME]


class PDF(FPDF):
    def header(self):
        # Logo
       # self.image('./static/images/ekm_qr.png', 10, 8, 20)
        # Arial bold 15
        self.set_font('Arial', 'B', 20)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(40, 15, 'IMA MSN', 1, 0, 'C')

        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) , 0, 0, 'C')


@router.get("/generate/")
async def convert_to_pdf(token:str=Depends(decode_token)):
  # Convert the data to a dictionary
  
  
    # Set the path to the HTML template
    template_path = "./template/"


    user_dict = user_collection.find_one({"email_id": token})
  #   jinja_env = Environment(loader=FileSystemLoader(template_path))
  #   jinja_env.globals.update(map_embed)
  #   # Render the HTML template with the data using Jinja2
  #   rendered_html = jinja_env.get_template("pdf_template.html").render(**user_dict)
  #   pdf_buffer = BytesIO()
  #   # Generate the PDF from the rendered HTML using pisa
  #   pisa_status = pisa.CreatePDF(
  #       rendered_html,
  #       dest=pdf_buffer,
  #       encoding="UTF-8"
  #   )

  # # Check if the PDF was generated successfully
  #   if pisa_status.err:
  #       return {"error": "Failed to generate PDF"}

  #   # Get the PDF content from the buffer
  #   pdf_content = pdf_buffer.getvalue()

  #   # Set the content type and content disposition headers
  #   headers = {
  #       "Content-Type": "application/pdf",
  #       "Content-Disposition": f"attachment;filename={user_dict["reg_no"]}.pdf"
  #   }

  #   # Create a response object with the PDF as the content and the headers
  #   response = responses.Response(content=pdf_content, headers=headers)

  #   # Return the response
  
    pdf = PDF('P', 'mm', 'A4')

    # Add a page
    pdf.add_page()

    # Set font and font size
    # Add image to center of page
    pdf.image("./static/images/ekm_qr.png" if user_dict["pref_loc"]=="Kochi" else "./static/images/tvm_qr.png"  , x=10, y=pdf.h- 140, w=30)
    # Add text to page
    # Add fields to page
    pdf.set_font("Arial", "B",size=16)
    pdf.line(10, 30, 200, 30)
    pdf.cell(100, 20, f"Reg No: {user_dict['reg_no']}", align="L")
    pdf.line(10, 50, 200, 50)
    pdf.set_font("Arial", size=12)
   
    pdf.ln(20)

    pdf.cell(100, 20, f"Name: {user_dict['name']}", align="L")
    pdf.ln(10)
    pdf.cell(100, 20, f"Place: {user_dict['place']}", align="L")
    pdf.ln(10)
    pdf.cell(100, 20, f"Phone: {user_dict['phone_no']}", align="L")
    pdf.ln(10)
    pdf.cell(100, 20, f"Email: {user_dict['email_id']}", align="L")
    pdf.ln(10)
    pdf.cell(100, 20, f"Venue: {user_dict['pref_loc']}", align="L")
    pdf.ln(10)

    pdf.cell(100, 20, "Time: 8.00am", align="L")
    pdf.ln(10)
    pdf.ln(10)
    pdf.ln(10)
    pdf.ln(10)
    pdf.cell(100, 20, "Scan the QR Code for Location", align="L")


    # Create a byte stream buffer to hold the PDF data
    pdf_buffer = pdf.output(dest='S').encode('latin1')

    # Return the PDF as a StreamingResponse
    return StreamingResponse(
        iter([pdf_buffer]),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment;filename={user_dict['reg_no']}.pdf"
        }
    )
    #return response