<<<<<<< HEAD
from io import BytesIO
from pypdf import PdfReader, PdfWriter


def is_pdf(filename: str) -> bool:
    return filename.lower().endswith(".pdf")


def lock_pdf(data: bytes, password: str) -> bytes:
    reader = PdfReader(BytesIO(data))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # ✅ Correct encryption usage
    writer.encrypt(
        user_password=password,
        owner_password=None,
        use_128bit=True
    )

    output = BytesIO()
    writer.write(output)
    return output.getvalue()
=======
from io import BytesIO
from pypdf import PdfReader, PdfWriter


def is_pdf(filename: str) -> bool:
    return filename.lower().endswith(".pdf")


def lock_pdf(data: bytes, password: str) -> bytes:
    reader = PdfReader(BytesIO(data))
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # ✅ Correct encryption usage
    writer.encrypt(
        user_password=password,
        owner_password=None,
        use_128bit=True
    )

    output = BytesIO()
    writer.write(output)
    return output.getvalue()
>>>>>>> b0b3d9ab2bc4e15400b7ff27417f58933d8d9200
