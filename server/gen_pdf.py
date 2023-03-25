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


@router.get("/generate/")
async def convert_to_pdf(token:str=Depends(decode_token)):
  # Convert the data to a dictionary
  
  
    # Set the path to the HTML template
    template_path = "./template/"


    user_dict = user_collection.find_one({"email_id": token})
    map_embed = {
    "map": template_path+"ekm-qr.png" if user_dict["pref_loc"]=="Kochi" else template_path+"tvm-qr.png",
    }  
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
  
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font and font size
    pdf.set_font("Arial", size=20)

    # Add image to center of page
    pdf.image("./static/images/ekm_qr.png" if user_dict["pref_loc"]=="Kochi" else "./static/images/tvm_qr.png"  , x=pdf.w / 2 - 50, y=pdf.h / 2 - 50, w=50)

    # Add text to page
    pdf.cell(0, 20, "IMA MSN",align="C")
    pdf.ln(10)
    # Add fields to page
    pdf.set_font("Arial", size=16)

    pdf.cell(100, 20, f"Reg No: {user_dict['reg_no']}", align="L")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    pdf.cell(100, 20, f"Name: {user_dict['name']}", align="L")
    pdf.ln(10)
    pdf.cell(100, 20, f"Place: {user_dict['place']}", align="L")
    pdf.ln(10)

    pdf.cell(100, 20, f"Venue: {user_dict['pref_loc']}", align="L")
    pdf.ln(10)

    pdf.cell(100, 20, "Time: 8.00am", align="L")
    pdf.ln(10)




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