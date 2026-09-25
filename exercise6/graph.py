import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt 

dat_60 = np.genfromtxt("gamma60k.txt")
dat_30 = np.genfromtxt("gamma30k.txt")
dat_15 = np.genfromtxt("gamma15k.txt")
dat_7 = np.genfromtxt("gamma7-5k.txt")
dat_3 = np.genfromtxt("gamma3-75k.txt")


colors = ["red", "orange", "purple", "magenta", "blue"]

count = 0
sigmas = list()
gammas = np.array([60000, 30000, 15000, 7500, 3750])

def asd(data, name):
    global count
    counter = colors[count]
    mu, sigma = stats.norm.fit(data)
    x = np.linspace(min(data), max(data), 100)
    x = np.linspace(-14., 15., 100)

    sigmas.append(sigma**2)

    pdf = stats.norm.pdf(x, loc=mu, scale=sigma)

    plt.hist(data, alpha=0.12, histtype="stepfilled", density=True, label = f"{name} || {sigma:.2f}", color = counter, edgecolor=counter)
    plt.hist(data, alpha=0.3, histtype="step", density=True, color = counter, edgecolor=counter)
    plt.plot(x, pdf, "r-", lw=2, color = counter)
    print(mu, sigma)

    count+= 1

asd(dat_60, "60K")
asd(dat_30, "30K")
asd(dat_15, "15K")
asd(dat_7, "7.5K")
asd(dat_3, "3.75K")


plt.xlabel("Value")
plt.ylabel("Density")
plt.legend(title = r"$\gamma_{resorte}$ || $\sigma_x$")
plt.show()



plt.plot(1./gammas, sigmas)
plt.show()
