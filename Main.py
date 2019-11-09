import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures
from scipy import stats
from datetime import date

referendumDate = pd.to_datetime("06/23/2016").tz_localize('Europe/London')

resultDictDelta = {}
resultDictCreated = {}
resultDictDeleted = {}

for bigIndex in range(1, 10):
    dataset1 = pd.read_csv("datasets/job_listings.csv")
    dataset1 = dataset1.drop(dataset1[dataset1.created.isnull()].index)
    dataset1 = dataset1.drop(dataset1[dataset1["SOC_occupation_code"] < bigIndex * 1000].index)
    dataset1 = dataset1.drop(dataset1[dataset1["SOC_occupation_code"] > (bigIndex + 1) * 1000].index)

    def getPrePastRef(key):
        dataset1[key] = pd.to_datetime(dataset1[key])

        dataset1[key] = dataset1[key].dt.round("14D")

        dataset1ByDate = dataset1.groupby([key])

        """drop_indices = np.random.choice(dataset1.index, 1639220, replace=False)
        dataset1 = dataset1.drop(drop_indices)
        """
        #datasetRef = pd.read_csv("datasets/EU-referendum-result-data.csv")

        dataset1PreRef = dataset1[dataset1[key] < referendumDate]
        dataset1PastRef = dataset1.drop(dataset1PreRef.index)
        dataset1PreRef = dataset1PreRef[dataset1PreRef[key] > (referendumDate - (pd.to_datetime(dataset1[key].values.max()).tz_localize('Europe/London') - referendumDate))]

        dataset1PreRef = dataset1PreRef.reset_index(drop=True)
        dataset1PastRef = dataset1PastRef.reset_index(drop=True)

        return dataset1PreRef, dataset1PastRef

    createdPre, createdPast = getPrePastRef("created")
    deletedPre, deletedPast = getPrePastRef("delete_date")

    print("t-test")
    #print([x for x in dataset1PreRef.groupby([key]).size()])

    createdPreGrouped = createdPre.groupby(["created"]).size()
    deletdPreGrouped = deletedPre.groupby(["delete_date"]).size()
    deltaPre = [0] * len(createdPreGrouped)
    for i in range(len(createdPreGrouped)):
        deltaPre[i] = createdPreGrouped[i] - deletdPreGrouped[i]

    createdPastGrouped = createdPast.groupby(["created"]).size()
    deletdPastGrouped = deletedPast.groupby(["delete_date"]).size()
    deltaPast = [0] * len(createdPastGrouped)
    for i in range(len(createdPastGrouped)):
        deltaPast[i] = createdPastGrouped[i] - deletdPastGrouped[i]

    resultDictDelta[bigIndex] = np.concatenate([[x for x in deltaPre], [x for x in deltaPast]], axis=None)
    resultDictCreated[bigIndex] = np.concatenate([[x for x in createdPreGrouped], [x for x in createdPastGrouped]], axis=None)
    resultDictDeleted[bigIndex] = np.concatenate([[x for x in deletdPreGrouped], [x for x in deletdPastGrouped]], axis=None)

    print(stats.ttest_ind(deltaPre, deltaPast, equal_var = False))
    print(stats.ttest_ind(createdPreGrouped, createdPastGrouped, equal_var = False))
    print(stats.ttest_ind(deletdPreGrouped, deletdPastGrouped, equal_var = False))
    print ("done with " + str(bigIndex))

pd.DataFrame(data=resultDictDelta).to_csv("deltatotal.csv")
pd.DataFrame(data=resultDictCreated).to_csv("createdtotal.csv")
pd.DataFrame(data=resultDictDeleted).to_csv("deletedtotal.csv")
