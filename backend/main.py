from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Argo CD Demo Backend API")

# Enable CORS so frontend can call API directly or through proxy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "service": "backend", "version": "v1"}

@app.get("/api/hello")
def get_hello():
    return {
        "message": "Hello from AWS ECR Backend v1.0.18",
        "version": "v1.0.18",
        "timestamp": time.time(),
        "status": "success"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
