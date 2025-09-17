import csv
import os

def dat_to_csv(dat_path, csv_path, start_ts=1700000000, step=60):
    rows = []
    with open(dat_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    while i < len(lines):
        if lines[i].startswith("#"):
            # 获取 user_id
            try:
                user_id = int(lines[i][1:-1])  # "#0:" -> 0
            except ValueError:
                user_id = lines[i][1:-1]
            # 下一行是轨迹点
            if i+1 < len(lines):
                pts_line = lines[i+1]
                pts_line = pts_line.split(":",1)[-1]  # 去掉 ">0:"
                pairs = [p for p in pts_line.split(";") if p]
                ts = start_ts
                for p in pairs:
                    lon, lat = p.split(",")
                    rows.append([user_id, ts, float(lon), float(lat)])
                    ts += step
            i += 2
        else:
            i += 1

    # 输出 CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["user_id","timestamp","lon","lat"])
        writer.writerows(rows)

    print(f"转换完成: {csv_path}，共 {len(rows)} 行")

if __name__ == "__main__":
    dat_path = os.path.join("data","raw","syn15.dat")
    csv_path = os.path.join("data","raw","syn15.csv")
    dat_to_csv(dat_path, csv_path)
