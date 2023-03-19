from fastapi import FastAPI
from server.routes import router as list_router
from server.payments import router as payment_router
from server.database import shutdown_db_client,startup_db_client
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "http://0.0.0.0:8000",
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

@app.get("/",tags=["Test"])
async def test_response():
    return "Api Start"
@app.on_event("startup")
def init_db():
    startup_db_client


@app.on_event("shutdown")
def close_client():
    shutdown_db_client