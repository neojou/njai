import pandas as pd

df = pd.read_csv('Data.csv')
print(df)

X = df.iloc[:,:-1].values
Y = df.iloc[ : , 3].values

print(X)
print(Y)

