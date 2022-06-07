from fastapi import APIRouter, UploadFile, Form

from app.models.pdf import ExtractTableRequest, ExtractTableResponse
from app.services.pdf import PdfService

router = APIRouter(
    prefix='/pdf',
    tags=['pdf']
)


@router.post('/table/extract', response_model=ExtractTableResponse, status_code=200)
def extracts_table(file: UploadFile, payload: ExtractTableRequest = Form(...)):
    pdf_service = PdfService()
    return pdf_service.extract_table(file.file, payload.page_number, payload.region, payload.lattice)
