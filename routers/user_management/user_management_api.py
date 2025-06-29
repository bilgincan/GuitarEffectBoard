from fastapi import APIRouter

router = APIRouter(
    prefix="/user-management",
    tags=["user_management"],
    responses={404: {"description": "Not found"}}
)

@router.post("/create-user")
def create_user():
    pass

@router.get("/list-users")
def list_users():
    pass

@router.get("/get-user")
def get_user():
    pass

@router.delete("/delete-user")
def delete_user():
    pass

@router.put("/update-user")
def update_user():
    pass

