from fastapi import APIRouter
import uuid

from exception.OutOfBound import OutOfBoundException
from models.effect_board.EffectBoardBase import EffectBoard
from models.effects.EffectBase import Effect
from repository.effect_board.EffectBoardModel import EffectBoardModel
from repository.effect_board.EffectBoardRepository import EffectBoardRepository
from routers.dto_mother_class import ResponseDto, ResponseStatus
from routers.effect_board.dto.pedal_board_dto import PedalBoardInputDto, PedalBoardOutputDto, \
    EffectInBoardDto, EffectBoardUserDto
from player import ConcretePedalBoard
from routers.effects.dto.effect_dto import EffectDto, DelayDto, ByPassDto
from routers.effects.dto.effect_type_enum import EffectType

router = APIRouter(
    prefix="/effect-board",
    tags=["effect-board"],
    responses={404: {"description": "Not found"}}
)

user_board: ConcretePedalBoard = ConcretePedalBoard()
effect_board_repository: EffectBoardRepository = EffectBoardRepository()

@router.post("/initialize")
def initialize(pedal_board_dto: PedalBoardInputDto) -> ResponseDto:
    pedal_board = EffectBoard(board_size=pedal_board_dto.board_size)
    new_id = str(uuid.uuid4())
    pedal_board.id = new_id
    pedal_board.user_id = str(uuid.uuid4())

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

@router.get("/get-current-board-info")
def get_board_info() -> ResponseDto:
    return prepare_response(user_board.effect_board)

@router.get("/list-effect-boards")
def list_effect_boards() -> ResponseDto:
    pass

@router.get("/get")
async def get_effect_board(id: str) -> ResponseDto: # change return type to ResponseDBDto
    effect_board_model: EffectBoardModel = effect_board_repository.get(id)
    if effect_board_model is None:
        return prepare_response(pedal_board=user_board.effect_board, success=False)
    else:
        return prepare_response(pedal_board=effect_board_model, success=True)

@router.put("/save")
async def save_effect_board(effect_board_user_dto: EffectBoardUserDto) -> ResponseDto: # change return type to ResponseDBDto
    # save the current effect board in to the database, if it does not exist. If it exists, update
    if effect_board_user_dto.id == "":
        effect_board_model: EffectBoardModel = EffectBoardModel.reverse_map(user_board.effect_board)
        result = effect_board_repository.create(effect_board_model)
    else:
        effect_board_model: EffectBoardModel = effect_board_repository.get(effect_board_user_dto.id)

        if effect_board_model is not None:
            result = effect_board_repository.update(effect_board_model)
        else:
            effect_board_model: EffectBoardModel = EffectBoardModel.reverse_map(user_board.effect_board)
            result = effect_board_repository.create(effect_board_model)

    response_dto = ResponseDto(
        status=ResponseStatus.SUCCESS,
        data=result,
        message=""
    )
    return response_dto



@router.delete("/delete")
async def delete_effect_board(id: str) -> ResponseDto:  # change return type to ResponseDBDto
    pass # delete the current effect board from database


def transform_dto_into_concrete_dto(effect_dto: EffectDto) -> None | DelayDto | ByPassDto:
    if effect_dto.effect_type == EffectType.DELAY:
        return DelayDto(volume=effect_dto.volume, is_active=effect_dto.is_active, effect_type=effect_dto.effect_type, delay_rate=effect_dto.delay_rate, frequency=effect_dto.frequency)
    elif effect_dto.effect_type == EffectType.BYPASS:
        return ByPassDto(volume=effect_dto.volume, is_active=effect_dto.is_active, effect_type=effect_dto.effect_type)

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



