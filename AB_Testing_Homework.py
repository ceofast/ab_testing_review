# Business Problem

# Facebook recently introduced a new type of bid, average bidding,
# as an alternative to the current type of bidding called maximum bidding.
# One of our clients, bombabomba.com, decided to test this new feature,
# and would like to do an A/B test to see if averagebidding converts more than maximumbidding.


# Dataset Story

# In this dataset, which includes the website information of bombabomba.com,
# there is information such as the number of advertisements that users see and click,
# as well as earnings information from here.
# There are two separate data sets, the control and test groups.


# Variables

# Impression: Ad views count
# Click: Indicates the number of clicks on the displayed ad.
# Purchase: Indicates the number of products purchased after the ads clicked.
# Earning: Earnings after purchased products


# Task 1: Define the hypothesis of the A/B test.

# H0: There is no statistically significant difference between maximum bidding and average bidding.
# H1: There is statistically significant difference between maximum bidding and average bidding.


# Task 2: Comment on whether the test results are statistically significant.

# Task 3: Which tests did you use, please indicate the reasons?

# Task 4: Based on your answer in Task 2, what is your advice to the client?

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, pearsonr, spearmanr, kendalltau, \
    f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_excel(r"/Users/cenancanbikmaz/PycharmProjects/DSMLBC-7/HAFTA_5/ab_testing.xlsx", sheet_name="Control Group")
df.head()

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

test = pd.read_excel(r"/Users/cenancanbikmaz/PycharmProjects/DSMLBC-7/HAFTA_5/ab_testing.xlsx", sheet_name="Test Group")
test.head()

check_df(test)

def create_displot(dataframe, col):
    sns.displot(data=dataframe, x=col, kde=True)
    plt.show()

df["Purchase"].mean()  #Maximum Bidding

test["Purchase"].mean() #Average Bidding

# Normality Assumption
# H0: There is no difference between the number of products purchased. (p-value < 0.05)
# H1: Normal distribution assumption not provided.

test_stat, pvalue = shapiro(df["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# The p-value is greater than 0.05, it means we can not reject H0 hypothesis,
# and we say that it's a normal distribution for df group.

create_displot(df, "Purchase")

test_stat, pvalue = shapiro(test["Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# The p-value is greater than 0.05, it means we can not rejected H0 hypothesis,
# and we say that it's a normal distribution for test group.

create_displot(test, "Purchase")

# Variance Homogeneity Assumption

# H0: Variances are homogeneous.
# H1: Variances aren't homogeneous.

test_stat, pvalue = levene(df["Purchase"], test["Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# The p-value is greater than 0.05 and we can't reject H0 hypothesis.
# It means, variances are homogenous and both dataset are the similar.
# An independent two-sample t-test will be applied.

test_stat, pvalue = ttest_ind(df["Purchase"], test["Purchase"], equal_var=True)
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# P-value is greater than 0.05 and we can't reject H0 hypothesis.
# There is no significant difference in sales after clicking on Web Ads.

# Conlusion

# After statistical applications, a statistical difference was found between
# the control and test groups, but no significant difference was found.
# Shapiro test was applied to test whether the control and test groups comply
# with the normality assumption. The next step was homogeneity of variance,
# since it provided the assumption of normality in both groups.
# Levene's test was used to observe the homogeneity of the variances of the two groups.
# When the values obtained as a result of the test were examined, it was seen that
# there was a similarity between the homogeneity of variance of the groups.
# At the same time, since it provides variance homogeneity,
# the Independent Two Sample T-Test was applied to reveal the statistical significance
# of the difference between the two groups.
# The p value obtained after applying the Independent Two Sample T-Test was examined.
# H0 hypothesis could not be rejected because our value was not less than 0.05.
# Even if there is a difference between the means of the control and test groups,
# it was determined as a result of the analyzes that this was not statistically significant.
# A new test and measurement can be made with more samples to re-examine
# the new system added to the website.