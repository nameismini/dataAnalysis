'''
 * 도서의 두번째 장의 실습부분입니다.
 * @author Min
 * @version 1.0
 * @since 2024-03-13
'''

# %% import 영역
import mglearn.datasets
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from scipy import sparse
import pandas as pd

# %% Memo
# 분류 classficateion
#    - 이진분류 : 예/아니오 와 같이 두가지로만 선택함  , 다중분류 : 셋 이상의 클래수로 나누는것
# 회귀 regression : 연속적인 숫자, 프로그래밍 언어로는 부동소수점(수학으로는 실수)를 예측하는것

# 과대적합 : 가진 정보를 모두 사용해서 복잡한 모델을 만들어 내는것
# 과소적합 : 반대로 모델이 너무 간단하면, 데이터의 면면과 다양성을 잡아내지 못하고 훈련세트에도 잘 맞지 않을것
# 과대적합도 아닌 과소적합도 아닌 일반화 성능이 최대가 되는 최적점에 있는 모델을 만들어 내는것이 좋음


# %% 지도학습 알고리즘

# 현재 컴퓨터에 설치된 글꼴의 폰트 패밀리 알아보는 방법
[f.name for f in fm.fontManager.ttflist]
# 한글 폰트
plt.rc('font', family='Malgun Gothic')

# Glyph 8722 (\N{MINUS SIGN}) missing from current font 메세지 방지
plt.rcParams['axes.unicode_minus'] = False

X, y = mglearn.datasets.make_forge()
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
plt.legend(["클래스 1", "클래스 2"], loc=4)
plt.xlabel("첫 번째 특성")
plt.ylabel("두 번째 특성")
plt.show()

# %% 문법 참고

# test용 X, y 는 X, y = mglearn.datasets.make_forge()

# 1. 서로다른 차원 합치기 reshape + concatenate
#    test_data = np.concatenate((X[:, 0].reshape(-1, 1), y.reshape(-1, 1)), axis=1)

# 2. array로 변환
# X[:, 0].tolist()

# 3. #1차원/차원 값만 가져오기
# # a[:,0] # a[:,1]

# 4. array 안에서 특정값만 걸러내기
# idx = np.where(test_data[:, 1] == 1)


# %% mglearn 말고 그냥 자료 만들어 보기

X, y = mglearn.datasets.make_forge()
yy = y.reshape([-1, 1])
data = np.concatenate((X, yy), axis=1)

plt.scatter(data[data[:, 2] == 0, 0], data[data[:, 2] == 0, 1], marker='^')
plt.scatter(data[data[:, 2] == 1, 0], data[data[:, 2] == 1, 1], marker='o')
plt.show()

# %% make_wave dataset 으로 테스트
X, y = mglearn.datasets.make_wave()

# plt.figure(figsize=(10,6)): 그래프 크기를 가로10, 세로 6으로 지정
# plt.scatter(x,y): x와 y의 데이터로 산점도를 그림
# plt.xlabel : x축 라벨링
# plt.ylabel: y축 라벨링
# plt.show(): terminal에 그래프를 표시

plt.figure(figsize=(10, 6))
# scatter 비하여 속도는 빠르나 기능이 작음 marker='o'으로 산점도 가능
plt.plot(X, y, 'o')
# scatter 방법은 크기, 색상 등에 사용자 정의할 수 있어 훨씬 자유로움
plt.scatter(X, y)
plt.show()

# %% 위스콘신 유방암 데이터셋 - cancer

from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer()
print(cancer.keys())

result = {n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}
print(result)
print(cancer.feature_names)

# mglearn.plots.plot_knn_classification(n_neighbors=1)

# plt.scatter()

# plt.show()

# %% 보스턴 주택가격 데이터셋

# from sklearn.datasets import load_boston

import pandas as pd
import numpy as np

data_url = "http://lib.stat.cmu.edu/datasets/boston"
raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

# test1 = raw_df.values[::2, :]
# test2 = raw_df.values[1::2, :2]


# %% K-NN k-최근접 이웃 분류

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

X, y = mglearn.datasets.make_forge()

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
clf = KNeighborsClassifier(n_neighbors=3)

# 학습
clf.fit(X_train, y_train)

# 예측
print("데이터 세트 예측 : ", clf.predict(X_test))
print("테스트 세트 정확도{:.2f}".format(clf.score(X_test, y_test)))

#%% 결정경계 나누기

fig, axes = plt.subplots(1, 3, figsize=(10,3))


for n_neighbors, ax in zip([1,3,9], axes):
    plt.scatter(X[:, 0], X[:, 1], c=y, cmap='winter')
    # mglearn.plots.plot_2d_separator(clf, X, fill=True, eps=0.5, ax=ax, alpha=.4)
    # ax.set_xticks(())
    # ax.set_yticks(())

plt.show()

