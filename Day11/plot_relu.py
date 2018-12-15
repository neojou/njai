import numpy as np
import matplotlib.pyplot as plt

def relu_func(x):
	if x <= 0:
		return 0
	else:
		return x

def relu_array(x):
	y = []
	for item in x:
		y.append(relu_func(item))
	return y

x = np.arange(-10., 10., 0.2)
sig = relu_array(x)

plt.plot(x, sig)
plt.show()

