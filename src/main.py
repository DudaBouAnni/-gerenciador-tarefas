from fastapi import FastAPI

from src.database import engine, Base

from src.routes.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow",
    description="Sistema de gerenciamento de tarefas",
    version="1.0.0",
)

app.include_router(tasks_router)

@app.get("/")
def home():
    return {
        "message": "Bem vindo ao TaskFlow!"
    }