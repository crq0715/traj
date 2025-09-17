from .density_query import run_density_query
TASKS = {"density_query": run_density_query}

def run_utility_suite(real, synth, tasks, params_dict):
    out={}
    for t in tasks:
        out[t]=TASKS[t](real, synth, params_dict.get(t, {}))
    return out
