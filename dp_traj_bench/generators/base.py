import pandas as pd
class BaseGenerator:
    def __init__(self, params=None): self.params = params or {}
    def generate(self, dataset: pd.DataFrame, epsilon: float, seed: int = 123):
        raise NotImplementedError
