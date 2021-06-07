import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import cdist
import math
import requests
import json



adp_column = 'Dynasty SF ADP'
  

df = pd.read_excel('rankings.xlsx')
df = df.sort_values('avg')
dataframe = df
X = dataframe[['avg']]

distortions = []
inertias = []
mapping1 = {}
mapping2 = {}

K = range(1, 49)      
 
for k in K:
    # Building and fitting the model
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)
    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X.shape[0])
    inertias.append(kmeanModel.inertia_)
 
    mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                           'euclidean'), axis=1)) / X.shape[0]
    mapping2[k] = kmeanModel.inertia_

distortions_diff = []
for i in range(len(distortions)-1):
    distortions_diff.append(distortions[i] - distortions[i+1])

distortions_change = []
for i in range(len(distortions_diff)-1):
    distortions_change.append(distortions_diff[i] / distortions_diff[i+1])

distortions_k_value = 0
for i in range(len(distortions_change)):
    if distortions_change[i] > 2:
        distortions_k_value = i + 1
    
inertias_diff = []
for i in range(len(inertias)-1):
    inertias_diff.append(inertias[i] - inertias[i+1])
    
inertias_change = []
for i in range(len(inertias_diff)-1):
    inertias_change.append(inertias_diff[i] / inertias_diff[i+1])
    
inertias_k_value = 0
for i in range(len(inertias_change)):
    if inertias_change[i] > 2:
        inertias_k_value = i + 1
        
k_value = int((distortions_k_value + inertias_k_value)/2)
  
if k_value < 25:
    k_value = 25

kmeans = KMeans(n_clusters=k_value, max_iter=600, algorithm = 'auto') # You want cluster the passenger records into 2: Survived or Not survived
scaler = MinMaxScaler()
#X_scaled = scaler.fit_transform(X)
#kmeans.fit(X_scaled)
kmeans.fit(X)

dataframe['tier'] = dataframe[['avg']].apply(lambda x: kmeans.predict(np.array(x).reshape(-1, len(np.array(x)))), axis=1)
dataframe['tier'] = dataframe['tier'].astype(str)
tier = 0
for i in dataframe['tier'].drop_duplicates().to_list():
    dataframe['tier'][dataframe['tier'] == i] = tier
    tier += 1
    
colors_unique = len(dataframe['tier'].drop_duplicates())
colors=['indianred', 'mediumseagreen', 'orchid', 'cornflowerblue', 'palevioletred', 'mediumpurple']
color_len = len(colors)
color_mult = int(math.ceil(colors_unique / color_len))
colors = colors * color_mult
colors = colors[:colors_unique]
color_dict = {}
dataframe['tier'] = dataframe['tier'].astype(str)
for i in range(len(dataframe['tier'].drop_duplicates().to_list())):
    color_dict[dataframe['tier'].drop_duplicates().to_list()[i]] = colors[i]
dataframe['colors'] = dataframe['tier'].apply(lambda x: color_dict[x])

sleeper = pd.DataFrame(json.loads(requests.get('https://api.sleeper.app/v1/players/nfl').text))
sleeper = sleeper.transpose()
sleeper = sleeper[['full_name', 'position', 'player_id', 'team']]
dataframe['player_merge'] = dataframe['player'].str.lower().str.replace('.', '').str.strip()
sleeper['player_merge'] = sleeper['full_name'].str.lower().str.replace('.', '').str.strip()

def remove_suffix(x):
    try:
        x = x.split()
        x = x[0] + ' ' + x[1]
        return x
    except:
        return x
    
dataframe['player_merge'] = dataframe['player_merge'].apply(lambda x: remove_suffix(x))
sleeper['player_merge'] = sleeper['player_merge'].apply(lambda x: remove_suffix(x))

dataframe['team'][dataframe['team'] == 'JAC'] = 'JAX'

sleeper['player_merge'][sleeper['player_merge'] == 'scott miller'] = 'scotty miller'
sleeper['player_merge'][sleeper['player_merge'] == 'christopher herndon'] = 'chris herndon'
sleeper['player_merge'][sleeper['player_merge'] == 'jeffery wilson'] = 'jeff wilson'

dataframe = pd.merge(dataframe, sleeper[['position', 'player_id', 'team', 'player_merge', 'full_name']], how='left', on=['player_merge', 'team'])
dataframe = pd.merge(dataframe, sleeper[['position', 'player_id', 'team', 'player_merge', 'full_name']], how='left', on=['player_merge'])

dataframe = dataframe[~dataframe['position_x'].isin(['OG', 'CB', 'G', 'DE', 'LB', 'SS'])]
dataframe = dataframe[~dataframe['position_y'].isin(['OG', 'CB', 'G', 'DE', 'LB', 'SS'])]

dataframe['position'] = dataframe.apply(lambda x: x['position_x'] if pd.isnull(x['position_x']) == False else x['position_y'], axis=1)
dataframe['player_id'] = dataframe.apply(lambda x: x['player_id_x'] if pd.isnull(x['player_id_x']) == False else x['player_id_y'], axis=1)
dataframe['full_name'] = dataframe.apply(lambda x: x['full_name_x'] if pd.isnull(x['full_name_x']) == False else x['full_name_y'], axis=1)
dataframe['team'] = dataframe['team_x']

dataframe = dataframe.drop_duplicates()
dataframe = dataframe[(dataframe['player'] != 'Alex Smith ') | (dataframe['position'] != 'TE')]

adp = pd.read_excel('sleeper ADP.xlsx', header=1)
adp = adp.rename(columns = {adp_column:'adp', 'Player Team':'team', 'Player First Name':'first_name', 'Player Last Name':'last_name', 'Player Fantasy Positions':'position', 'Sleeper ID':'sleeper_id'})
adp['player'] = adp['first_name'] + ' ' + adp['last_name']

adp['player_merge'] = adp['player'].str.lower().str.replace('.', '').str.strip()
adp['player_merge'] = adp['player_merge'].apply(lambda x: remove_suffix(x))

adp['player_merge'][adp['player_merge'] == 'scott miller'] = 'scotty miller'
adp['player_merge'][adp['player_merge'] == 'christopher herndon'] = 'chris herndon'
adp['player_merge'][adp['player_merge'] == 'jeffery wilson'] = 'jeff wilson'

dataframe = pd.merge(dataframe, adp[['adp', 'player_merge', 'team']], how='left', on=['player_merge', 'team'])
dataframe = pd.merge(dataframe, adp[['adp', 'player_merge']], how='left', on=['player_merge'])

dataframe['adp'] = dataframe.apply(lambda x: x['adp_x'] if pd.isnull(x['adp_x']) == False else x['adp_y'], axis=1)
  

dataframe = dataframe[['rank', 'full_name', 'team', 'best', 'worst', 'avg', 'stddev', 'tier', 'colors', 'position', 'player_id', 'adp']]
dataframe = dataframe.rename(columns={'full_name':'player'})
dataframe['rank_diff'] = dataframe['worst'] - dataframe['best']
dataframe['avg_plot'] = dataframe['avg'] - .5
dataframe['value'] = dataframe['avg'] - dataframe['adp']
dataframe['value'] = dataframe['value'].round(2)
dataframe['pick'] =  dataframe['adp']

dataframe = dataframe.drop_duplicates()
dataframe = dataframe[(dataframe['player'] != 'Alex Smith ') | (dataframe['position'] != 'TE')]

with pd.ExcelWriter('draft_tiers.xlsx') as writer:  
    dataframe.to_excel(writer, sheet_name='all_players', index=False)
    


