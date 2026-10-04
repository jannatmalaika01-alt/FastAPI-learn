from fastapi import FastAPI,Path,HTTPException,Query
from fastapi.responses import JSONResponse
import json
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal

app=FastAPI()

class Patient(BaseModel):
    id: Annotated[int,Field(...,description="id of patient",example=1)]
    name: Annotated[str,Field(...,description="name of patient",example="John Doe")]
    city: Annotated[str,Field(...,description="name of city",example="Lahore")]
    gender: Annotated[Literal['Male','Female','other'],Field(...,description="gender",example="Male,Female,other")]
    height: Annotated[int,Field(...,gt=0,description="height of patient",example=186)]
    weight: Annotated[int,Field(...,gt=0,description="weight of patient",example=88)]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height/100)**2,2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return "underweight"
        elif self.bmi<25:
            return "normal"
        else:
            return "overweight"

def load_data():
    with open("patients.json",'r') as f:
        data=json.load(f)
        return data

def save_data(data):
    with open("patients.json","w") as f:
        json.dump(data,f,indent=4)

@app.get("/")
def hello():
    return {'message':"Patient manager api"}

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
    raise HTTPException(status_code=404,detail="patient not found")

@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="sort by bmi,weight,height"),order:str=Query('asc',description="order by ascending order")):
    valid_feilds=['weight','height','bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail=f"invalid field, choose from {valid_feilds}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="invalid order, choose between asc and desc")
    data=load_data()
    sort_order=True if order=='asc' else False
    sorted_data=sorted(data,key=lambda x:x[sort_by],reverse=sort_order)
    return sorted_data

@app.post("/create")
def create_patient(patient:Patient):
    data=load_data()

    for existing_patient in data:
        if existing_patient['id']==patient.id:
            raise HTTPException(status_code=400,detail="patient already exists")

    data.append(patient.model_dump())

    save_data(data)

    return JSONResponse(status_code=201,content={"message":"patient created successfully","id":patient.id})