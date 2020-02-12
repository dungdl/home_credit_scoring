import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

import matplotlib.pyplot as plt
import seaborn as sns
import re
# Function to count missing values by column# Funct


def missing_values_table(df):
    # Total missing values
    mis_val = df.isnull().sum()

    # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)

    # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)

    # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(
        columns={0: 'Missing Values', 1: '% of Total Values'})

    # Sort the table by percentage of missing value in descending order
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:, 1] != 0].sort_values(
        '% of Total Values', ascending=False).round(1)

    # Print some summary information
    print("\nYour selected dataframe has " + str(df.shape[1]) + " columns.\n"
          "There are " + str(mis_val_table_ren_columns.shape[0]) +
          " columns that have missing values.")

    # Return the dataframe with missing information
    return mis_val_table_ren_columns


def plot_stats(application_train, feature, label_rotation=False, horizontal_layout=True):
    temp = application_train[feature].value_counts()
    df1 = pd.DataFrame(
        {feature: temp.index, 'Number of contracts': temp.values})

    # Calculate the percentage of target=1 per category value
    cat_perc = application_train[[feature, 'label']].groupby(
        [feature], as_index=False).mean()
    cat_perc.sort_values(by='label', ascending=False, inplace=True)

    if(horizontal_layout):
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(12, 6))
    else:
        fig, (ax1, ax2) = plt.subplots(nrows=2, figsize=(12, 14))
    sns.set_color_codes("pastel")
    s = sns.barplot(ax=ax1, x=feature, y="Number of contracts", data=df1)
    if(label_rotation):
        s.set_xticklabels(s.get_xticklabels(), rotation=90)

    s = sns.barplot(ax=ax2, x=feature, y='label',
                    order=cat_perc[feature], data=cat_perc)
    if(label_rotation):
        s.set_xticklabels(s.get_xticklabels(), rotation=90)
    plt.ylabel('Percent of target with value 1 [%]', fontsize=10)
    plt.tick_params(axis='both', which='major', labelsize=10)

    plt.show()


def plot_many_stats(l_features, label_rotaion=True, horizontal_layout=True):
    for feature in l_features:
        plot_stats(feature, label_rotation=label_rotaion,
                   horizontal_layout=horizontal_layout)


# Plot distribution of one feature
def plot_distribution(feature, color, bins=100):
    plt.figure(figsize=(10, 6))
    plt.title("Distribution of %s" % feature)
    sns.distplot(application_train[feature].dropna(),
                 color=color, kde=True, bins=bins)
    plt.show()


def plot_many_distribution(dict_features_bin_color):
    nrow = len(dict_features_bin_color)
    plt.figure()
    fig, ax = plt.subplots(nrow, 1, figsize=(12, 6*nrow))

    i = 0
    for e_key, e_value in dict_features_bin_color.items():
        i += 1
        plt.subplot(nrow, 1, i)
        plt.title("Distribution of %s" % e_key)
        sns.distplot(application_train[e_key].dropna(
        ), color=e_value['color'], kde=True, bins=e_value['bins'])
    plt.show()


# Plot distribution of multiple features, with TARGET = 1/0 on the same graph
def plot_distribution_comp(var, nrow=2):

    i = 0
    t1 = application_train.loc[application_train['label'] != 0]
    t1 = t1.dropna()
    t0 = application_train.loc[application_train['label'] == 0]
    t0 = t0.dropna()

    sns.set_style('whitegrid')
    plt.figure()
    fig, ax = plt.subplots(nrow, 1, figsize=(12, 6*nrow))

    for feature in var:
        i += 1
        plt.subplot(nrow, 1, i)
        sns.kdeplot(t1[feature], bw=0.5, label="label = 1")
        sns.kdeplot(t0[feature], bw=0.5, label="label = 0")
        plt.ylabel('Density plot', fontsize=12)
        plt.xlabel(feature, fontsize=12)
        locs, labels = plt.xticks()
        plt.tick_params(axis='both', which='major', labelsize=12)
    plt.show()


def normalization(input):
    macv = input
    patterns = {}

    f = open("patterns.txt", "r", encoding='utf-8')
    i = 0
    for line in f:
        line = re.sub(r'\n', '', line, flags=re.UNICODE)
        words = re.split(r':', line, flags=re.UNICODE)
        patterns[words[0]] = words[1]
    f.close()

    for i in range(macv.__len__()):
        line = macv[i].rstrip()
        line = re.sub('(\s{2,})', ' ', line)
        line = line.lower()
        match = False
        rep = "{,1}"

        for k in patterns:
            if re.match(rf"(.*{k[0]}[. ]{rep}{k[1]}.*)", line, flags=re.UNICODE):
                macv[i] = patterns[k]
                match = True
                break
        if not match:
            words = re.split(r" ", line, flags=re.UNICODE)
            if words.__len__() >= 2:
                if (words[0]) not in patterns:
                    try:
                        key = str(words[0][0]) + str(words[1][0])
                        if key in patterns:
                            value = patterns[key]
                    except Exception:
                        print("ERROR:" + str(i))
                        pprint.pprint(words)
                else:
                    key = words[0]
                    value = patterns[key]

                if key in patterns:
                    current_pattern = re.compile(rf"(.*{key[0]}[. ]{rep}{key[1]}.*)|"
                                                 rf"({value}.*)", flags=re.IGNORECASE)
                    if current_pattern.match(line):
                        macv[i] = patterns[k]
    return macv
