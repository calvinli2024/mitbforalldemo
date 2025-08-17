from fastapi import FastAPI
from starlette.responses import FileResponse
from starlette.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI()

templates = Jinja2Templates(directory=".")

@app.get("/")
def index():
    return FileResponse("index.html")

@app.post("/form") 
async def form(request: Request):
    async with request.form() as form:
        return templates.TemplateResponse(
            "echo.html",
            context={"comment": form['comment'], "request": request}
        )