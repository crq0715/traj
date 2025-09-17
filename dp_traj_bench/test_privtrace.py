import os
import pandas as pd

# 导入你的生成器
from dp_traj_bench.generators.privtrace.adapter import PrivTraceGenerator

if __name__ == "__main__":
    # 1. 读取 CSV 文件
    csv_path = os.path.join("data", "raw", "syn15.csv")
    df = pd.read_csv(csv_path)
    print("原始数据：")
    print(df.head())

    # 2. 初始化生成器
    gen = PrivTraceGenerator(params={})

    # 3. 运行生成（这里 epsilon=1.0，seed=123）
    synth = gen.generate(df, epsilon=1.0, seed=123)

    # 4. 打印结果
    print("\n合成数据：")
    print(synth.head())

    # 5. 保存合成数据到文件，方便检查
    out_csv = os.path.join("outputs", "syn15_synth.csv")
    os.makedirs("outputs", exist_ok=True)
    synth.to_csv(out_csv, index=False)
    print(f"\n合成数据已保存到 {out_csv}")
