import uvicorn
from fastapi import FastAPI

from routers.effect_board import pedal_board_api

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})
app.include_router(pedal_board_api.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)