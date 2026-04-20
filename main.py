from fastapi import FastAPI
import ctypes
import os

lib_path = os.path.join(os.path.dirname(__file__), "libparallel.so")

print("Library path:", lib_path)   # debug log


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# load shared library
lib_path = os.path.join(os.path.dirname(__file__), "libparallel.so")
lib = ctypes.CDLL(lib_path)

# define function types
lib.count_matches.argtypes = [
    ctypes.POINTER(ctypes.c_char_p),
    ctypes.c_int,
    ctypes.c_char_p
]

lib.count_matches.restype = ctypes.c_int


@app.post("/count")
def count_api(data: dict):

    lines = data["lines"]
    keyword = data["keyword"]

    n = len(lines)

    # create array
    array_type = ctypes.c_char_p * n
    arr = array_type()

    # fill array (no shorthand)
    i = 0
    for line in lines:
        arr[i] = line.encode()
        i = i + 1

    # call C++ function
    result = lib.count_matches(arr, n, keyword.encode())

    return {"count": result}