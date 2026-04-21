from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from processing import run_parallel
import ctypes
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load library
lib_path = os.path.join(os.path.dirname(__file__), "libparallel.so")
lib = ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)

lib.count_matches.argtypes = [
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_int,
    ctypes.c_char_p
]
lib.count_matches.restype = ctypes.c_int


@app.post("/process")
async def count_api(
    file: UploadFile = File(...),
    keyword: str = Form(...)
):
    content = await file.read()

    lines = content.split(b"\n")   # bytes split (correct)

    n = len(lines)
    arr = (ctypes.c_char_p * n)(*lines)

    keyword_bytes = keyword.encode()    

    result = lib.count_matches(arr, n, keyword_bytes)
    return {
        "keyword": keyword,
        "total_matches": result,
        #"sample_output": processed[:10]
    }

@app.post("/process_serial")
async def process_file(
    file: UploadFile = File(...),
    keyword: str = Form(...)   # 🔥 NEW
):
    content = await file.read()
    lines = content.decode("utf-8").split("\n")

    # pass keyword to processing
    processed, count = run_parallel(lines, keyword)

    return {
        "keyword": keyword,
        "total_matches": count,
        #"sample_output": processed[:10]
    }