from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, HTMLResponse
from fastapiUtils import cwd_path


def get_html_content(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


router = APIRouter()
