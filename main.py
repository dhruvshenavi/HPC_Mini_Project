from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from processing import run_parallel

app = FastAPI()

# ✅ Enable CORS (important for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Root endpoint
@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}

# 🔹 Updated API with keyword input
@app.post("/process")
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
        "sample_output": processed[:10]
    }