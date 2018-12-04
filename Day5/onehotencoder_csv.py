import pandas as pd

df = pd.read_csv('Data.csv')
#print(df)

X = df.iloc[:,:-1].values
Y = df.iloc[ : , 3].values

print(Y)

from sklearn.preprocessing import Imputer
imputer = Imputer(missing_values = "NaN", strategy = "mean", axis = 0)
imputer = imputer.fit(X[ : , 1:3])
X[ : , 1:3] =  imputer.transform(X[ : , 1:3])


from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X = LabelEncoder()
X[ : , 0] = labelencoder_X.fit_transform(X[ : , 0])


onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()


labelencoder_Y = LabelEncoder()
Y = labelencoder_Y.fit_transform(Y)

print(Y)
