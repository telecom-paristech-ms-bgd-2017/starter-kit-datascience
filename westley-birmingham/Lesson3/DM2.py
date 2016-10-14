import numpy as np
import matplotlib.pyplot as plt

# 500 samples from Beta distribution
beta_distrib = np.random.beta(2, 5, 500)
len(beta_distrib)

# Display the histogram
plt.figure()
plt.hist(beta_distrib, 25, alpha = 0.4)
plt.title("Histogram Beta distribution")
plt.show()

# Generate 500 independant random vectors
X_i = np.random.beta(2, 5, [500, 2])
print(X_i[:10])