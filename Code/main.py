# MARK:- libs
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from support_function import *

import matplotlib.pyplot as plt
import seaborn as sns
import re
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


