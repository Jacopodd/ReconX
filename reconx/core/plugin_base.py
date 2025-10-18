from typing import List, Dict, Any, Protocol

class Plugin(Protocol):
    name: str
    version: str
    inputs_supported: set

    async def run(self, target: str, ctx) -> List[Dict[str, Any]]:
        ...
