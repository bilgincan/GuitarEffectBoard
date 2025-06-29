from models.effects.EffectBase import Effect


class NoneTypeEffect(Effect):
    def __init__(self) -> None:
        super().__init__(volume=0, is_active=False)

    def effect_channel(self) -> None:
        pass

    def activate_effect(self) -> None:
        pass

    def deactivate_effect(self) -> None:
        pass