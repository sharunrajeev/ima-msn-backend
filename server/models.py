
from fastapi import  FastAPI
from pydantic import BaseModel,EmailStr, Field
from enum import Enum

class prefLoc(str, Enum):
    ekm = "Kochi",
    tvm = "Trivandrum"


class PaymentModel(BaseModel):
    order_id: str = Field(...)
    pay_id: str|None = None
    signature: str|None = None
    status:int =Field(...,description="1 if completed otherwise 0")

    class Config:
        schema_extra = {
            "example": {
                "order_id": "order_9A33XWu170gUtm",
                "pay_id": "pay_29QQoUBi66xm2f",
                "signature": "9ef4dffbfd84f1318f6739a3ce19f9d85851857ae648f114332d8401e0949a3d",
                "status":1
            }
        }
class ParticipantModel(BaseModel):
    name: str = Field(...)
    place: str = Field(...)
    phone_no: int = Field(default=...)
    alt_phone_no: int | None = Field(description="optional")
    email_id: str = Field(...)
    alt_email_id:str | None =Field(description="optional")
    pref_loc:str=Field(...)
    transac:PaymentModel|None=None
    reg_no:str|None=None
    password:str |None= None

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "place":"Thrikkakara",
                "phone_no":1000000000,
                "alt_phone_no":9999999999,
                "email_id": "jdoe@hotmail.com",
                "alt_email_id": "johndoe@gmail.com",
                "pref_loc":"Kochi",
                "transac":None,
                "reg_no":None,
                "password":None
            }
        }
class ParticipantModelOut(BaseModel):
    name: str = Field(...)
    place: str = Field(...)
    phone_no: int = Field(default=...)
    alt_phone_no: int | None = Field(description="optional")
    email_id: str = Field(...)
    alt_email_id:str | None =Field(description="optional")
    pref_loc:str=Field(...)
    transac:PaymentModel|None=None
    reg_no:str|None=None

    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "place":"Thrikkakara",
                "phone_no":1000000000,
                "alt_phone_no":9999999999,
                "email_id": "jdoe@hotmail.com",
                "alt_email_id": "johndoe@gmail.com",
                "pref_loc":"Kochi",
                "transac":None,
                "reg_no":None
            }
        }


class Token(BaseModel):
    access_token: str 
    token_type: str
    class Config:
        schema_extra = {
            "example": {
                "accestoken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NGQ1OWNlZi1kYmI4LTRlYTUtYjE3OC1kMjU0MGZjZDY5MTkiLCJqdGkiOiI2Yj",
                "token_type":"Bearer",
            }
        }

class TokenData(BaseModel):
    username: str | None = None

def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}