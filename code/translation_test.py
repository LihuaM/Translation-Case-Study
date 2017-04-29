from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as sc

def get_data(file_path_user, file_path_test):
    df_user = pd.read_csv(file_path_user)
    df_test = pd.read_csv(file_path_test)
    df = pd.merge(df_user, df_test, how='outer')
    return df

def conversion_rate_control_group(df):
    df_control = df[df.test == 0].groupby('conversion').country.value_counts().unstack()
    df_control.drop('Spain', axis=1, inplace=True)
    df_control_mean = df_control.loc[1,:].sum() / df_control.values.sum()
    df_control_rate = df_control.apply(lambda x: x[1]/x.sum())
    return df_control, df_control_mean, df_control_rate

def conversion_rate_test_group(df):
    df_test = df[df.test == 1].groupby('conversion').country.value_counts().unstack()
    df_test_mean = df_test.loc[1,:].sum()/df_test.values.sum()
    df_test_rate = df_test.apply(lambda x: x[1]/x.sum())
    return df_test, df_test_mean, df_test_rate

def conversion_rate_control_group_plot(df_control_mean, df_control_rate):
    plt.rcParams['figure.figsize'] = (8,6)
    df_control_rate.plot(kind='bar', title='Conversion Rate in Control Group')
    plt.axhline(df_control_mean, color='r')
    plt.show()

def conversion_rate_test_group_plot(df_test_mean, df_control_rate):
    plt.rcParams['figure.figsize'] = (8,6)
    df_test_rate.plot(kind='bar', title='Conversion Rate in Test Group')
    plt.axhline(df_test_mean, color='r')
    plt.show()

def sample_size_comparison_plot(df_control, df_test):
    fig,axs = plt.subplots(1, 2, sharey=True, figsize =(12,5))
    df_control.sum(axis=0).plot(kind='bar',ax=axs[0], title='Sample Size in Control Group')
    df_test.sum(axis=0).plot(kind='bar',ax=axs[1], title='Sample Size in Test Group')
    plt.show()

def check_p_val(country_list, df):
    result = pd.DataFrame()
    for country in country_list:
        cg = df[(df.country == country) & (df.test == 0)].conversion
        tg = df[(df.country == country) & (df.test == 1)].conversion
        p_val = sc.ttest_ind(cg, tg, equal_var=False)[1]
        result = result.append(dict(country=country, p_value=p_val), ignore_index=True)
    return result

if __name__ == '__main__':
    file_path_user = '../data/user_table.csv'
    file_path_test= '../data/test_table.csv'
    df = get_data(file_path_user, file_path_test)
    df_control, df_control_mean, df_control_rate = conversion_rate_control_group(df)
    df_test, df_test_mean, df_test_rate = conversion_rate_test_group(df)
    conversion_rate_control_group_plot(df_control_mean, df_control_rate)
    conversion_rate_test_group_plot(df_test_mean, df_test_rate)
    sample_size_comparison_plot(df_control, df_test)
    country_list = df_control.columns.values
    print check_p_val(country_list, df)
