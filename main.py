from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend import post_url


app = FastAPI()

app.include_router(post_url.router)


app.add_middleware(
            CORSMiddleware,
            allow_origins = ["http://localhost:3000"],
            allow_credentials = True,
            allow_methods=["*"],
            allow_headers=["*"]
            )




