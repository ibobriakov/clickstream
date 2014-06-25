
# coding: utf-8

# In[335]:

import pandas as pd
import fnmatch
import os
import numpy as np


# In[336]:

android = pd.DataFrame()
itunes = pd.DataFrame()


# In[337]:

for file in os.listdir('.\data'):
    if fnmatch.fnmatch(file, '*android*.csv'):
        fname = "data\\" + file
        print "appending: " + fname
        file_df = pd.read_csv(fname)#, index_col='id')
        print file_df['Latino / Hispanic'].head(25) 
        android = pd.concat([android, file_df])

        
    if fnmatch.fnmatch(file, '*itunes*.csv'):
        fname = "data\\" + file
        print "appending: " + fname
        file_df = pd.read_csv(fname, index_col='id')
        print file_df['Latino / Hispanic'].head(25) 
        itunes = pd.concat([itunes,file_df])
    


# In[338]:

def count_totals(df):
    df['Ethnic-total'] = df['Caucasian (white)'] + df['Middle Eastern'] + df['Native American'] + df['East Indian'] + df['African descent (black)']  + df['Asian'] + df['Latino / Hispanic'] +df['Pacific Islander']
    df['Related Apps: Ethnic-total'] = df['Related Apps: Caucasian (white)'] + df['Related Apps: Middle Eastern'] +         df['Related Apps: Native American'] + df['Related Apps: East Indian'] + df['Related Apps: African descent (black)']  +         df['Related Apps: Asian'] + df['Related Apps: Latino / Hispanic'] +df['Related Apps: Pacific Islander']
    
    df['Gender-total'] = df['M'] + df['F']
    df['Related Apps: Gender-total'] = df['Related Apps: F'] + df['Related Apps: M']
    
    return df

itunes = count_totals(itunes)
android = count_totals(android)


# In[339]:


def share_count(row, one, two):
    import math
    #for i in two:
    
    if math.isnan(row[two]) or row[two]==0:
        #print "nan or zero:", row[one], row[two]
        return 0
    else:
        #print "ok:", row[one], row[two]
        return row[one] / row[two]

#df = df[df['F-share'].notnull()]


# In[340]:

def share_platform_gender(df):
    df['F-share'] = df.apply(share_count, one = 'F', two = 'Gender-total', axis=1)
    df['M-share'] = df.apply(share_count, one = 'M', two = 'Gender-total', axis=1)
    
    #df['Related Apps: F-share'] = df['Related Apps: F'] / (df['Related Apps: F'] + df['Related Apps: M'])
    df['Related Apps: F-share'] = df.apply(share_count, one = 'Related Apps: F', two = 'Related Apps: Gender-total', axis=1)
    df['Related Apps: M-share'] = df.apply(share_count, one = 'Related Apps: M', two = 'Related Apps: Gender-total', axis=1)
    
    return df


itunes = share_platform_gender(itunes)
android = share_platform_gender(android)


# In[341]:

