from sklearn import preprocessing
enc = preprocessing.OneHotEncoder()
enc.fit([[1,4,1],[3,2,0],[5,4,1],[7,6,0]])
X = enc.transform([[3,2,1]]).toarray()

print(X)

