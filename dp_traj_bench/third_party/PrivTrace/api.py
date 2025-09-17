# third_party/PrivTrace/api.py
import os, sys, subprocess, time
from typing import List, Tuple

PRIVTRACE_ROOT = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(PRIVTRACE_ROOT, "datasets")
DEFAULT_OUT = os.path.join(PRIVTRACE_ROOT, "generated_tras.txt")

def _write_dat_file(trajs: List[List[Tuple[float, float]]], out_path: str):
    """
    将轨迹列表写PrivTrace 所需 .dat 格式
    trajs: [ [(x,y),(x,y),...],  [(x,y),...], ... ]
    """
    with open(out_path, "w", encoding="utf-8") as f:
        for i, traj in enumerate(trajs):
            f.write(f"#{i}:\n")
            f.write(">0:")
            for (x, y) in traj:
                f.write(f"{x},{y};")
            f.write("\n")

def _parse_generated_file(path: str):
    """
    读取默认输出 generated_tras.txt，解析为 [[(x,y,t),...], ...]
    如果没有时间戳，生成一个简单的递增 t
    """
    trajs = []
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        # 期望成对：第1"#idx:"，第2">0:x,y;..."
        if not lines[i].startswith("#"):
            i += 1
            continue
        idx_line = lines[i]; pts_line = lines[i+1] if i+1 < len(lines) else ""
        i += 2

        # 解析
        pts_line = pts_line.split(":")[-1]  # 去掉前缀 >0:
        pairs = [p for p in pts_line.split(";") if p]
        traj = []
        t = 0
        for p in pairs:
            x_str, y_str = p.split(",")
            x = float(x_str); y = float(y_str)
            traj.append((x, y, t))
            t += 1
        trajs.append(traj)
    return trajs

def run_with_xy_trajs(trajs_xy: List[List[Tuple[float, float]]], dataset_name: str, epsilon: float | None = None, timeout_sec: int = 3600):
    """
    (x,y) 轨迹直接调用 PrivTrace，dataset_name 用作 .dat 文件名
    注意：epsilon 目前只能通过修改 config/parameter_setter.py folder_and_file_names.py 的方式传入；
    如果下游需要精确控ε，可在项目内添加参数支持后再扩展这里
    """
    os.makedirs(DATASETS_DIR, exist_ok=True)
    in_dat = os.path.join(DATASETS_DIR, f"{dataset_name}.dat")

    # 1) 写入 .dat
    _write_dat_file(trajs_xy, in_dat)

    # 2) 调用 main.py（cwd 切到仓库根，传入 --dataset_file_name
    cmd = [sys.executable, "main.py", f"--dataset_file_name={os.path.basename(in_dat)}"]
    # 注：如果 PrivTrace 支持更多 CLI 参数，可以在这里追加
    proc = subprocess.run(cmd, cwd=PRIVTRACE_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=timeout_sec)

    if proc.returncode != 0:
        raise RuntimeError(f"PrivTrace failed.\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}")

    # 3) 解析默认输出
    if not os.path.exists(DEFAULT_OUT):
        # 某些版本可能把输出放 datasets 下；如需定制，请调整 folder_and_file_names.py
        alt = os.path.join(DATASETS_DIR, "generated_tras.txt")
        if os.path.exists(alt):
            out_path = alt
        else:
            raise FileNotFoundError(f"Cannot find generated file: {DEFAULT_OUT}")
    else:
        out_path = DEFAULT_OUT

    return _parse_generated_file(out_path)
