# MARK:- libs
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from support_function import *

import matplotlib.pyplot as plt
import seaborn as sns
import time
import pprint


# MARK:- read input
path_data = "train.csv"
application_train = pd.read_csv(path_data)

# MARK:- EDA

# Ratio of labelset


def ratio_pie(application_train):
    data_labels = application_train['label']
    plot_labels = {"0", "1"}
    label_count = data_labels.value_counts()

    plt.pie(label_count, labels=plot_labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.show()

# Missing value examination


def exam_missing_value():
    df_missing = missing_values_table(application_train)
    print(df_missing.head(20))


# ratio_pie(application_train)
# exam_missing_value()
# plot_stats(application_train, 'province', label_rotation=True, horizontal_layout=False)
# plot_stats(application_train, 'maCv', label_rotation=True, horizontal_layout=False)

macv = application_train['maCv']
ori = application_train['maCv']
macv = macv.replace(np.nan, '', regex=True)
edit_macv = normalization(macv)

application_train = application_train.assign(maCv=edit_macv)
edit_macv = application_train['maCv']

# plot_stats(application_train, 'maCv', label_rotation=True, horizontal_layout=False)

f = open("macv.txt", "w", encoding='utf-8')
for m in edit_macv:
    f.write(m)
    f.write("\n")
f.close()

f = open("ori.txt", "w", encoding='utf-8')
ori = ori.replace(np.nan, '', regex=True)
for m in ori:
    f.write(m)
    f.write("\n")
f.close()
