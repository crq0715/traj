def test_imports():
    import dp_traj_bench
    from dp_traj_bench.core import Schema
    assert hasattr(dp_traj_bench, "__version__")
    # 简单调用占位方法
    import pandas as pd
    df = pd.DataFrame({"traj_id":[1], "t":[pd.Timestamp.utcnow()], "lat":[0.0], "lon":[0.0]})
    Schema.enforce(df)
