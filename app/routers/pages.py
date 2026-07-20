"""
HTML page routes — serves the form UI that replaces the Streamlit widgets.
Rendered with Jinja2 and calls the JSON API via fetch() in the browser.
"""
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
