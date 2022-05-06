from fastapi import APIRouter

router = APIRouter(
    prefix='/annotate',
    tags=['annotate']
)


@router.get('/cs')
def cs_ner_annotator(title: str, abstract: str):
    return {
        'title': title,
        'abstract': abstract
    }
