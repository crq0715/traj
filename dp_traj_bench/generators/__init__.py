from ..core.registry import GEN_REGISTRY
from .privtrace.adapter import PrivTraceGenerator

GEN_REGISTRY.register("privtrace")(PrivTraceGenerator)

def build_generator(name: str, params: dict):
    Gen = GEN_REGISTRY.get(name)
    return Gen(params)
