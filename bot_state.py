class BotState:
    _enabled = True

    @classmethod
    def set_bot_enabled(cls, enabled: bool):
        cls._enabled = enabled

    @classmethod
    def get_bot_enabled(cls) -> bool:
        return cls._enabled