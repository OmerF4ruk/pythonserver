import os 
import psycopg2
from dotenv import load_dotenv
from machine import Machine
from flask import Flask,request

CREATE_CSV_TABLE="COPY (select * from herb_datas where device_id=%s) TO 'C:\\Users\\Pc\\Desktop\\pythonserver\\datas.csv' DELIMITER ',' CSV HEADER;"
UPDATE_PREDICT_TABLE=""" UPDATE predict SET predict = %s WHERE device_id = %s""" 
load_dotenv()


connection = psycopg2.connect(
    host="localhost",
    database="Herb",
    user="postgres",
    password="123456")
app= Flask(__name__)

@app.get("/")
def home():
    return "hello world"


def create_csv(id):
    cursor = connection.cursor()
    cursor.execute("COPY (select * from herb_datas where device_id=(%s)) TO 'C:\\Users\\Pc\\Desktop\\pythonserver\\datas.csv' DELIMITER ',' CSV HEADER;", 
    (str(id),))
    connection.commit()

@app.post("/predict")
def predict():
    datas = request.get_json()
    create_csv(datas["device_id"])
    data=[datas["air_humidity"],datas["air_temperature"],datas["soil_temperature"],datas["sulanma"]]
   
    tahmin=str(Machine(data))
    print(tahmin)

    cursor = connection.cursor()
    cursor.execute(
    "UPDATE predict SET predict=(%s)"
    " WHERE device_id = (%s)", 
    (tahmin,datas["device_id"]))
    connection.commit()
    return {"predict":tahmin},201



