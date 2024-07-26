import uuid
from spire.doc import *
from spire.doc.common import *
from pdf2docx import converter


class ConvertFileExtension:
    def __init__(self, save_dir_path):
        self.save_dir_path = os.path.abspath(save_dir_path)
        print(f"Save directory path: {self.save_dir_path}")

        if not os.path.exists(self.save_dir_path):
            os.makedirs(self.save_dir_path)

    def convert_docx_to_pdf(self, file_path):
        unique_id = uuid.uuid4()
        document = Document()
        document.LoadFromFile(file_path)

        parameters = ToPdfParameterList()
        parameters.IsEmbeddedAllFonts = True

        # image quality is 40%
        # document.JPEGQuality = 40

        output_file = os.path.join(self.save_dir_path, f"{unique_id}_file.pdf")
        document.SaveToFile(output_file, FileFormat.PDF)
        document.Close()
        print(f"Converted DOCX to PDF: {output_file}")

    def convert_pdf_to_docx(self, pdf_file_path):
        unique_id = uuid.uuid4()
        output_file = os.path.join(self.save_dir_path, f"{unique_id}_file.docx")
        cv = converter.Converter(pdf_file_path)
        cv.convert(output_file, start=0, end=None)
        cv.close()
        print(f"Converted PDF to DOCX: {output_file}")
