import json
from fastapi import UploadFile

async def handle_json_upload(file: UploadFile):
    try:
        contents = await file.read()
        data = contents.decode()
        json_data = json.loads(data)

        # Extraer la parte deseada del JSON
        graph_data = json_data.get('graph')
        if graph_data:
            graph = graph_data[0]
            desired_json = {
                "name": graph.get('name'),
                "data": graph.get('data')
            }
            return desired_json
        else:
            return {"error": "El JSON no contiene la clave 'graph' o no tiene el formato esperado."}
    except Exception as e:
        return {"error": str(e)}