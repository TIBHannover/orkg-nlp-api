# -*- coding: utf-8 -*-
from fastapi import APIRouter, Form, UploadFile
from fastapi.responses import HTMLResponse

from app.common.util.decorators import log
from app.models.pdf import ExtractTableRequest, ExtractTableResponse
from app.services.pdf import PdfService

router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.post("/table/extract", response_model=ExtractTableResponse, status_code=200)
@log(__name__)
def extracts_table(file: UploadFile, payload: ExtractTableRequest = Form(...)):
    pdf_service = PdfService()
    return pdf_service.extract_table(
        file.file, payload.page_number, payload.region, payload.lattice
    )


@router.post("/convert", response_class=HTMLResponse, status_code=200)
@log(__name__)
def converts_pdf(file: UploadFile):
    pdf_service = PdfService()
    return pdf_service.convert_pdf(file.file)
