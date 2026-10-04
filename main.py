from fastapi import FastAPI,Path,HTTPException,Query
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
        raise HTTPException(status_code=404,detail="patient not found")

@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="sort by bmi,weight,height"), order:str=Query('asc',description="order by ascending order")):
    valid_feilds=['weight','height','bmi']
    if sort_by not in valid_feilds:
        raise HTTPException(status_code=400,detail=f"invalid field, choose from {valid_feilds}")
    if order not in ['asc','desc']:
         raise HTTPException(status_code=400,detail=f"invalid field, choose between valid and invalid")
    data=load_data()
    sort_order=True if order=='asc' else False
    sorted_data=sorted(data,key=lambda x:x[sort_by],reverse=sort_order)
    return sorted_data