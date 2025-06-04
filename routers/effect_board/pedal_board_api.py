from fastapi import APIRouter
import uuid

from exception.OutOfBound import OutOfBoundException
from models.effect_board.EffectBoardBase import EffectBoard
from models.effects.EffectBase import Effect
from routers.dto_mother_class import ResponseDto, ResponseStatus
from routers.effect_board.dto.pedal_board_dto import PedalBoardInputDto, PedalBoardOutputDto, \
    EffectInBoardDto
from player import ConcretePedalBoard
from routers.effects.dto.effect_dto import EffectDto, DelayDto
from routers.effects.dto.effect_type_enum import EffectType

router = APIRouter(
    prefix="/effect-board",
    tags=["effect-board"],
    responses={404: {"description": "Not found"}}
)

user_board: ConcretePedalBoard = ConcretePedalBoard()

@router.post("/initialize")
def initialize(pedal_board_dto: PedalBoardInputDto) -> ResponseDto:
    pedal_board = EffectBoard(board_size=pedal_board_dto.board_size)
    new_id = str(uuid.uuid4())
    pedal_board.id = new_id

    user_board.effect_board = pedal_board

    response = prepare_response(pedal_board)
    return response

@router.post("/add-effect")
def add_effect(effect_in_board_dto: EffectInBoardDto) -> ResponseDto:
    concrete_dto: EffectDto = transform_dto_into_concrete_dto(effect_in_board_dto.effect)
    real_effect: Effect = concrete_dto.map(audio_in=user_board.audio_in, audio_out=user_board.audio_out)
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
        return prepare_response(pedal_board=user_board.effect_board, success=False, message=str(ex))

@router.post("/activate-effect")
def activate_effect(effect_in_board_dto: EffectInBoardDto) -> ResponseDto:
    position: int = effect_in_board_dto.position

    try:
        user_board.effect_board.activate_pedal(position)
        return prepare_response(user_board.effect_board)
    except OutOfBoundException as ex:
        return prepare_response(pedal_board=user_board.effect_board, success=False, message=str(ex))

@router.post("/deactivate-effect")
def activate_effect(effect_in_board_dto: EffectInBoardDto) -> ResponseDto:
    position: int = effect_in_board_dto.position

    try:
        user_board.effect_board.deactivate_pedal(position)
        return prepare_response(user_board.effect_board)
    except OutOfBoundException as ex:
        return prepare_response(pedal_board=user_board.effect_board, success=False, message=str(ex))

@router.get("/get")
async def get_effect_board(id: str) -> ResponseDto: # change return type to ResponseDBDto
    pass # get effect board from database

@router.put("/save")
async def save_effect_board(id: str) -> ResponseDto: # change return type to ResponseDBDto
    pass # save the current effect board in to the database, if it does not exist. If it exists, update

@router.delete("/delete")
async def delete_effect_board(id: str) -> ResponseDto:  # change return type to ResponseDBDto
    pass # delete the current effect board from database


def transform_dto_into_concrete_dto(effect_dto: EffectDto) -> EffectDto:
    if effect_dto.effect_type == EffectType.DELAY:
        return DelayDto(volume=effect_dto.volume, is_active=effect_dto.is_active, effect_type=effect_dto.effect_type, delay_rate=effect_dto.delay_rate, frequency=effect_dto.frequency)

def prepare_response(pedal_board: EffectBoard, success: bool= True, message: str="") -> ResponseDto:
    effects_dto = []

    for effect in pedal_board.effects:
        effects_dto.append(EffectDto.reverse_map(effect))

    pedal_board_output: PedalBoardOutputDto = PedalBoardOutputDto(
        board_id=pedal_board.id,
        board_size=pedal_board.board_size,
        effects=effects_dto
    )

    data = pedal_board_output.__dict__

    if success:
        return ResponseDto(
            message=message,
            data=data,
            status=ResponseStatus.SUCCESS
        )
    else:
        return ResponseDto(
            message=message,
            data=data,
            status=ResponseStatus.FAIL
        )



