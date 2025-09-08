from fastapi import APIRouter, File, Request
from src.package.pdf.setup import pdf_to_word
from src.routers import store

router = APIRouter()


@router.post("/pdf-to-word")
async def pdf_to_word_api(file_id: int, req: Request = None):
    ip = req.client.host
    file_path = store.file_id(file_id)
    name = file_path.name
    doc_path = store.sendPath / f"{name}.docx"
    pdf_to_word(file_path.path, doc_path)
    file_id = store.addUseFile(ip, filename=f"{name}.docx")
    return file_id
