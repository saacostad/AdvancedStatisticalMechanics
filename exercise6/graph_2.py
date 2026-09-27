import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt 

dat_30 = np.genfromtxt("gamma30k.txt")
dat_30_P = np.genfromtxt("gamma30k_Px.txt")


colors = ["red", "orange", "purple", "magenta", "blue"]


x = np.linspace(-14., 15., 100)

b = 0.039275514000455806
gamma = 4. / 30000.
KBT = b**2 / gamma



mu, sigma = stats.norm.fit(dat_30)
sigma_real = np.sqrt(KBT)

pdf = stats.norm.pdf(x, loc=mu, scale=sigma)
pdf_real = stats.norm.pdf(x, loc=0, scale=sigma_real)

plt.hist(dat_30, alpha=0.12, histtype="stepfilled", density=True, color = "orange", edgecolor="orange")
plt.hist(dat_30, alpha=0.3, histtype="step", density=True, color = "orange", edgecolor="orange")
plt.plot(x, pdf, "r-", lw=2, color = "orange", label = rf"Dist. simulada $x$")
plt.plot(x, pdf_real, "r-", lw=2, color = "blue", label = rf"Dist. teórica $p_x$")

mu, sigma = stats.norm.fit(dat_30_P)
sigma_real = np.sqrt(KBT)

pdf = stats.norm.pdf(x, loc=mu, scale=sigma)
pdf_real = stats.norm.pdf(x, loc=0, scale=sigma_real)

plt.hist(dat_30_P, alpha=0.12, histtype="stepfilled", density=True, color = "red", edgecolor="red")
plt.hist(dat_30_P, alpha=0.3, histtype="step", density=True, color = "red", edgecolor="red")
plt.plot(x, pdf, "r-", lw=2, color = "red", label = rf"Dist. simulada $p_x$")
plt.plot(x, pdf_real, "r-", lw=2, color = "purple", label = rf"Dist. teórica $p_x$")

plt.xlabel(r"$x$ / $p_x$")
plt.ylabel("densidad")
plt.legend()
plt.show()



