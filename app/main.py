from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.routes import router
from app.shared.databases.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    print("Database initialized")
    yield
    # Shutdown
    print("Shutting down gracefully")


app = FastAPI(
    title="Summary API",
    description="An API to generate summaries from text inputs.",
    version="0.1.0",
    lifespan=lifespan
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
