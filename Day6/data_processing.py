import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataset = pd.read_csv('studentscores.csv')
X = dataset.iloc[ :, : 1].values
Y = dataset.iloc[ : , 1].values

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 1/4, random_state = 0)

print(X_train)
print(X_test)
print(Y_train)
print(Y_test)


