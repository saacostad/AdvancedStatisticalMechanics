import numpy as np

# ---------------
#   CLASES
# ---------------

class SpinSystem:
    
    def __init__(self, L = 8, def_state = -1, J = 1.):
        self.s = np.ones([L, L]) * def_state
        self.E = -2*L*L*J
        self.M = -L*L

        self.L = L 
        self.L2 = L**2
        self.J = J

    def MetropolisStep(self, beta, rng):
        i = rng.integers(0, self.L)
        j = rng.integers(0, self.L)
        
        J, L, s = self.J, self.L, self.s

        dE=2.*J*s[i, j]*(s[i+1][j]+s[i-1][j]+s[i][j+1]+s[i][j-1]);

        if dE <= 0 or rng.random() < np.exp(-beta * dE):
            s[i, j] *= -1.
            self.E += dE
            self.M += 2*s[i, j]

        print(dE)


# ----------------------
#   MAIN EXECUTION
# ----------------------
random_engine = np.random.default_rng(seed = 67)

T = 1.0
kB = 1.0
beta = 1.0 / (kB * T)

L = 8

system = SpinSystem()

teq=600*np.power(L/8.0,2.4); 
tcorr=50*np.power(L/8.0,2.4);
Nmuestras=10000;

