from fastapi import FastAPI
from settings import host, port
from api.urls import router
import uvicorn

app = FastAPI()
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
