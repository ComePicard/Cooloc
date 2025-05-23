import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # Path to your FastAPI app instance
        host="0.0.0.0",  # Host to bind the server to
        port=8000,         # Port to bind the server to
        reload=True        # Enable auto-reload during development
    )