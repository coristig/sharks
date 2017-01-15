import pandas as pd
import numpy as np
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# set our path
path = '~/github/colin/sharks/'

# read in xls as a dataframe
df = pd.read_excel(path + 'data/GSAF5.xls',encoding='utf-8')

# clean our columns
df['Activity'] = df['Activity'].str.lower()
df['Activity'] = df['Activity'].str.replace('-','')
df['Species '] = df['Species '].str.lower()
df['Country'] = df['Country'].str.upper()

df.rename(columns={'Fatal (Y/N)':'Fatal','Species ':'Species','Sex ':'Sex'}, inplace=True)
df.drop(['Case Number.1', 'original order', 'Unnamed: 21', 'Unnamed: 22','pdf', 'href formula', 'href'],inplace=True, axis=1)

# clean our Fatal column up
def clean_Fatal(x):
    if x == 'Y':
        return True
    elif x == 'UNKNOWN':
        return ''
    else:
        return False


df.Fatal = df.Fatal.map(clean_Fatal)

# clean up our dates w/ some regex-ing
def year(x):
    res = re.search(r'([0-9]{4})',str(x))
    if res is None:
        return None
    else:
        return int(res.group())

def day(x):
    res = re.search(r'(^|\b)(([0-9]{2}))(?=-)',str(x))
    if res is None:
        return None
    else:
        return int(res.group())

def month(x):
    res = re.search(r'(?!-)(([A-Za-z]{3}))(?=-)',str(x))
    if res is None:
        return None
    else:
        return str(res.group())

df['year'] = df['Date'].map(year)
df['month'] = df['Date'].map(month)
df['day'] = df['Date'].map(day)

df.Activity.value_counts()

# people murdered (thrown overboard to sharks)
df[(df.Activity=='murder')][['Date','Country','Activity','Injury']]

#
len(df[df['Activity'].str.contains('diving')==True]['Activity'].value_counts())
df[df['Activity'].str.contains('diving')==True]['Activity'].value_counts()

def types(x):
    #x = x.encode('utf-8').strip()
    if re.search(r'\bscuba\b',str(x)):
        x='scuba_diving'
        return x
    elif re.search(r"\bspearfishing\b",str(x)) and not(re.search(r'\bscuba\b',str(x))):
        x = 'spear_fishing'
        return x
    elif re.search(r"\bswimming\b",str(x)):
        x = 'swimming'
        return x
    elif re.search(r"\bstanding\b",str(x)):
        x = 'standing'
        return x
    elif re.search("bodysurfing",str(x)) or (re.search("body surfing",str(x))):
        x = 'body_surfing'
        return x
    elif re.search("bodyboarding",str(x)) or (re.search("body-boarding",str(x)))or (re.search("body boarding",str(x))):
        x = 'body_boarding'
        return x
    elif re.search(r"\bsurfing\b",str(x)) or (re.search("surfboard",str(x))):
        x = 'surfing'
        return x
    elif re.search("surf-skiing",str(x)) or (re.search("surf skiing",str(x))) or (re.search("surfskiing",str(x))):
        x = 'surf_skiing'
        return x
    elif re.search("pearl diving",str(x)):
        x = 'pearl_diving'
        return x
    elif re.search(r"\bdiving\b",str(x)):
        x = 'diving'
        return x
    elif re.search(r"\bspear\b",str(x)):
        x = 'spear_fishing'
        return x
    elif re.search(r"\bbathing\b",str(x)):
        x = 'bathing'
        return x
    elif re.search(r"\bfishing\b",str(x)):
        x = 'fishing'
        return x
    elif re.search(r"\bfreediving\b",str(x)) or (re.search("free diving",str(x))):
        x = 'free_diving'
        return x
    elif re.search("boogie",str(x)):
        x = 'boogie_boarding'
        return x
    elif re.search("capsized",str(x)) or (re.search("sank",str(x))) or (re.search("went down",str(x)))     or (re.search("disaster",str(x))) or (re.search("crash",str(x))) or (re.search("wreck",str(x))):
        x = 'sea_disaster'
        return x
    elif re.search(r"\bwading\b",str(x)):
        x = 'wading'
        return x
    else: return x

df['Activity'] = df['Activity'].map(types)

df.Type.value_counts()

# create a plot for top attacks by activity over time
top_activities = df[df.Type=='Unprovoked'].Activity.value_counts().index.tolist()[:10]
df_top_activities = df[df.Activity.isin(top_activities) & (df.year >1950) & (df.Type=='Unprovoked')].dropna(axis=0,subset=['year'])
df_top_activities.groupby(['Activity','year']).count().reset_index()

years = range(1950, 2016)
activities = df_top_activities.Activity.unique()

import itertools

# http://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
def expandgrid(*itrs):
   product = list(itertools.product(*itrs))
   return {'Var{}'.format(i+1):[x[i] for x in product] for i in range(len(itrs))}

all_combos = expandgrid(activities, years)
all_combos = pd.DataFrame(all_combos)
all_combos.columns = ["Activity", "year"]
all_years = pd.merge(all_combos, df_top_activities, on=["year", "Activity"], how='left')
all_years = all_years.groupby(['Activity','year']).count().reset_index()

from ggplot import *

ggplot(aes(x='year', y='Case Number', color='Activity'),all_years) + geom_line() + ylab("Number of Attacks") +\
    xlab("Year") + ggtitle("Shark Attacks by Activity Type")

### FATAL Attacks
top_activities = df[df.Type=='Unprovoked'].Activity.value_counts().index.tolist()[:10]
df_top_activities = df[df.Activity.isin(top_activities) & (df.year >1950) & (df.Type=='Unprovoked') & (df.Fatal==True)].dropna(axis=0,subset=['year'])
df_top_activities.groupby(['Activity','year']).count().reset_index()

years = range(1950, 2016)
activities = df_top_activities.Activity.unique()

import itertools

# http://stackoverflow.com/questions/12130883/r-expand-grid-function-in-python
def expandgrid(*itrs):
   product = list(itertools.product(*itrs))
   return {'Var{}'.format(i+1):[x[i] for x in product] for i in range(len(itrs))}

all_combos = expandgrid(activities, years)
all_combos = pd.DataFrame(all_combos)
all_combos.columns = ["Activity", "year"]
all_years = pd.merge(all_combos, df_top_activities, on=["year", "Activity"], how='left')
all_years = all_years.groupby(['Activity','year']).count().reset_index()

from ggplot import *

ggplot(aes(x='year', y='Case Number', color='Activity'),all_years) + geom_line() + ylab("Number of Attacks") +\
    xlab("Year") + ggtitle("Fatal Shark Attacks by Activity Type")
