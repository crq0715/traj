import random, numpy as np, pandas as pd, pyproj
from datetime import datetime, timezone
import shapely.geometry as geom

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)

def example_df(n=5):
    # 统一 schema 的最小样例
    return pd.DataFrame({
        "traj_id": np.arange(n),
        "t": [datetime.now(timezone.utc) for _ in range(n)],
        "lat": 35 + np.random.rand(n) * 0.01,
        "lon": 135 + np.random.rand(n) * 0.01,
    })

def quick_projection(lat, lon):
    # WGS84 -> UTM（京都附近示例：zone 53N，真实项目请根据数据自动判断）
    proj = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:32653", always_xy=True)
    return proj.transform(lon, lat)

set_seed(0)
df = example_df()
x, y = quick_projection(df.loc[0, "lat"], df.loc[0, "lon"])
print("smoke ok; sample UTM:", round(x,2), round(y,2))
print("df columns:", list(df.columns))
print("shapely point ok:", geom.Point(df.loc[0,"lon"], df.loc[0,"lat"]).wkt)
