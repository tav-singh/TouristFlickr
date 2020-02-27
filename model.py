#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy
 
df = pd.read_csv("flickr_sample.csv")
#print(df)


# In[64]:


import warnings
warnings.filterwarnings("ignore")


# In[75]:


#currently only focus on photos with the following tags : travel, nature, beach, museum, wildlife, landscape

nature_df=df[df['tags'].str.contains('nature')]#30
nature_df['group']='nature'
travel_df=df[df['tags'].str.contains('travel')]#41
travel_df['group']='travel'
beach_df=df[df['tags'].str.contains('beach')]#24
beach_df['group']='beach'
museum_df=df[df['tags'].str.contains('museum')]#17
museum_df['group']='museum'
wildlife_df=df[df['tags'].str.contains('wildlife')]#13
wildlife_df['group']='wildlife'
landscape_df=df[df['tags'].str.contains('landscape')]#11
landscape_df['group']='landscape'


# In[76]:


#print(len(wildlife_df))


# In[77]:


#calculate popularity score for each group
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler()#scale counts of views and comments to the [0,1] range

nature_df['norm_views']=min_max_scaler.fit_transform(nature_df['views'].values.reshape(-1,1))
nature_df['norm_comments']=min_max_scaler.fit_transform(nature_df['comments'].values.reshape(-1,1))

nature_df['popularity_score']=0.5*nature_df['norm_comments']+0.5*nature_df['norm_views']

print(nature_df[['views','norm_views','comments','norm_comments','popularity_score']].sort_values('popularity_score', ascending=False))


# In[78]:


travel_df['norm_views']=min_max_scaler.fit_transform(travel_df['views'].values.reshape(-1,1))
travel_df['norm_comments']=min_max_scaler.fit_transform(travel_df['comments'].values.reshape(-1,1))
travel_df['popularity_score']=0.5*travel_df['norm_comments']+0.5*travel_df['norm_views']
beach_df['norm_views']=min_max_scaler.fit_transform(beach_df['views'].values.reshape(-1,1))
beach_df['norm_comments']=min_max_scaler.fit_transform(beach_df['comments'].values.reshape(-1,1))
beach_df['popularity_score']=0.5*beach_df['norm_comments']+0.5*beach_df['norm_views']
museum_df['norm_views']=min_max_scaler.fit_transform(museum_df['views'].values.reshape(-1,1))
museum_df['norm_comments']=min_max_scaler.fit_transform(museum_df['comments'].values.reshape(-1,1))
museum_df['popularity_score']=0.5*museum_df['norm_comments']+0.5*museum_df['norm_views']
wildlife_df['norm_views']=min_max_scaler.fit_transform(wildlife_df['views'].values.reshape(-1,1))
wildlife_df['norm_comments']=min_max_scaler.fit_transform(wildlife_df['comments'].values.reshape(-1,1))
wildlife_df['popularity_score']=0.5*wildlife_df['norm_comments']+0.5*wildlife_df['norm_views']
landscape_df['norm_views']=min_max_scaler.fit_transform(landscape_df['views'].values.reshape(-1,1))
landscape_df['norm_comments']=min_max_scaler.fit_transform(landscape_df['comments'].values.reshape(-1,1))
landscape_df['popularity_score']=0.5*landscape_df['norm_comments']+0.5*landscape_df['norm_views']


# In[79]:


#write new datasframes into csv file
f='ranked_flickr_sample.csv'
nature_df.sort_values('popularity_score', ascending=False).to_csv(f,index=False)
travel_df.sort_values('popularity_score', ascending=False).to_csv(f, mode='a', header=False,index=False)
beach_df.sort_values('popularity_score', ascending=False).to_csv(f, mode='a', header=False,index=False)
museum_df.sort_values('popularity_score', ascending=False).to_csv(f, mode='a', header=False,index=False)
wildlife_df.sort_values('popularity_score', ascending=False).to_csv(f, mode='a', header=False,index=False)
landscape_df.sort_values('popularity_score', ascending=False).to_csv(f, mode='a', header=False,index=False)
pd.read_csv(f)


# In[ ]:


#calculate a popularity score for a place if multiple groups are selected
    

