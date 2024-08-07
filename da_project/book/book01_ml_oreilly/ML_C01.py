# %% 버전 확인
import matplotlib.pyplot as plt
import mglearn as mglearn
import pandas as pd
import numpy as np

print(pd.__version__)

import sys

print(sys.version)

import matplotlib

print(matplotlib.__version__)

import sklearn

print(sklearn.__version__)

# %%
from sklearn.datasets import load_iris
import sklearn

iris_dataset = load_iris()

print('iris_dataset 의 key : ', iris_dataset.keys())

# iris_dataset.values()

# iris_dataset.get("DESCR")
iris_dataset.keys()
# iris_dataset['data'][:5]
iris_dataset['target'][:5]

print('traget의 타입 : ', type(iris_dataset['target']))
print('traget의 크기 : ', iris_dataset['target'].shape)

# %%
# 훈련 데이터와 테스트 데이터

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    iris_dataset['data'], iris_dataset['target'], test_size=0.25, random_state=0
)

print(X_train.shape)
print(X_test.shape)

print(iris_dataset.feature_names)
# ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
# 꽃받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭
print(iris_dataset.target_names)
# ['setosa' 'versicolor' 'virginica']

iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)

print(iris_dataframe)

# c:색, s:사이즈, cmap : 컬러 맵 인스턴스 또는 등록 된 컬러 맵, alpha : 마커의 투명도로 0~1
pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker='o', hist_kwds={'bins': 20}, s=60,
                           alpha=.8, cmap=mglearn.cm3)
# 파이참에서 볼때만
plt.show()

# %%
# k-최근접 이웃 알고리즘
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)
# 훈련
knn.fit(X_train, y_train)
X_new = ([[5, 2.9, 1, 0.2]])

perdiction = knn.predict(X_new)
print('예측 : ', perdiction)
print('예측한 타깃의 이름 : ', iris_dataset['target_names'][perdiction])

y_pred = knn.predict(X_test)
print('테스트 세트에 대한 예측값 : \n', y_pred)
print('테스트 세트의 정확도 {:.2f}'.format(np.mean(y_pred == y_test)))

# y_pred, y_test 비교의 평균
np.mean(y_pred == y_test)

# knn에 대입하여 정확도
print('테스트 세트의 정확도 {:.2f}'.format(knn.score(X_test, y_test)))

