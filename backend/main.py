from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import joblib
import numpy as np
import requests

app=FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)

model=joblib.load("ml/rain_model.pkl")

scaler=joblib.load("ml/scaler.pkl")

API_KEY="31b10d9ca5546f34549e1dad8c6b4086"


def get_weather(city):

    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response=requests.get(url)

    data=response.json()
    
    print(data)

    if response.status_code!=200:

        return {

            "error":data.get("message","Weather API Error")

        }

    return {

        "tavg":data['main']['temp'],

        "tmin":data['main']['temp_min'],

        "tmax":data['main']['temp_max'],

        "pres":data['main']['pressure']

    }


@app.get("/")
def home():

    return {

        "message":"Weather API Running"

    }


@app.get("/predict")
def predict(

    tavg:float,
    tmin:float,
    tmax:float,
    pres:float

):

    features=np.array([[

        tavg,
        tmin,
        tmax,
        pres

    ]])

    scaled_features=scaler.transform(features)

    prediction=model.predict(scaled_features)

    probability=model.predict_proba(scaled_features)

    return {

        "prediction":int(prediction[0]),

        "rain_probability":float(probability[0][1])

    }


@app.get("/predict-live")
def predict_live(city:str):

    weather=get_weather(city)

    if "error" in weather:

        return weather

    features=np.array([[

        weather['tavg'],
        weather['tmin'],
        weather['tmax'],
        weather['pres']

    ]])

    scaled_features=scaler.transform(features)

    prediction=model.predict(scaled_features)

    probability=model.predict_proba(scaled_features)

    return {

        "city":city,

        "weather":weather,

        "prediction":int(prediction[0]),

        "rain_probability":float(probability[0][1])

    }