import json
import logging
from typing import Callable, Any, Awaitable

import aio_pika
import asyncio

import rabbitmq

logger = logging.getLogger(__name__)


# type : async function
HANDLERS = dict()


async def process_message(
    message: aio_pika.abc.AbstractIncomingMessage,
) -> None:
    async with message.process():
        logger.debug("%s %s", message.body)

        body_dict = json.loads(message.body)
        message_types: list[str] = body_dict["messageType"]

        for mt_type in message_types:
            t = __cut_mt_type(mt_type)

            if handler := HANDLERS.get(t):
                await handler(body_dict, message)
            else:
                logger.warning("No handler for %s", t)


def handle(t: str, handler: Callable[[dict, aio_pika.abc.AbstractIncomingMessage], Awaitable[None]]):
    HANDLERS[t] = handler


