from fastapi import APIRouter

router = APIRouter(
    prefix="/effects/delay",
    tags=["effect", "delay"],
    responses={404: {"description": "Not found"}},
)

@router.get("/test")
async def test_method():
    return "Test delay"

@router.get("/get")
async def get_delay_pedal(delay_pedal_dto):
    pass

@router.put("/create")
async def create_new(delay_pedal_dto):
    pass

@router.post('/update')
async def configure_existing_pedal(delay_pedal_dto):
    pass

@router.delete('/delete')
async def delete_pedal(delay_pedal_dto):
    pass