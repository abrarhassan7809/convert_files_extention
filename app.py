from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from curd_functions import ConvertFileExtension
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")
convert_methods = ConvertFileExtension("converted_files")


upload_dir = "uploaded_files"
os.makedirs(upload_dir, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...), select_format: str = Form(...)):

    upload_path = os.path.join(upload_dir, file.filename)
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Convert the file
    if select_format == "docx":
        convert_methods.convert_pdf_to_docx(upload_path)
    elif select_format == "pdf":
        convert_methods.convert_docx_to_pdf(upload_path)
    else:
        return {"error": "Unsupported conversion format"}

    return templates.TemplateResponse("upload.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, workers=1)
