import numpy as np

def run_density_query(real_df, synth_df, params):
    rng=np.random.default_rng(123)
    vc=real_df["loc_id"].value_counts()
    locs=vc.index.tolist()
    if not locs: return 0.0
    sample=rng.choice(locs, size=min(10,len(locs)), replace=False)
    errs=[]
    for loc in sample:
        ar=int((real_df["loc_id"]==loc).sum())
        as_=int((synth_df["loc_id"]==loc).sum())
        errs.append(abs(ar-as_)/max(abs(ar),1e-9))
    return float(sum(errs)/len(errs))
