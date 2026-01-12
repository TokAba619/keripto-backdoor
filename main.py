from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO

from crypto_service import process_and_encrypt, process_and_decrypt

app = FastAPI(title="Secure File Vault API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/encrypt")
async def encrypt(file: UploadFile = File(...),
                  vault_password: str = Form(...),
                  file_password: str = Form(None)):
    """
    Encrypt the uploaded file.
    - vault_password: for AES-GCM vault encryption
    - file_password: optional, for PDF file-level protection
    """
    try:
        data = await file.read()
        enc = process_and_encrypt(
            data=data,
            filename=file.filename,
            vault_password=vault_password,
            file_password=file_password
        )

        out_name = (file.filename or "file") + ".enc"
        return StreamingResponse(
            BytesIO(enc),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{out_name}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@app.post("/decrypt")
async def decrypt(file: UploadFile = File(...), vault_password: str = Form(...)):
    """
    Decrypt the uploaded .enc file using the vault password.
    The file-level password (e.g., PDF password) is not removed.
    """
    try:
        blob = await file.read()
        dec = process_and_decrypt(
            encrypted_data=blob,
            vault_password=vault_password
        )

        in_name = file.filename or "encrypted.enc"
        out_name = in_name[:-4] if in_name.lower().endswith(".enc") else "decrypted_file"

        return StreamingResponse(
            BytesIO(dec),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f'attachment; filename="{out_name}"'}
        )
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Decryption failed. Wrong password or corrupted file."
        )