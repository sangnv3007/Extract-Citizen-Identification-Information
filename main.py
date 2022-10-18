from fastapi import FastAPI, File, UploadFile
from process import ReturnInfoCard, MessageInfo, ExtractCardFront, ExtractCardBack
import json
import os
import cv2
import time
import shutil
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "Tan Dan SJC"}


@app.post("/CitizenIdentification/upload")
def upload(file: UploadFile = File(...)):
    try:
        pathSave = os.getcwd() + '\\anhcancuoc'
        if (os.path.exists(pathSave)):
            with open(f'anhcancuoc/{file.filename}','wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
        else:
            os.mkdir(pathSave)
            with open(f'anhcancuoc/{file.filename}','wb') as buffer:
                shutil.copyfileobj(file.file, buffer)
        obj = ReturnInfoCard(f'anhcancuoc/{file.filename}')
        if (obj.type == "cccd_front"):
            return {"errorCode": obj.errorCode, "errorMessage": obj.errorMessage,
                    "data":[{"id": obj.id, "name": obj.name, "dob": obj.dob,"sex": obj.sex,
                    "nationality": obj.nationality,"home": obj.home, "address": obj.address, "doe": obj.doe, "type": obj.type}]}
        if (obj.type == "cccd_back"):
            return {"errorCode": obj.errorCode, "errorMessage": obj.errorMessage,
                    "data":[{"features": obj.features, "issue_date": obj.issue_date,
                    "type": obj.type}]}
        else:
            return {"errorCode": obj.errorCode, "errorMessage": obj.errorMessage,
                    "data": []}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}