def share_platform_age(df):
    ethnic = [ 'Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 
    
    for e in ethnic:
        res = e + '-share'
        df[res] = df.apply(share_count, one = e, two = 'Ethnic-total', axis=1)

    for e in ethnic:
        e = "Related Apps: " + e
        res = e + '-share'
        df[res] = df.apply(share_count, one = e, two = 'Related Apps: Ethnic-total', axis=1)
    
    return df

itunes = share_platform_age(itunes)
android = share_platform_age(android)


# In[342]:

itunes.columns.values


# In[343]:

android.to_csv('tmp\\a-sample.csv')
itunes.to_csv('tmp\\i-sample.csv')


# In[344]:

def index_count(row, one, two):
    #print row[one], two
    return row[one] / two

#df = df[df['F-share'].notnull()]

def index_platform_gender(df):
    df['F-index'] = df.apply(index_count, one = 'F-share', two = df[df['F-share']!=0]['F-share'].mean(), axis=1)
    df['M-index'] = df.apply(index_count, one = 'M-share', two = df[df['M-share']!=0]['M-share'].mean(), axis=1)
    
    #df['Related Apps: F-share'] = df['Related Apps: F'] / (df['Related Apps: F'] + df['Related Apps: M'])
    df['Related Apps: F-index'] = df.apply(index_count, one = 'Related Apps: F-share', two = df[df['Related Apps: F-share']!=0]['Related Apps: F-share'].mean(), axis=1)
    df['Related Apps: M-index'] = df.apply(index_count, one = 'Related Apps: M-share', two = df[df['Related Apps: M-share']!=0]['Related Apps: M-share'].mean(), axis=1)
    
    return df

itunes = index_platform_gender(itunes)
android = index_platform_gender(android)


# In[345]:

itunes.columns.values


# In[346]:

def index_platform_age(df):
    ethnic = [ 'Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 
    
    for e in ethnic:
        res = e + '-index'
        o = e +'-share'
        df[res] = df.apply(index_count, one = o, two = df[df[o]!=0][o].mean(), axis=1)

    for e in ethnic:
        o = "Related Apps: " + e + "-share"
        res = "Related Apps: " + e + '-index'
        df[res] = df.apply(index_count, one = e, two = df[df[o]!=0][o].mean(), axis=1)
  
    return df


itunes = index_platform_age(itunes)
android = index_platform_age(android)


# In[347]:

android.to_csv('tmp\\a-sample.csv')
itunes.to_csv('tmp\\i-sample.csv')
# done index against platform


# In[348]:

itunes.columns.values


# In[349]:

# begin index against category
cats = itunes.groupby('category')


# In[350]:

def cat_count(row):
    return row[row>0].mean()


# In[351]:

categories = pd.DataFrame(index=cats.groups.keys())
categories


# In[352]:

#m = cats['F-index'].apply(cat_count)


categories['F-share'] = cats['F-share'].apply(cat_count)
categories['M-share'] = cats['M-share'].apply(cat_count)
categories['Related Apps: F-share'] = cats['Related Apps: F-share'].apply(cat_count)
categories['Related Apps: M-share'] = cats['Related Apps: M-share'].apply(cat_count)

ethnic = [ 'Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 
    
for e in ethnic:
    res = e + '-index'
    o = e +'-share'
    categories[o] = cats[o].apply(cat_count)

for e in ethnic:
    e = "Related Apps: " + e + "-share"
    res = e + '-index'
    categories[e] = cats[e].apply(cat_count)


# In[353]:

categories.columns
#categories[categories.index=='Books']['F-share'].values[0]


# In[354]:

def cat_find(row, index):
    #print "App:", row[index]
    #print "Category: \n", categories[categories.index==row['category']][index]
    result = row[index] / categories[categories.index==row['category']][index]
    if result.values:
        #print "result", result.values[0]
        return result.values[0]
    else:
        #print "-"
        return 0
    
    
def index_cat(df):
    df['F-index-cat'] = df.apply(cat_find, index='F-share', axis=1)#[itunes['category'] == 'Books']
    df['M-index-cat'] = df.apply(cat_find, index='M-share', axis=1)#[itunes['category'] == 'Books']
    df['Related Apps: F-index-cat'] = df.apply(cat_find, index='Related Apps: F-share', axis=1)#[itunes['category'] == 'Books']
    df['Related Apps: M-index-cat'] = df.apply(cat_find, index='Related Apps: M-share', axis=1)#[itunes['category'] == 'Books']

    ethnic = [ 'Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 
    
    for e in ethnic:
        res = e + '-index-cat'
        o = e +'-share'
        df[res] = df.apply(cat_find, index = o, axis=1)

    for e in ethnic:
        o = "Related Apps: " + e + "-share"
        res = "Related Apps: " + e + '-index-cat'
        df[res] = df.apply(cat_find, index = o, axis=1)
  
    return df    
 
itunes = index_cat(itunes)
android = index_cat(android)


# In[355]:

itunes.to_csv('itunes_master.csv')
android.to_csv('android_master.csv')


# In[356]:

itunes.to_csv('cats.csv')


# In[357]:

#index against both platforms
rows = [ 'M','F','Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 

final_rows = []

for r in rows:
    final_rows.append(r + '-share')
    final_rows.append('Related Apps: ' + r + '-share')
  
both_platforms_shares = pd.concat([android[final_rows],itunes[final_rows]])


# In[358]:

both_platforms_shares.to_csv('tmp/both_platforms.csv')


# In[359]:

def index_both_platform(df, both_shares):
    rows = [ 'M','F','Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 

    for e in rows:
        res = e + '-index-both'
        o = e +'-share'
        df[res] = df.apply(index_count, one = o, two = both_shares[both_shares[o]!=0][o].mean(), axis=1)

    for e in rows:
        o = "Related Apps: " + e + "-share"
        res = "Related Apps: " + e + '-index-both'
        df[res] = df.apply(index_count, one = o, two = both_shares[both_shares[o]!=0][o].mean(), axis=1)
  
    return df


itunes = index_both_platform(itunes,both_platforms_shares)
android = index_both_platform(android,both_platforms_shares)


# In[360]:

print android.columns.values


# In[361]:

itunes.to_csv('itunes_master.csv')
android.to_csv('android_master.csv')



# In[362]:

cols = "Publisher	Placement	AID	Publisher	URL	1 day avails	title	language	icon	category	developer	price	reviews count	content rating	brand score	release date	likely to be	top_free_rank	top_paid_rank	top_grossing_rank	top keywords title	top keywords description	top keywords description sip	top keywords review	top keywords review sip	M	F	Caucasian (white)	Middle Eastern	Native American	East Indian	African descent (black)	Asian	Pacific Islander	Latino / Hispanic	Related Apps	Related Apps Icons	Related Apps Categories	Related Apps SUB Categories	Related Apps: M	Related Apps: F	Related Apps: Caucasian (white)	Related Apps: Middle Eastern	Related Apps: Native American	Related Apps: East Indian	Related Apps: African descent (black)	Related Apps: Asian	Related Apps: Pacific Islander	Related Apps: Latino / Hispanic"
cols = cols.split('\t')
#cols = []
#those columns are in itunes, but not in android:
'''['installs',
 'sub categories',
 'Related Apps Name',
 'review rating',
 'id',
 'featured_rank']'''

cols_additional = ['installs',
 'sub categories',
 'Related Apps Name',
 'review rating',
 'id',
 'featured_rank']

rows = [ 'M','F','Caucasian (white)', 'Middle Eastern', 'Native American', 'East Indian', 'African descent (black)', 'Asian', 'Pacific Islander', 'Latino / Hispanic' ] 

for e in rows:
    ind = e + '-index'
    cat = e + '-index-cat'
    both = e + '-index-both'
    inds = e +'-share'
    
    cols.extend([inds,ind,cat,both])
    #print inds,ind,cat,both

for e in rows:
    e = "Related Apps: " + e
    ind = e + '-index'
    cat = e + '-index-cat'
    both = e + '-index-both'
    inds = e +'-share'
    cols.extend([inds,ind,cat,both])
    
    #print inds,ind,cat,both
print cols


# In[363]:

cols_final = list(  set(cols) - set(itunes.columns.values) )


# In[364]:

cols_final


# In[365]:

cols_android = []
cols_android.extend(cols)
cols_android.extend(cols_additional)

if set(cols_additional) <= set(android.columns.values):
    pass
else:
    for column in cols_additional:
        android[column] = np.nan
     
cols_itunes = []
cols_itunes.extend(cols)
cols_itunes.extend(cols_additional)

if set(cols_additional) <= set(itunes.columns.values):
    pass
else:
    for column in cols_additional:
        itunes[column] = np.nan


# In[366]:

itunes[cols_additional].head()


# In[367]:

itunes.to_csv('itunes_master_cols.csv', cols = cols_android)
android.to_csv('android_master_cols.csv', cols = cols_itunes)



# In[368]:

pd.version.version

