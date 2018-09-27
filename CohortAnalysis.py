# Import modules
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

# Load in data set by reading the CSV
my_data = pd.read_csv('MRR Company Data Set.csv')


def get_datetime_from_string(date_string):
  return datetime.strptime(date_string, '%m/%d/%y')

def get_order_period_from_date(date_object):
  return date_object.strftime('%Y-%m')

def get_total_revenue_from_row(row):
  days = (row['Plan Cancel'] - row['Plan Start']).days
  revenue = (days / 28) * row['Monthly Payment']
  return revenue

my_data['Plan Start'] = my_data['Plan Start Date'].apply(get_datetime_from_string).values
my_data['Plan Cancel'] = my_data['Plan Cancel Date'].apply(get_datetime_from_string)
my_data['Order Period'] = my_data['Plan Start'].apply(get_order_period_from_date)
my_data['Total Revenue'] = my_data.apply(get_total_revenue_from_row, axis=1)


my_data['Cohort Group'] = my_data.groupby(level=0)['Plan Start'].min().apply(lambda x: x.strftime('%Y-%m'))
groups = my_data.groupby(['Order Period']).agg({
  'Customer ID': 'count',
  'Total Revenue': 'sum'
  })
groups.reset_index(inplace=True)
print(groups.head())


%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns

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

title = 'MRR and Customers Count'
axis_1_label = 'MRR'
axis_2_label = 'Customers Count'
dualAxis2Lines(groups["Order Period"], groups["Total Revenue"], groups["Customer ID"], title, axis_1_label, axis_2_label)



# grouped = planOne.groupby(['Cohort Group', 'Order Period'])


# cohorts = grouped.agg({'Customer ID': pd.Series.nunique,
#                        'Monthly Payment': np.sum})

# cohorts.rename(columns={'Customer ID': 'TotalUsers'}, inplace=True)



# def cohort_period(df):
#     """
#     Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.

#     Example
#     -------
#     Say you want to get the 3rd month for every user:
#         df.sort(['UserId', 'OrderTime', inplace=True)
#         df = df.groupby('UserId').apply(cohort_period)
#         df[df.CohortPeriod == 3]
#     """
#     df['Cohort Period'] = np.arange(len(df)) + 1
#     return df


# cohorts = cohorts.groupby(level=0).apply(cohort_period)
# print(cohorts['TotalUsers'].unstack(0))
