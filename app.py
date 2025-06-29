import uvicorn
from fastapi import FastAPI

from routers.effect_board import pedal_board_api
from routers.auth import auth_api
from routers.user_management import user_management_api

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": True})
app.include_router(pedal_board_api.router)
app.include_router(auth_api.router)
app.include_router(user_management_api.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)