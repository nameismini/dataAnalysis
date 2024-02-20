#%% 버전 확인
import pandas as pd
print(pd.__version__)

import sys
print(sys.version)

import matplotlib
print(matplotlib.__version__)

import sklearn
print(sklearn.__version__)


#%%
from sklearn.datasets import load_iris
import sklearn


iris_dataset = load_iris()

print('iris_dataset 의 key : ', iris_dataset.keys())

# iris_dataset.values()

iris_dataset.get("target")
