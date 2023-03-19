from fastapi import FastAPI
from .routes import router as list_router
from.payments import router as payment_router
from .database import shutdown_db_client,startup_db_client
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://ima-msn-backend-production.up.railway.app",
    "https://ima-msn-backend-production.up.railway.app",
    "http://localhost",
    "http://0.0.0.0:80"
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(list_router, tags=["User"])
app.include_router(payment_router,tags=["Payment"],prefix="/payment")

@app.get("/")
async def start_response():
    return "Api Start"
@app.on_event("startup")
def init_db():
    startup_db_client


@app.on_event("shutdown")
def close_client():
    shutdown_db_client