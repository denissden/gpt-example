import logging
from asyncio import Future
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage, StorageKey, StateType

from masstransit.providers import RpcProvider
from masstransit import MtCache, MassTransit

_STATE_KEY = "_state"
_DATA_KEY = "_data"


logger = logging.getLogger(__name__)


@dataclass()
class MtStorage(BaseStorage):
    masstransit: MassTransit
    mt_save_type: str
    mt_request_type: str
    mt_response_type: str

    _rpc: RpcProvider = None
    _state_cache: MtCache = field(default_factory=MtCache)
    _data_cache: MtCache = field(default_factory=MtCache)

    def __post_init__(self):
        self._rpc = RpcProvider(
            mt_request_type=self.mt_request_type,
            mt_response_type=self.mt_response_type,
            mt=self.masstransit
        )

    async def set_state(self, bot: Bot, key: StorageKey, state: StateType = None) -> None:
        logger.info("set_state")
        value = str(state.state)
        await self.masstransit.publisher.publish({
            "botId": key.bot_id,
            "userId": key.chat_id,
            "chatId": key.chat_id,
            "key": _STATE_KEY,
            "jsonValue": {
                "s": value
            }
        }, mt_type=self.mt_save_type)
        self._state_cache.set(key, value)

    async def get_state(self, bot: Bot, key: StorageKey) -> Optional[str]:
        if hit := self._state_cache.get(key):
            return hit

        logger.info("req_state")

        msg = await self.rpc(key, _STATE_KEY) or {}
        res = msg.get("jsonValue", {}).get("s")
        self._state_cache.set(key, res)
        return res

    async def set_data(self, bot: Bot, key: StorageKey, data: Dict[str, Any]) -> None:
        logger.info("set_data")
        await self.masstransit.publisher.publish({
            "botId": key.bot_id,
            "userId": key.chat_id,
            "chatId": key.chat_id,
            "key": _DATA_KEY,
            "jsonValue": data
        }, mt_type=self.mt_save_type)
        self._data_cache.set(key, data)

    async def get_data(self, bot: Bot, key: StorageKey) -> Dict[str, Any]:
        if hit := self._data_cache.get(key):
            return hit

        logger.info("req_data")

        msg = await self.rpc(key, _DATA_KEY)
        res = msg and msg.get("jsonValue") or {}
        self._data_cache.set(key, res)
        return res

    async def rpc(self, key: StorageKey, state_key: str):
        response = await self._rpc.execute({
            "botId": key.bot_id,
            "userId": key.chat_id,
            "chatId": key.chat_id,
            "key": state_key
        })

        return response[0]

    async def close(self) -> None:
        pass