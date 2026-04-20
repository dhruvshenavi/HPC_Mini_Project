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
    try:
        text = content.decode("utf-8")
    except:
        text = content.decode("latin-1")

    lines = text.split("\n")
    n = len(lines)

    array_type = ctypes.c_char_p * n
    arr = array_type()

    i = 0
    for line in lines:
        arr[i] = line.encode()
        i = i + 1

    result = lib.count_matches(arr, n, keyword.encode())

    return {
        "keyword": keyword,
        "total_matches": result
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