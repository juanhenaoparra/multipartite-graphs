# app/services/json_upload_service.py
import json

from fastapi import UploadFile

async def handle_json_upload(file: UploadFile):
    try:
        contents = await file.read()
        data = contents.decode()
        json_data = json.loads(data)
        
        print(json_data)
        
        return {"message": "Archivo JSON subido correctamente"}
    except Exception as e:
        return {"error": str(e)}