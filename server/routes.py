from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
import secrets
from dotenv import load_dotenv
from .models import ParticipantModel,ParticipantModelOut,Token,TokenData,prefLoc
from passlib.context import CryptContext
import re
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .database import startup_db_client
from .sendmail import send_mail
import os

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
load_dotenv()
SECRET_KEY= os.environ.get('SECRET_KEY')
MONGO_DB_NAME=os.environ.get('MONGO_DB_NAME')
ALGORITHM=os.environ.get("ALGORITHM")
TOKEN_EXPIRES=int(os.environ.get("TOKEN_EXPIRES"))
COLLECTION_NAME=os.environ.get("COLLECTION_NAME")


db_helper=startup_db_client()
user_collection=db_helper[COLLECTION_NAME]


def decode_token(token: str = Depends(oauth2_scheme)):
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


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if user_collection.find_one({"email_id": username}):
        user_dict = user_collection.find_one({"email_id": username})
        return ParticipantModel(**user_dict)
    
def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str,):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(MONGO_DB_NAME, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: ParticipantModel = Depends(get_current_user)):
    return current_user


@router.post("/login/", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(os.environ.get("MONGO_DB_NAME"), form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=120)
    access_token = create_access_token(
        data={"sub": user.email_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/current_user/", response_model=ParticipantModelOut)
async def read_users_me(current_user: ParticipantModel = Depends(get_current_active_user)):
    return current_user

@router.get("/participants/",response_model=list[ParticipantModelOut],description="list_participants")
async def read_participants(username:str=Depends(decode_token)):
    users=user_collection.find()
    return list(users)


@router.post("/register/", description='Enter Participant Detail and Call on Form Submit', status_code=status.HTTP_201_CREATED)
async def create_list(lists: ParticipantModel = Body(...),):

    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


    lists = jsonable_encoder(lists)
    
    if user_collection.find_one({"email_id": lists['email_id']}):
        raise HTTPException(status_code=400, detail="User already exists",headers={"X-Error": "Duplicate"})
    if not email_pattern.match(lists['email_id']):
        raise HTTPException(status_code=400, detail="Invalid email address")
    if not email_pattern.match(lists['alt_email_id']) and  not lists['alt_email_id'] == None:
        raise HTTPException(status_code=400, detail="Invalid alternate email address")
    if  user_collection.count_documents({"pref_loc":prefLoc.ekm})>300 and lists["pref_loc"]==prefLoc.ekm:
        raise HTTPException(status_code=400, detail="The Centre Kochi is Full")
    elif user_collection.count_documents({"pref_loc":prefLoc.tvm})>700 and lists["pref_loc"]==prefLoc.tvm:
        raise HTTPException(status_code=400, detail="The Centre Tvm is Full")

   
    password =str(secrets.token_hex(4))
    reg_no =f"reg-{lists['name'].replace(' ','')[0:min(4,len(lists['name']))]}-{secrets.token_hex(2)}"
    lists["password"]=get_password_hash(password)
    lists["reg_no"]=reg_no
    
    new_list_item = user_collection.insert_one(lists)
    #sending username and password through email
    send_mail(lists['email_id'],password,lists['name'])
    #if(response.status_code!=200):
        #raise HTTPException(status_code=500, detail="Unexpected Error Occured",headers={"X-Error": "Unknown"})
    created_list_item = user_collection.find_one({
            "_id": new_list_item.inserted_id
        })
    user = authenticate_user(os.environ.get("MONGO_DB_NAME"), created_list_item["email_id"], password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=TOKEN_EXPIRES)
    access_token = create_access_token(
        data={"sub": user.email_id}, expires_delta=access_token_expires
    )

    return {"username":created_list_item["email_id"],"tokenId":access_token}

@router.get("/centre_count/")
async def fetch_centre_count():
    kochi=user_collection.count_documents({"pref_loc":prefLoc.ekm})
    tvm=user_collection.count_documents({"pref_loc":prefLoc.tvm})
    return {"kochi":kochi,"tvm":tvm}