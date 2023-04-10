
from fastapi import  FastAPI
from pydantic import BaseModel,EmailStr, Field
from enum import Enum

class prefLoc(str, Enum):
    ekm = "Kochi",
    tvm = "Trivandrum"
    kzh = "Kozhikode"


class PaymentModel(BaseModel):
    order_id: str = Field(...)
    pay_id: str|None = None
    signature: str|None = None
    class Config:
        schema_extra = {
            "example": {
                "order_id": "order_9A33XWu170gUtm",
                "pay_id": "pay_29QQoUBi66xm2f",
                "signature": "9ef4dffbfd84f1318f6739a3ce19f9d85851857ae648f114332d8401e0949a3d",  
            }
        }
class ParticipantModel(BaseModel):
    name: str = Field(...)
    place: str = Field(...)
    phone_no: str = Field(default=...)
    alt_phone_no: str | None = Field(description="optional")
    email_id: str = Field(...)
    alt_email_id:str | None =Field(description="optional")
    pref_loc:str=Field(...)
    transac:PaymentModel=Field(default={"order_id": "",
                "pay_id": "",
                "signature": ""})
    reg_no:str|None=None
    password:str |None= None
    upi:str|None=None
    status:int=Field(default=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "place":"Thrikkakara",
                "phone_no":'1000000000',
                "alt_phone_no":"9999999999",
                "email_id": "jdoe@hotmail.com",
                "alt_email_id": "johndoe@gmail.com",
                "pref_loc":"Kochi",
                "transac":None,
                "status":0,
                "reg_no":None,
                "password":None,
                "upi":None,
                "status":0


            }
        }
class ParticipantModelOut(BaseModel):
    name: str = Field(...)
    place: str = Field(...)
    phone_no: str = Field(default=...)
    alt_phone_no: str | None = Field(description="optional")
    email_id: str = Field(...)
    alt_email_id:str | None =Field(description="optional")
    pref_loc:str=Field(...)
    transac:PaymentModel|None=None
    reg_no:str|None=None
    upi:str|None=None
    status:int=Field(default=0)


    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "place":"Thrikkakara",
                "phone_no":"1000000000",
                "alt_phone_no":"9999999999",
                "email_id": "jdoe@hotmail.com",
                "alt_email_id": "johndoe@gmail.com",
                "pref_loc":"Kochi",
                "transac":None,
                "reg_no":None,
                "upi":None,
                "status":0
            }
        }

class ParticipantModelLite(BaseModel):
    name: str = Field(...)
    phone_no: str = Field(default=...)
    alt_phone_no: str | None = Field(description="optional")
    email_id: str = Field(...)
    alt_email_id:str | None =Field(description="optional")
    reg_no:str|None=None
    status:int=Field(default=0)

    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "phone_no":"1000000000",
                "alt_phone_no":"9999999999",
                "email_id": "jdoe@hotmail.com",
                "alt_email_id": "johndoe@gmail.com",
                "reg_no":None,
                "status":0

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