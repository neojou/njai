from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

iris = datasets.load_iris()

iris_data = iris.data
iris_label = iris.target

train_data, test_data, train_label, test_label = train_test_split(iris_data, iris_label, test_size=0.2)


knn = KNeighborsClassifier()
knn.fit(train_data, train_label)

print(knn.predict(test_data))
print(test_label)

