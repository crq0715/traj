# dp_traj_bench/generators/privtrace/adapter.py
import os, sys, pandas as pd, numpy as np
from ..base import BaseGenerator

# 将 third_party/PrivTrace 加入路径
TP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../third_party/PrivTrace"))
if TP_DIR not in sys.path:
    sys.path.insert(0, TP_DIR)

from dp_traj_bench.third_party.PrivTrace.api import run_with_xy_trajs  

class PrivTraceGenerator(BaseGenerator):
    def generate(self, dataset: pd.DataFrame, epsilon: float, seed: int = 123) -> pd.DataFrame:
        # 1) 检查输入：PrivTrace 需要真实坐标数据（x,y），我们用 lon/lat 当作 x/y 即可
        if not {"user_id","timestamp","lon","lat"}.issubset(dataset.columns):
            raise ValueError("PrivTrace 需要列：user_id, timestamp, lon, lat。请传入原始坐标数据。")

        # 2) 组装 (x,y) 轨迹（按用户聚合，保序）
        trajs_xy = []
        for _, g in dataset.sort_values(["user_id","timestamp"]).groupby("user_id"):
            xs = g["lon"].to_numpy().astype(float)
            ys = g["lat"].to_numpy().astype(float)
            trajs_xy.append(list(zip(xs, ys)))

        # 3) 调用 PrivTrace（dataset_name 取个临时名）
        dataset_name = self.params.get("dataset_name", "bench_temp")
        synth_trajs = run_with_xy_trajs(trajs_xy, dataset_name=dataset_name, epsilon=float(epsilon))

        # 4) 回填为 DataFrame：生成合成 user_id/timestamp/lon/lat
        rows = []
        uid0 = 10_000
        rng = np.random.default_rng(seed)
        for i, traj in enumerate(synth_trajs):
            # traj: [(x,y,t), ...]，如果没有 t，这里生成 1s 递增
            t0 = int(rng.integers(1_700_000_000, 1_800_000_000))
            for k, p in enumerate(traj):
                x, y = float(p[0]), float(p[1])
                # p 可能是 (x,y,t) 或 (x,y)；做个兜底
                ts = int(p[2]) if len(p) >= 3 else (t0 + k)
                rows.append({"user_id": uid0 + i, "timestamp": ts, "lon": x, "lat": y})
        return pd.DataFrame(rows).sort_values(["user_id","timestamp"]).reset_index(drop=True)
