import pandas as pd

df = pd.read_csv('Data.csv')
print(df)

X = df.iloc[:,:-1].values
Y = df.iloc[ : , 3].values

print(X)

from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)
imputer = imputer.fit(X[ : , 1:3])
X[ : , 1:3] =  imputer.transform(X[ : , 1:3])

print(X)

