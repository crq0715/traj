from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
import pandas as pd

@dataclass
class TrajectoryRecord:
    """统一 Schema 的单条记录数据结构（后续可扩展）。"""
    traj_id: int
    t: pd.Timestamp
    lat: float
    lon: float
    user_id: Optional[int] = None
    speed: Optional[float] = None
    edge_id: Optional[int] = None

class Schema:
    """统一 Schema 校验/修正的占位实现（阶段 2 会完善）。"""
    REQUIRED: List[str] = ["traj_id", "t", "lat", "lon"]
    OPTIONAL: List[str] = ["user_id", "speed", "edge_id"]

    @classmethod
    def validate(cls, df: pd.DataFrame) -> None:
        """检查必要列是否存在。后续将加入类型/时区/范围检查。"""
        missing = [c for c in cls.REQUIRED if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    @classmethod
    def enforce(cls, df: pd.DataFrame) -> pd.DataFrame:
        """
        轻量占位：当前只做列存在性检查并返回原 df。
        阶段 2 将支持：别名修正、类型转换、时间戳标准化、排序等。
        """
        cls.validate(df)
        return df
