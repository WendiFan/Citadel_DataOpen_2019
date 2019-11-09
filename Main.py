import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures

referendumDate = pd.to_datetime("06/23/2016").tz_localize('Europe/London')
print(referendumDate)

dataset1 = pd.read_csv("datasets/dataset_1.csv")
dataset1 = dataset1.drop(dataset1[dataset1.zip.isnull()].index)
dataset1["created"] = pd.to_datetime(dataset1["created"])

datasetRef = pd.read_csv("datasets/EU-referendum-result-data.csv")
dataset1PreRef = dataset1[dataset1.created < referendumDate]
dataset1PastRef = dataset1.drop(dataset1PreRef.index)

dataset1PreRef = dataset1PreRef.reset_index(drop=True)
dataset1PastRef = dataset1PastRef.reset_index(drop=True)

print(dataset1PreRef)
print(dataset1PastRef)
