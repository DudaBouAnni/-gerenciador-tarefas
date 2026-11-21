from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

from src.database import engine, Base
from src.routes.tasks import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow",
    description="Sistema de gerenciamento de tarefas",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="src/static"),
    name="static"
)

templates = Jinja2Templates(directory="src/templates")

app.include_router(tasks_router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )