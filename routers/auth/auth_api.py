from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)

@router.post("/login")
def login():
    pass

@router.get("/logout")
def logout():
    pass