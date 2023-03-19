from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")

mongodb_client = MongoClient(config["MONGO_URL"])


def startup_db_client():
    database = mongodb_client[config["MONGO_DB_NAME"]]
    print("Connected to the MongoDB database!")
    return database


def shutdown_db_client():
    mongodb_client.close()