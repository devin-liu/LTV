# Import modules
import pandas as pd
from datetime import datetime, timedelta, date

# Load in data set by reading the CSV
my_data = pd.read_csv('MRR Company Data Set.csv')

# Separate plans into dataframes
# What is a dataframe?
# You pick out a group that you want to analyze in the spreadsheet
# The dataframe is a wrapper around that group
# We are categorizing the groups by their plan types

# simple LTV
# what is a function definition?
# what are parameters?

# Pipeline functions to turn the CSV data into usable insights
# We let this function take care of items row by row

def getCustomerValuePerWeekFromRow(row):
  # Access row's customer value cell
  # Row name is Monthly Payment
  # Return is how we close out our logic and send back a value
  return row['Monthly Payment'] / 4


def getCustomerValuePerMonth(row):
  # Access row's customer value cell
  # Row name is Monthly Payment
  # Return is how we close out our logic and send back a value
  return row['Monthly Payment']


def get_datetime_from_string(date_string):
  return datetime.strptime(date_string, '%m/%d/%y')


def getTimeDeltaFromRow(row):
  startString = row['Plan Start Date']
  endString = row['Plan Cancel Date']
  # Our cell rows are currently just letters and numbers
  # We need to translate them into dates that the computer can understand

  # The datetime library has a strptime function that receives a string and a date format
  # The date format is decided by us using characters like '%m', '%d', and '/'
  # to specify what the date format we have, not the format we want

  # datetime.strptime('10/20/15', '%m/%d/%y')
  startDate = datetime.strptime(startString, '%m/%d/%y')
  endDate = datetime.strptime(endString, '%m/%d/%y')

  # We now have machine-readable dates
  # We can directly subtract the dates from each other
  # However this will not return a single number
  # It will create a new object

  # Steve Jobs:
  # Objects are like people.
  # They’re living, breathing things that have knowledge inside them about how to do things
  # and have memory inside them so they can remember things. And rather than interacting
  # with them at a very low level, you interact with them at a very
  # high level of abstraction, like we’re doing right here.

  # Time delta objects store two dates, and can tell you the difference in days, years, etc

  # startDate = datetime.strptime('10/19/15', '%m/%d/%y')
  # endDate = datetime.strptime('01/19/15', '%m/%d/%y')
  return (endDate - startDate)

def getDaysFromRow(row):
  # We are creating a time delta object and making sure the times we parse are standardized to days
  # The .days attribute is calculated from the difference between two machine-readable dates
  return getTimeDeltaFromRow(row).days

def getMonthsFromRow(row):
  # We are creating a time delta object and making sure the times we parse are standardized to days
  # The .days attribute is calculated from the difference between two machine-readable dates
  return getTimeDeltaFromRow(row).days / 28

def getYearsFromRow(row):
  # After we calculate the days in our row, it is easy to calculate what % of a year it is
  return getDaysFromRow(row) / 365

def getSimpleLTVFromGroup(df):
  # get (a) -> average customer value per week
  # get (t) -> average customer lifespan in years

  # We are accessing the dataframe's columns and creating new calculated cells
  # df.apply will apply the calculations to every row in the columns
  # Axis 1 means do it every row
  df['CustomerValue'] =  df.apply(getCustomerValuePerMonth,axis=1)
  df['CustomerLifespan'] =  df.apply(getMonthsFromRow,axis=1)

  # We now have two new columns (a) and (t) for LTV calculation

  # clean data frame
  # Make sure to eliminate the rows where the begin and end dates are not possible (reversed)
  df = df[df['CustomerLifespan'] > 0]

  # Have pandas automatically calculate the mean of your entire column
  a = df['CustomerValue'].mean()
  t = df['CustomerLifespan'].mean()
  # LTV formula is avg customer value * avg customer lifespan
  return a*t

# # We can now run the calculations on the spreadsheet and display it on your screen
# # Run the calculations on each group, separated by their plan type
for name, group in my_data.groupby('Plan Id'):
  print(f'Plan {name} Simple LTV: ${getSimpleLTVFromGroup(group)}')
