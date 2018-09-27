
# coding: utf-8

# In[47]:

# Import modules
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta, date


# In[49]:

def get_datetime_from_string(date_string):
  return datetime.strptime(date_string, '%m/%d/%y')

def get_order_period_from_date(date_object):
  return date_object.strftime('%Y-%m')

def get_total_revenue_from_row(row):
  num_days = (row['Plan Cancel'] - row['Plan Start']).days
  revenue = (num_days / 28) * row['Monthly Payment']
  return revenue

def get_months_retention_from_row(row):
  num_days = (row['Plan Cancel'] - row['Plan Start']).days
  return math.ceil(num_days / 28)



# In[50]:

# Load in data set by reading the CSV
my_data = pd.read_csv('MRR Company Data Set.csv')


# In[51]:

my_data['Plan Start'] = my_data['Plan Start Date'].apply(get_datetime_from_string)
my_data['Plan Cancel'] = my_data['Plan Cancel Date'].apply(get_datetime_from_string)
my_data['Months Retention'] = my_data.apply(get_months_retention_from_row, axis=1)
my_data['Total Revenue'] = my_data.apply(get_total_revenue_from_row, axis=1)
my_data = my_data[my_data['Total Revenue'] > 0]


# In[52]:

groups = my_data.groupby(['Plan Start']).agg({
  'Customer ID': 'count',
  'Total Revenue': 'sum'
  })
groups.reset_index(inplace=True)


# In[53]:

groups.head()


# In[54]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
import seaborn as sns


# In[55]:

def dualAxis2Lines(timeAxis, y, z, title, axis_1_label, axis_2_label):
    sns.set_style("darkgrid")
    colors =['xkcd:sky blue','green', 'coral']
    fig, ax = plt.subplots()
    fig.set_size_inches(14,8)

    ax.plot(timeAxis,y, color=colors[0], linewidth=4, label=axis_1_label)
    ax.legend(bbox_to_anchor=(1.05, 1), loc=2)
    ax.fill_between(timeAxis.dt.to_pydatetime(), y, color=colors[1], alpha=0.3) #Create an area chart
    ax.set_ylabel(axis_1_label, fontsize=18, color=colors[0])

    ax2 = ax.twinx()
    ax2.plot(timeAxis,z, color=colors[2], linewidth=4, label=axis_2_label)
    ax2.legend(bbox_to_anchor=(1.05, 1.05), loc=2)
    ax2.set_ylabel(axis_2_label, fontsize=18, color=colors[2])

    fig.autofmt_xdate()
    fig.suptitle(title, fontsize=18)
    fig.savefig('pic1.png')


# In[56]:

title = 'MRR and Customers Count'
axis_1_label = 'MRR'
axis_2_label = 'Customers Count'
dualAxis2Lines(groups["Plan Start"], groups["Total Revenue"], groups["Customer ID"], title, axis_1_label, axis_2_label)


# In[57]:

cohort_df = my_data
cohort_df.set_index('Customer ID', inplace=True)


# In[58]:

cohort_df['CohortGroup'] = cohort_df.groupby(level=0)['Plan Start'].min().apply(lambda x: x.strftime('%Y-%m'))


# In[59]:

cohort_df.reset_index(inplace=True)


# In[60]:

cohort_df


# In[61]:

cohorts = cohort_df.groupby(['CohortGroup', 'Plan Start']).agg({'Customer ID' : pd.Series.nunique, 'Total Revenue': np.sum})


# In[62]:

cohorts.rename(columns={'Customer ID': 'TotalCustomers'}, inplace=True)


# In[63]:

cohorts.head()


# In[64]:

cohorts = cohorts.reset_index()


# In[65]:

def cohort_period(df):
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df


# In[66]:

cohorts = cohorts.groupby(['CohortGroup']).apply(cohort_period)


# In[67]:

cohorts.head()


# In[68]:

