from exception.IllegalArgument import IllegalArgumentException
from repository.database.DatabaseConnector import DatabaseConnector
from repository.effect_board.EffectBoardModel import EffectBoardModel


class EffectBoardRepository(DatabaseConnector):
    def __init__(self):
        super().__init__("effect_board")

    def get_boards_by_user_id(self, user_id: str) -> EffectBoardModel | None:
        database = self.db_connection.database
        query = {"user_id": user_id}

        db_output = database.find(query)

        if db_output:
            return EffectBoardModel(_id=db_output[0]["id"], user_id=db_output[0]["user_id"], board_size=db_output[0]["board_size"], effects=db_output[0]["effects"])
        else:
            return None

    def create(self, effect_board: EffectBoardModel) -> dict:
        if effect_board.user_id is None:
            raise IllegalArgumentException()

        effect_board_dict = effect_board.__dict__
        result = super().create(effect_board_dict)
        result_dict = {
            "id": str(result.inserted_id)
        }

        return result_dict

    def update(self, effect_board: EffectBoardModel) -> dict:
        if effect_board.id is None and effect_board.user_id is None:
            raise IllegalArgumentException()

        effect_board_dict = effect_board.__dict__
        return super().update(effect_board_dict).raw_result.__dict__




