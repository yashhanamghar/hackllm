from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
import requests
import os
from app.utils import extract_text_from_file
from app.rag_pipeline import process_document_and_answer_questions

app = FastAPI()
from fastapi.openapi.models import APIKey, APIKeyIn, SecuritySchemeType
from fastapi.openapi.utils import get_openapi
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="authorization", auto_error=False)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI",
        version="0.1.0",
        description="HackRx LLM Query API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# ✅ Replace this with your actual HackRx Bearer token from dashboard
HACKATHON_BEARER = "504635995f102f61f796b6b872fc2c4aab9746b70aed2ccac264c0928c881adc"

# ✅ Request body format matches HackRx: "documents" and "questions"
class RequestBody(BaseModel):
    documents: str
    questions: list
@app.get("/")
def root():
    return {"message": "Welcome to HackRx RAG API"}

@app.post("/hackrx/run")
async def run_rag(request: RequestBody, authorization: str = Header(...)):
    if authorization != f"Bearer {HACKATHON_BEARER}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    file_path = "temp_document.pdf"  # Temporary file to save downloaded PDF

    try:
        # ✅ Download the document from the given URL
        response = requests.get(request.documents)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            f.write(response.content)

        # ✅ Extract text and answer questions
        text = extract_text_from_file(file_path)
        answers = process_document_and_answer_questions(text, request.questions)

        return {"answers": answers}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # ✅ Clean up temp file
        if os.path.exists(file_path):
            os.remove(file_path)

