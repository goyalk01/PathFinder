from __future__ import annotations

import os
from dotenv import load_dotenv

# Load environment variables
if os.path.exists(".env.production"):
    load_dotenv(".env.production")
else:
    load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.database import add_generated_document, analytics, create_case, get_case, init_db, list_cases
from app.graph_engine import LegalGraphEngine
from app.knowledge import load_rules
from app.models import CaseCreate, PathRequest, PdfRequest
from app.pdf_generator import generate_pdf
from app.seed import seed_cases


app = FastAPI(title="PathFinder API", version="1.0.0")

# Parse allowed origins from environment variable
cors_origins_str = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
allowed_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = LegalGraphEngine()


@app.on_event("startup")
def startup() -> None:
    init_db()
    seed_cases(engine)


@app.get("/health")
@app.head("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/rules")
def rules() -> list[dict]:
    return load_rules()


@app.get("/stats")
def stats() -> dict:
    return {"legal_graph": engine.stats(), "analytics": analytics()}


@app.post("/generate-path")
def generate_path(request: PathRequest) -> dict:
    return engine.generate_path(request).model_dump()


@app.post("/cases")
def post_case(request: CaseCreate) -> dict:
    path = engine.generate_path(request).model_dump()
    return create_case(request.person, request.problem, path).model_dump(mode="json")


@app.get("/cases")
def get_cases(search: str | None = None) -> list[dict]:
    return [case.model_dump(mode="json") for case in list_cases(search)]


@app.get("/cases/{case_id}")
def get_case_by_id(case_id: str) -> dict:
    try:
        return get_case(case_id).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found") from None


@app.post("/generate-pdf")
def post_pdf(request: PdfRequest) -> dict:
    try:
        case = get_case(request.case_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Case not found") from None
    if request.document_type not in case.generated_path.get("required_documents", []):
        raise HTTPException(status_code=400, detail="Document is not required for this case")
    pdf_path = generate_pdf(case, request.document_type)
    updated = add_generated_document(case.case_id, request.document_type, pdf_path.name)
    return {
        "document_type": request.document_type,
        "filename": pdf_path.name,
        "download_url": f"/pdfs/{pdf_path.name}",
        "case": updated.model_dump(mode="json"),
    }


@app.get("/pdfs/{filename}")
def download_pdf(filename: str) -> FileResponse:
    from app.pdf_generator import PDF_DIR

    path = PDF_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(path, media_type="application/pdf", filename=filename)


if __name__ == "__main__":
    import uvicorn
    import sys
    from pathlib import Path
    
    backend_path = Path(__file__).resolve().parent
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
        
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host=host, port=port, reload=True)
