from fastapi import FastAPI
from router.router import router
from db import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router=router)
