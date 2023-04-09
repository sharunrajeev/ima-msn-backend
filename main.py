from fastapi import FastAPI
from server.users import router as list_router
from server.payments import router as payment_router
from server.gen_pdf import router as pdf_router
from server.database import shutdown_db_client,startup_db_client
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

description = """## Users

You will be able to:

* **Login User**.
* **Get current user**.
* **Get users**.
* **Register Participants**.
* **Count of each centres**.

## Payment

You will be able to:

* **Initiate payment and create order ID**.
* **Verify Payment after success and change payment status from 0 to 1**.

## PDF

You will be able to:

* **Generate User Data as PDF after login**."""

app = FastAPI(
    title="IMA MSN API",
    description=description,
    version="1.2.0",
)


origins = [
    "http://localhost",
    "http://0.0.0.0:8000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
description="""You will be able to:

* **Login User**.
* **Get current user**.
* **Get users**.
* **Register Participants**.
* **Count of each centres**.
"""

app.include_router(list_router, tags=["User"])
app.include_router(payment_router,tags=["Payment"],prefix="/payment")
app.include_router(pdf_router,tags=["PDF"],prefix="/pdf")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/",tags=["Test"])
async def test_response():
    return "Api Start"



@app.on_event("shutdown")
def close_client():
    shutdown_db_client