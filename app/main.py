from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

from fastapi import FastAPI
import uvicorn
from app.routes import router


app = FastAPI(
    title="Summary API",
    description="An API to generate summaries from text inputs.",
    version="0.1.0",
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