cohort_group_size = cohorts.groupby(['CohortGroup'])['TotalCustomers'].first()


# In[69]:

# cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)


# In[70]:

customer_retention = cohorts['TotalCustomers'].unstack(0).divide(cohort_group_size, axis=1)
customer_revenue = cohorts['Total Revenue'].unstack(0)


# In[71]:

colors = ['red','coral', sns.xkcd_rgb["medium green"],'green']
plt.figure(figsize=(24, 8))
plt.title('Cohorts: User Total Revenue', fontsize=22)
sns.set_style("darkgrid")
sns.heatmap(customer_revenue.T, mask=customer_revenue.T.isnull(),
            annot=True, fmt='f', cbar=False)


# In[72]:

colors = ['red','coral', sns.xkcd_rgb["medium green"],'green']
plt.figure(figsize=(24, 8))
plt.title('Cohorts: User Retention', fontsize=22)
sns.set_style("darkgrid")
sns.heatmap(customer_retention.T, mask=customer_retention.T.isnull(),
            annot=True, fmt='.0%', cbar=False)


# In[79]:

cohort_df.head()


# In[144]:

cohorts = cohort_df.groupby(['CohortGroup'])
cohorts.head()
cohorts['CohortGroup'].unique().size


# In[191]:

cohort_df['CohortGroup'].unique().sort()


# In[160]:

# np.zeros()
cohort_revenue = []
monthly_periods = math.ceil((cohort_df['Plan Start'].max() - cohort_df['Plan Start'].min()).days/28)
for i in range(monthly_periods):
    retention = np.zeros(monthly_periods)
    retention[i:monthly_periods] = 1
    revenue_cohorts.append(retention)
revenue_cohorts
monthly_periods


# In[207]:

revenues = []
start = 0
for name, group in cohorts:
    cohort = np.zeros(36)
    for index, row in group.iterrows():
        customer_revenue = np.zeros(monthly_periods)
        customer_revenue[start:start+row['Months Retention']] = row['Monthly Payment']
        cohort += customer_revenue
    start += 1
    revenues.append(cohort)
print(np.array(revenues).shape)
# customer_revenues = np.array(revenues)
customer_revenues = pd.DataFrame(data=revenues)
group_dates = sorted(cohort_df['CohortGroup'].unique())
customer_revenues['CohortGroup'] = group_dates
customer_revenues.set_index('CohortGroup', inplace=True)
customer_revenues.reset_index()
customer_revenues.head()


# In[222]:

colors = ['red','coral', sns.xkcd_rgb["medium green"],'green']
plt.figure(figsize=(36, 29))
plt.title('Monthly Revenues', fontsize=22)
sns.set_style("darkgrid")
sns.heatmap(customer_revenues, mask=customer_revenues.isnull(),
            annot=True, fmt='f', cbar=False)


# In[223]:

monthly_revenues = []
for name, group in cohorts:
    cohort = np.zeros(36)
    for index, row in group.iterrows():
        customer_revenue = np.zeros(monthly_periods)
        customer_revenue[0:row['Months Retention']] = row['Monthly Payment']
        cohort += customer_revenue
    monthly_revenues.append(cohort)
print(np.array(monthly_revenues).shape)
monthly_revenues = pd.DataFrame(data=monthly_revenues)
group_dates = sorted(cohort_df['CohortGroup'].unique())
monthly_revenues['CohortGroup'] = group_dates
monthly_revenues.set_index('CohortGroup', inplace=True)
monthly_revenues.reset_index()
monthly_revenues.head()


# In[224]:

colors = ['red','coral', sns.xkcd_rgb["medium green"],'green']
plt.figure(figsize=(36, 29))
plt.title('Cohorts: Monthly Revenues', fontsize=22)
sns.set_style("darkgrid")
sns.heatmap(monthly_revenues, mask=monthly_revenues.isnull(),
            annot=True, fmt='.0f', cbar=False)

