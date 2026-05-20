# DATA INGESTION & VALIDATION
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

d=pd.read_csv(r"C:\Users\HP\Downloads\European_Bank.csv")

#copying the dataset
df = d.copy(deep=True)

#data preview
df.head()

#rows, columns
print(df.shape)

#columns names
print(df.columns)

#checking data types and null values
print(df.info())

#checking no. of nulls
print(df.isnull().sum())

#binary variable consistency
print(df['Exited'].value_counts())
print(df['HasCrCard'].value_counts())
print(df['IsActiveMember'].value_counts())

#churn label accuracy
print(df['Exited'].value_counts(normalize=True))



# DATA CLEANING & PREPARATION
#removing column surname and year
df.drop(['Surname'], axis=1, inplace=True)
df.drop(['Year'], axis=1, inplace=True)

#converting categorical variables for grouping
df = pd.get_dummies(df, columns=['Geography', 'Gender'], drop_first=True)



#CUSTOMER SEGMENTATION DESIGN
#geographic segment
df['GeographySegment'] = df.apply(lambda x:'Germany' 
if x['Geography_Germany'] ==1 
else('Spain' if x['Geography_Spain']==1 
else 'France'), axis=1)

#age segmentation
df['AgeGroup'] = pd.cut(df['Age'], 
bins=[0, 30, 45, 60, 100], 
labels=['<30', '30-45', '45-60', '60+'])

#credit score segmentation
df['CreditScoreSegment'] = pd.cut(df['CreditScore'], 
bins=[300, 600, 700, 850], 
labels=['Low', 'Medium', 'High'])

#tenure segment
df['TenureGroup'] = pd.cut(df['Tenure'], 
bins=[-1, 3, 7, 10], 
labels=['New Customers', 'Mid-Term Customers', 'Long-Term Customers'])

#balance segment
df['BalanceSegment'] = pd.cut(df['Balance'], 
bins=[-1, 0, 100000, 300000], 
labels=['Zero-Balance', 'Low-Balance', 'High-Balance'])

print(df.columns)
print(df.dtypes)



#CHURN DISTRIBUTION ANALYSIS
# 1] overall churn rate
churn_dist = df['Exited'].value_counts(normalize=True)
print(churn_dist)


# 2] segment-wise churn rates
#Geography
pd.crosstab(df['GeographySegment'], df['Exited'], normalize='index')

#Age Group
pd.crosstab(df['AgeGroup'], df['Exited'], normalize='index')

#Credit Score
pd.crosstab(df['CreditScoreSegment'], df['Exited'], normalize='index')

#Tenure Group
pd.crosstab(df['TenureGroup'], df['Exited'], normalize= True)

#Balance Segment
pd.crosstab(df['BalanceSegment'], df['Exited'], normalize='index')


# 3] churn contribution by segment size
#geographic contribution
df[df['Exited'] == 1]['GeographySegment'].value_counts(normalize=True)

#age group contribution
df[df['Exited'] == 1]['AgeGroup'].value_counts(normalize=True)

#credit score contribution
df[df['Exited'] == 1]['CreditScoreSegment'].value_counts(normalize=True)

#tenure group contribution
df[df['Exited'] == 1]['TenureGroup'].value_counts(normalize=True)

#balance contribution
df[df['Exited'] == 1]['BalanceSegment'].value_counts(normalize=True)


# 4] comparision of churned vs retained profiles
df.groupby('Exited').mean(numeric_only= True)



#COMPARATIVE DEMOGRAPHIC ANALYSIS
# gender-based churn differences
pd.crosstab(df['Gender_Male'], df['Exited'], normalize='index')

# geography-age interaction analysis
pd.crosstab([df['GeographySegment'], df['AgeGroup']], df['Exited'], normalize='index')

# financial stability vs churn comparision
pd.crosstab(df['BalanceSegment'], df['Exited'], normalize='index')
pd.crosstab(df['CreditScoreSegment'], df['Exited'], normalize='index')



#HIGH-VALUE CUSTOMER CHURN ANALYSIS
#identify high-balance churners
high_balance_churners = df[(df['Balance'] > df['Balance'].median()) & (df['CreditScore'] > df['CreditScore']. median())]

#check churn in high value group
high_balance_churners['Exited'].value_counts(normalize=True)


#compare salary vs balance churn patterns
#group comparision
df.groupby('Exited')[['EstimatedSalary', 'Balance']].mean()


#quantify revenue risk from churn
revenue_risk = df[df['Exited'] == 1]['Balance'].sum()
print("Total Revenue at Risk : ", revenue_risk)


#df.to_csv
df.to_csv("European_churn_cleaned.csv", index = False)

print(df.columns)