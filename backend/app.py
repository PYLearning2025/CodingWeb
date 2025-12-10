from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import account, question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(account.router)
app.include_router(question.router, prefix='/question')

@app.get("/")
def index():
    # TODO: Handle the root route
    return {"message": "Welcome to Coding Web"}