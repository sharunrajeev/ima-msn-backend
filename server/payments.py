from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from .models import PaymentModel
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from .database import startup_db_client
import razorpay
import os
from .sendmail import send_mail_link

load_dotenv()

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/register/login/")
RZR_KEY_SECRET= os.environ.get('RZR_KEY_SECRET')
RZR_KEY_ID=os.environ.get('RZR_KEY_ID')
MONGO_DB_NAME=os.environ.get('MONGO_DB_NAME')
ALGORITHM=os.environ.get("ALGORITHM")
SECRET_KEY= os.environ.get('SECRET_KEY')
COLLECTION_NAME=os.environ.get("COLLECTION_NAME")


db_helper=startup_db_client()
user_collection=db_helper[COLLECTION_NAME]


razorpay_client = razorpay.Client(auth=(RZR_KEY_ID, RZR_KEY_SECRET))
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")



def decode_token(token: str=Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        elif not user_collection.find_one({"email_id":username}):
            raise HTTPException(status_code=401, detail="Invalid token")
        
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username


@router.get("/initiate/")
async def payment_initiate(token:str=Depends(decode_token)):
    amount=300
    # Replace the values below with your own
    user=user_collection.find_one({"email_id":token})
    receipt_id =f"order-{str(user['phone_no'])[-4:]}-{str(user['name'])[-3:]}-{str(user['_id'])[-3:]}"
    data = { "amount": amount, "currency": "INR", "receipt": receipt_id}
    payment = razorpay_client.order.create(data=data)
    user_collection.update_one({"email_id":token},{"$set":{"transac":jsonable_encoder(PaymentModel(order_id=payment["id"],status=0))}})
    return payment
    
@router.post("/verify/",description="call on payment success")
async def payment_verify(razorpay_payment_id=Body(title="razorpay_payment_id"),razorpay_signature=Body(title="razorpay_signature"),token:str=Depends(decode_token)):
    # Replace the values below with your own
    user=user_collection.find_one({"email_id":token})
    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': user["transac"]["order_id"],
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
        user_collection.update_one({"email_id":token},{"$set":{"transac":jsonable_encoder(PaymentModel(order_id=user["transac"]["order_id"],status=1,pay_id=razorpay_payment_id,signature=razorpay_signature))}})

    # Signature verification successful
    except razorpay.errors.SignatureVerificationError as e:
    # Signature verification failed
        raise HTTPException(status_code=400, detail="Invalid Order Signatures")
    send_mail_link(user["email_id"],user["name"])
    return {"msg","verification successful"}

  


    

