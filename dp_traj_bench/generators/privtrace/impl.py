import numpy as np, pandas as pd

class MarkovModel:
    def __init__(self, n_states:int): self.n_states=n_states; self.P=None
    def fit(self, seqs):
        n=self.n_states; C=np.ones((n,n),float)
        for s in seqs:
            for a,b in zip(s[:-1], s[1:]): C[a,b]+=1
        self.P = C / C.sum(axis=1, keepdims=True)
    def sample(self, L, rng):
        x=int(rng.integers(0,self.n_states)); seq=[x]
        for _ in range(L-1):
            p=self.P[seq[-1]]; x=int(rng.choice(self.n_states, p=p)); seq.append(x)
        return seq

def fit_markov_model(df, params):
    n=int(df["loc_id"].max())+1
    m=MarkovModel(n)
    seqs=[g["loc_id"].tolist() for _,g in df.groupby("user_id")]
    m.fit(seqs)
    return m

def synthesize_with_privacy(model, epsilon, seed, params):
    rng=np.random.default_rng(seed)
    P=model.P.copy()
    if np.isfinite(epsilon):
        noise=rng.laplace(0.0, scale=max(1e-6,1.0/(epsilon+1e-12)), size=P.shape)
        P=np.clip(P+noise,1e-9,None); P/=P.sum(axis=1,keepdims=True)
    rows=[]; uid0=100000
    for i in range(50):
        L=20; seq=[int(rng.integers(0,model.n_states))]
        for _ in range(L-1):
            p=P[seq[-1]]; seq.append(int(rng.choice(model.n_states, p=p)))
        t0=1700000000+i*1000
        for k,loc in enumerate(seq): rows.append({"user_id":uid0+i,"timestamp":t0+k,"loc_id":int(loc)})
    return pd.DataFrame(rows)
