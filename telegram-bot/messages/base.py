from aiogram.types import Message
from pydantic import BaseModel


def bot():
    from ..bot import static
    return static


class MessageBase(BaseModel):
    botId: int
    userId: int
    chatId: int
    key: str

    @classmethod
    async def from_message(cls, msg: Message, key: str):
        return cls(
            botId=bot().id,
            userId=msg.from_user.id,
            chatId=msg.chat.id,
            key=cls.__name__
        )
