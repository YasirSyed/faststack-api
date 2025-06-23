from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn

from app.core.config import settings
from app.api.v1 import auth, users, questions, answers, comments, tags

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="A Stack Overflow clone API built with FastAPI",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Set up trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"]
)

# Include API routes
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])
app.include_router(questions.router, prefix=settings.API_V1_STR, tags=["questions"])
app.include_router(answers.router, prefix=settings.API_V1_STR, tags=["answers"])
app.include_router(comments.router, prefix=settings.API_V1_STR, tags=["comments"])
app.include_router(tags.router, prefix=settings.API_V1_STR, tags=["tags"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FastStack API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    ) 