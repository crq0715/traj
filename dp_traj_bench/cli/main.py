import argparse
from ..core.runner import run_experiment

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--raw", default="./data/raw/sample_city.csv")
    p.add_argument("--eps", default="0.1,1,10,inf")
    p.add_argument("--out", default="./outputs")
    args=p.parse_args()

    eps=[float(x) if x!="inf" else float("inf") for x in args.eps.split(",")]
    cfg={
        "data": {"name":"sample_city","raw_path":args.raw,"discretize":{"grid_size":200}},
        "gen":  {"method":"privtrace","epsilon_list":eps,"seed":123,"output_dir":args.out,"params":{}},
        "eval": {"utility_tasks":["density_query"],"privacy_attacks":["mia"]}
    }
    run_experiment(cfg)

if __name__=="__main__":
    main()
