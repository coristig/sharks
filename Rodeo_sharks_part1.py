import pandas as pd
import numpy as np
import re

# read in xls as a dataframe
df = pd.read_excel('/Users/coristig/github/colin/sharks/GSAF5.xls')

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

df[(df.Activity=='murder')][['Date','Country','Activity','Injury']]

#df[df['Activity'].str.contains('diving')==True]['Activity'].value_counts()

def types(x):
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

top_activities = df[df.Type=='Unprovoked'].Activity.value_counts().index.tolist()[:10]
df_top_activities = df[df.Activity.isin(top_activities) & (df.year >1950) & (df.Type=='Unprovoked')].dropna(axis=0,subset=['year'])
df_top_activities.groupby(['Activity','year']).count().reset_index()

years = range(1950, 2016)
activities = df_top_activities.Activity.unique()