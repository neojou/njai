from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.svm import SVC

iris = datasets.load_iris()

iris_data = iris.data
iris_label = iris.target

train_data, test_data, train_label, test_label = train_test_split(iris_data, iris_label, test_size=0.8)

# KNN
knn = KNeighborsClassifier()
knn.fit(train_data, train_label)
score_knn = knn.score(test_data, test_label)
print("KNN Score %f \n" %score_knn)

# SVM
clf = SVC()
clf.fit(train_data, train_label)
score_clf = clf.score(test_data, test_label)
print("SVM Score %f \n" %score_clf)

