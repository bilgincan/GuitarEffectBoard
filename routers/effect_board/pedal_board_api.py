from fastapi import APIRouter

from exception.OutOfBound import OutOfBoundException
from models.effect_board.EffectBoardBase import EffectBoard
from models.effects.EffectBase import Effect
from routers.dto_mother_class import ResponseDto, ResponseStatus
from routers.effect_board.dto.pedal_board_dto import PedalBoardInputDto, PedalBoardOutputDto, \
    EffectInBoardDto
from player import ConcretePedalBoard

router = APIRouter(
    prefix="/effect-board",
    tags=["effect-board"],
    responses={404: {"description": "Not found"}}
)

user_board: ConcretePedalBoard = ConcretePedalBoard()

@router.post("/initialize")
def initialize(pedal_board_dto: PedalBoardInputDto) -> ResponseDto:
    pedal_board = EffectBoard(board_size=pedal_board_dto.board_size)
    user_board.effect_board = pedal_board

    return prepare_response(pedal_board)

@router.post("/add-effect")
def add_effect(effect_in_board_dto: EffectInBoardDto) -> ResponseDto:
    real_effect: Effect = effect_in_board_dto.effect.map()
    position: int = effect_in_board_dto.position

    user_board.effect_board.add_effect(position=position, effect=real_effect)

    return prepare_response(user_board.effect_board)

@router.post("/remove-effect")
def remove_effect(effect_in_board_dto: EffectInBoardDto) -> ResponseDto:
    position: int = effect_in_board_dto.position

    try:
        user_board.effect_board.remove_effect(position=position)
        return prepare_response(user_board.effect_board)
    except OutOfBoundException as ex:
        return prepare_response(pedal_board=user_board.effect_board, success=False, message=ex.__str__())

@router.get("/get")
async def get_effect_board(id: str) -> ResponseDto: # change return type to ResponseDBDto
    pass # get effect board from database

@router.put("/save")
async def save_effect_board(id: str) -> ResponseDto: # change return type to ResponseDBDto
    pass # save the current effect board in to the database, if it does not exist. If it exists, update

@router.delete("/delete")
async def delete_effect_board(id: str) -> ResponseDto:  # change return type to ResponseDBDto
    pass # delete the current effect board from database


def prepare_response(pedal_board: EffectBoard, success: bool= True, message: str="") -> ResponseDto:
    response = ResponseDto()
    pedal_board_output = PedalBoardOutputDto()

    pedal_board_output.effects = pedal_board.effects
    pedal_board_output.board_size = pedal_board.board_size

    response.message = message
    response.data = pedal_board_output

    if success:
        response.status = ResponseStatus.SUCCESS
    else:
        response.status = ResponseStatus.FAIL


    return response



