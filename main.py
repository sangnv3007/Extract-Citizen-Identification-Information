from fastapi import FastAPI, File, UploadFile
from process import ReturnInfoCard
import json
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
@app.post("/CitizenIdentification/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(file.filename, 'wb') as f:
            f.write(contents)
            obj = ReturnInfoCard(file.filename)
            if(obj.type=="cccd_front"):
                return {"id": obj.id,"name": obj.name,"dob": obj.dob,"sex": obj.sex,"nationality":obj.nationality,
                        "home":obj.home,"address":obj.address,"doe":obj.doe,"type":obj.type,"status": obj.status,"message": obj.message}
            if(obj.type=="cccd_back"):
                return {"features": obj.features,"issue_date": obj.issue_date,"type": obj.type,
                        "status": obj.status,"message": obj.message}
            else:
                return {"type": obj.type,"status": obj.status,"message": obj.message}
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    return {"message": f"Successfuly uploaded {file.filename}"}
