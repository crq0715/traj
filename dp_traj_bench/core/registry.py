from dataclasses import dataclass
from typing import Dict

@dataclass
class Registry:
    _items: Dict[str, object] = None
    def __post_init__(self): self._items = {} if self._items is None else self._items
    def register(self, name: str):
        def deco(obj): self._items[name.lower()] = obj; return obj
        return deco
    def get(self, name: str):
        key = name.lower()
        if key not in self._items: raise KeyError(f"Not found: {name}")
        return self._items[key]

GEN_REGISTRY = Registry()
