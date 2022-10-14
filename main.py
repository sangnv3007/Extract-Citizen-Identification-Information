from fastapi import FastAPI, File, UploadFile
from process import ReturnInfoCard
import json
import os
import cv2
import time
import shutil
from starlette.background import BackgroundTasks
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/CitizenIdentification/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        f = open(file.filename, 'wb')
        f.write(contents)
        pathSave = os.getcwd() + '\\ImageCard'
        if (os.path.exists(pathSave)):
            imgName = file.filename + '_'+str(time.time())+'.jpg'
            shutil.copyfile(file.filename, pathSave+"\\" + imgName)
        else:
            os.mkdir(pathSave)
            imgName = file.filename + '_'+str(time.time())+'.jpg'
            shutil.copyfile(file.filename, pathSave+"\\" + imgName)
        obj = ReturnInfoCard(file.filename)
        if (obj.type == "cccd_front"):
            return {"id": obj.id, "name": obj.name, "dob": obj.dob, "sex": obj.sex, "nationality": obj.nationality,
                    "home": obj.home, "address": obj.address, "doe": obj.doe, "type": obj.type, "status": obj.status, "message": obj.message}
        if (obj.type == "cccd_back"):
            return {"features": obj.features, "issue_date": obj.issue_date, "type": obj.type,
                    "status": obj.status, "message": obj.message}
        else:
            return {"type": obj.type, "status": obj.status, "message": obj.message}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}
