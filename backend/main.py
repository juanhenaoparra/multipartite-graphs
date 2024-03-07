# main.py
from fastapi import FastAPI
from app.api.endpoints import file_upload
import app.config.settings as settings

settings.Base.metadata.create_all(bind=settings.engine)
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

# Importar y registrar los routers de los endpoints
app.include_router(file_upload.router, prefix="/api")


# Iniciar la aplicación si este archivo se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)