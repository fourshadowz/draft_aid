import requests
import json
import pandas as pd

response = requests.get(url='https://keeptradecut.com/dynasty-rankings#').text
response = response.split('var playersArray = ')
response = response[1]
response = response .split('		var ')
response = response[0]
response1 = response[:len(response)-2]
response_json = json.loads(response1)
response_df = pd.DataFrame(response_json)
superflex_value = pd.DataFrame.from_dict(response_df['superflexValues'].to_list())


keeptradecut_rank = pd.concat([response_df[['playerName', 'position', 'team', 'rookie', 'age', 'seasonsExperience']], superflex_value[['value', 'rank']]], axis=1)

team_rename = {'KCC':'KC',
                'JAC':'JAX',
                'NOS':'NO',
                'GBP':'GB',
                'SFO':'SF',
                'LVR':'LV',
                'TBB':'TB',
                'NEP':'NE'}
keeptradecut_rank['team'] = keeptradecut_rank['team'].apply(lambda x: team_rename[x] if x in team_rename.keys() else x)
keeptradecut_rank['drop'] = keeptradecut_rank['playerName'].apply(lambda x: x[:4].isdigit())
keeptradecut_rank = keeptradecut_rank[keeptradecut_rank['drop'] == False]

keeptradecut_rank['best'] = keeptradecut_rank['rank'] - 1
keeptradecut_rank['worst'] = keeptradecut_rank['rank'] + 1
keeptradecut_rank['avg'] = keeptradecut_rank['rank']
keeptradecut_rank['stddev'] = 1

keeptradecut_rank = keeptradecut_rank.rename(columns={'playerName':'player'})



keeptradecut_rank.to_excel('dynasty_trade_value.xlsx', index=False)
keeptradecut_rank[['rank', 'player', 'team', 'best', 'worst', 'avg', 'stddev']].to_excel('rankings.xlsx', index=False)
