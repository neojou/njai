import numpy as np
import matplotlib.pyplot as plt

def sigmoid_func(x):
	y = 1/(1 + np.exp(-x))
	return y

def sigmoid_array(x):
	y = []
	for item in x:
		y.append(sigmoid_func(item))
	return y

x = np.arange(-10., 10., 0.2)
sig = sigmoid_array(x)

plt.plot(x, sig)
plt.show()

