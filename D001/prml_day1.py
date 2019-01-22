import numpy as np
import matplotlib.pyplot as plt


def mean_squared_error(y, ym):
    return sum((y - ym)**2)/len(y)

def mean_absolute_error(y, ym):
    return sum(abs(y - ym))/len(y)

w = 3
b = 5

x_lin = np.linspace(0, 100, 101)
y = (x_lin + np.random.randn(101) * 5) * w + b

y_hat = x_lin * w + b
mse = mean_squared_error(y, y_hat)
mae = mean_absolute_error(y, y_hat)
print("The Mean squared error is %.3f" % (mse))
print("The Mean absolute error is %.3f" % (mae))


plt.plot(x_lin, y, 'b.', label = 'data')
plt.plot(x_lin, y_hat, 'r-', label = 'prediction')
plt.title("Assume we have data and prediction")
plt.legend(loc = 2)
plt.show()
