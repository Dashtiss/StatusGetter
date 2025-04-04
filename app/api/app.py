from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import router
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import Base, db_engine, get_db

# Database configuration
DATABASE_URL = "sqlite:///./test.db"  # Replace with PostgreSQL URL in production
db_engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)

# Initialize database schema
Base.metadata.create_all(bind=db_engine)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router from endpoints
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)