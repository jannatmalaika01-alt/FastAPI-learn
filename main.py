from fastapi import FastAPI,Path
import json

app=FastAPI()

def load_data():
    with open("patients.json",'r') as f:
        data=json.load(f)
        return data
    
@app.get("/")
def hello():
    return {'message': "Patient manager api"}

@app.get("/about")
def about():
    return {"message":"this is the about page of patient management api"}

@app.get("/views")
def views():
    data=load_data()
    return data

@app.get("/patients/{patient_id}")
def get_patient(patient_id:int=Path(...,description="id of patient",example=1)):
    data=load_data()
    for patient in data:
        if patient['id']==patient_id:
            return patient
        return {"error":"patient not found"}