# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

__author__ = 'IGOR'
import pandas as pd
raw_data = pd.read_csv('trajectory_data_sample.csv')



# <codecell>

from datetime import datetime

# <codecell>


def get_timestamp(row):
    return datetime.strptime(row, '%d.%m.%Y %H:%M')

import numpy as np

raw_data['timestamp'] = raw_data['date_event'].apply( get_timestamp ) 

raw_data['delta'] = (raw_data['timestamp'] - raw_data['timestamp'].shift(1).fillna(0).astype('datetime64[ns]'))

# <codecell>

raw_data.delta = raw_data.delta / 1e9

# <codecell>

raw_data['is_session'] = ( raw_data.delta < 60*10 ) # consider session, if there is less then 10 minutes of break between events

# <codecell>

raw_data

# <codecell>

row_iterator = raw_data.iterrows()
 # take first item from row_iterator

    
last = row_iterator.next()
#print "lst", last
'''
for row in row_iterator:
    print "row", row[0]
    #last = row
    print "last", last[0]
    last = row
'''

session_list = [0]
session_id = 0
is_click = []
for row in row_iterator:
    next = row[1][['is_session','event']]
     
    #print "current:", curr
    #print last[1]
    
    curr = last[1][['is_session','event']]
    #print next['event']
    #print "next:", next
    if curr['is_session']:
        if next['is_session']:
            pass
        else:
            session_id +=1
    else:
        if next['is_session']:
            pass
        else:
            session_id +=1
    session_list.append(session_id)        
    
    #print "events " + curr['event'] + ' ' + next['event']
    
    if curr['event'] == 'visit':
        #print next['event']
        if next['event'] == 'click':
            is_click.append(1)
            #print curr,'visit+click'
        else:
            is_click.append(0)
    else:
        is_click.append(0)
    last = row        
    

is_click.append(0)

# <codecell>

len(is_click)
#len(session_list)
raw_data['session_id'] = session_list
raw_data['is_click'] = is_click

# <codecell>

processed_data = raw_data[raw_data.event != "click"]

# <codecell>

processed_data = pd.concat([processed_data, pd.get_dummies(processed_data['channel'])],axis=1) # transform category column into binary variables

# <codecell>

#print raw_data[['date_event','event','session_id', 'is_click']]
''' add columns:
aggregate by user:
amount of visits by channel type
amount of clicks by channel type

aggregate by session:
amount of visits by channel type
amount of clicks by channel type

'''

# <codecell>

processed_data

# <codecell>

# columns (sum of visits by each column):
# Direct Access, Other etc.
# sum of "is_click"
# add columns to main DF with this information
# by cust_id, by is_session
channels = ['Direct Access', 'Other', 'is_click'] 

session_data = processed_data.groupby('session_id').sum()[channels]
user_data = processed_data.groupby('cust_id').sum()[channels]# columns (sum of visits by each column):
# Direct Access, Other etc.
# sum of "is_click"
# add columns to main DF with this information
# by cust_id, by is_session
channels = ['Direct Access', 'Other', 'is_click'] 

session_data = processed_data.groupby('session_id').sum()[channels]
user_data = processed_data.groupby('cust_id').sum()[channels]

# <codecell>

session_data.columns = ["Session-"+x for x in channels]
user_data.columns = ["User-"+x for x in channels]

# <codecell>

processed_data = processed_data.merge(user_data, left_on='cust_id', right_index=True)

# <codecell>

processed_data = processed_data.merge(session_data, left_on='session_id', right_index=True)

# <codecell>

processed_data.to_csv('processed_data.csv')

# <codecell>

train_data = processed_data[['is_click','Direct Access','Other','User-Direct Access',
    'User-Other','User-is_click','Session-Direct Access','Session-Other','Session-is_click']] #'cust_id','session_id',

# <codecell>

train_data

# <codecell>

import numpy as np

# <codecell>

data = np.array(train_data)
data.shape

# <codecell>

Y = data[:,[0]]
X = data[:,1:]

# <codecell>

from sklearn.cross_validation import train_test_split,cross_val_score
from sklearn.linear_model import LogisticRegression
train_X, test_X, train_Y, test_Y = train_test_split(X,Y, test_size=0.33, random_state=42)


# <codecell>

est = LogisticRegression()
scores = cross_val_score(est, train_X, train_Y, cv=5)
#cross_val_score

# <codecell>

scores

est.fit(train_X, train_Y)
est.predict(test_X)

# <codecell>


# <codecell>

raw_data.to_csv('result_data.csv')

