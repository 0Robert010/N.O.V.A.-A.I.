import asyncio
from typing import Set

_active_websockets: Set[object] = set()


def register(ws):
    _active_websockets.add(ws)


def unregister(ws):
    _active_websockets.discard(ws)


async def broadcast(message: str) -> None:
    if not _active_websockets:
        return
    coros = []
    for ws in list(_active_websockets):
        try:
            coros.append(ws.send_text(message))
        except Exception:
            try:
                _active_websockets.discard(ws)
            except Exception:
                pass
    if coros:
        await asyncio.gather(*coros, return_exceptions=True)
