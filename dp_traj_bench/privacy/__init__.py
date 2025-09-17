from .attacks import run_mia
ATTACKS = {"mia": run_mia}

def run_privacy_suite(real, synth, attacks, params_dict):
    out={}
    for a in attacks:
        out[a]=ATTACKS[a](real, synth, params_dict.get(a, {}))
    return out
