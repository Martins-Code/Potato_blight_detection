from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get('/ping')
async def ping():
    return {"message": "Hello, I'm aLive"}  


if __name__ == '__main__':
    uvicorn.run(app=app, host='localhost', port=8080)
