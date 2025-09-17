import pandas as pd, numpy as np

def _grid_discretize(df, grid_size=200):
    lon,lat=df["lon"].to_numpy(),df["lat"].to_numpy()
    lx=(lon-lon.min())/max(1e-9,(lon.max()-lon.min())); ly=(lat-lat.min())/max(1e-9,(lat.max()-lat.min()))
    xi=np.floor(lx*(grid_size-1)).astype(int); yi=np.floor(ly*(grid_size-1)).astype(int)
    out=df.copy(); out["loc_id"]=xi*grid_size+yi
    return out[["user_id","timestamp","loc_id"]]

def load_dataset(cfg_data: dict):
    df=pd.read_csv(cfg_data["raw_path"])
    df=df.sort_values(["user_id","timestamp"]).reset_index(drop=True)
    return _grid_discretize(df, grid_size=cfg_data.get("discretize",{}).get("grid_size",200))
