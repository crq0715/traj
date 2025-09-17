import os, json
from ..core.logging import get_logger
logger = get_logger()

def run_experiment(cfg):
    os.makedirs(cfg["gen"]["output_dir"], exist_ok=True)

    # 延用你已有的 datasets 模块
    from ..datasets import load_dataset
    from ..generators import build_generator
    from ..utility import run_utility_suite
    from ..privacy import run_privacy_suite

    dataset = load_dataset(cfg["data"])
    results = {"meta": {"data": cfg["data"]["name"]}, "runs": []}

    for eps in cfg["gen"]["epsilon_list"]:
        logger.info(f"RUN method={cfg['gen']['method']} eps={eps}")
        gen = build_generator(cfg["gen"]["method"], cfg["gen"].get("params", {}))
        synth = gen.generate(dataset, epsilon=eps, seed=cfg["gen"]["seed"])

        util_res = run_utility_suite(dataset, synth, cfg["eval"]["utility_tasks"], cfg["eval"].get("utility_params", {}))
        priv_res = run_privacy_suite(dataset, synth, cfg["eval"]["privacy_attacks"], cfg["eval"].get("privacy_params", {}))

        results["runs"].append({"epsilon": eps, "utility": util_res, "privacy": priv_res})

    out_path = os.path.join(cfg["gen"]["output_dir"], f"{cfg['data']['name']}_{cfg['gen']['method']}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    logger.info(f"Saved => {out_path}")
    return results
