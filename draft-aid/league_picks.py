import requests
import json
import pandas as pd

league_id = 688639493300912128
users_in_league = f'https://api.sleeper.app/v1/league/{league_id}/users'

users_response = requests.get(users_in_league)
users_response = json.loads(users_response.text)
users_response = pd.DataFrame(users_response)

df_users = users_response
df_drafts = pd.DataFrame()
df_picks = pd.DataFrame()

for user_id in users_response['user_id']:
    draft_by_user = f'https://api.sleeper.app/v1/user/{user_id}/drafts/nfl/2021'
    drafts_response = requests.get(draft_by_user)
    drafts_response = json.loads(drafts_response.text)
    drafts_response = pd.DataFrame(drafts_response)
    drafts_response['user_id'] = user_id
    df_drafts = pd.concat([df_drafts, drafts_response], axis=0)
    
    
df_drafts['teams'] = df_drafts['settings'].apply(lambda x: x['teams'])
df_drafts['format'] = df_drafts['metadata'].apply(lambda x: x['scoring_type'])
df_drafts = df_drafts[['user_id', 'draft_id', 'teams', 'format']]
    
for i in enumerate(df_drafts.index):
    draft_id = df_drafts['draft_id'].iloc[i[0]]
    user_id = df_drafts['user_id'].iloc[i[0]]
    draft_picks = f'https://api.sleeper.app/v1/draft/{draft_id}/picks'
    drafts_picks_response = requests.get(draft_picks)
    drafts_picks_response = json.loads(drafts_picks_response.text)
    drafts_picks_response = pd.DataFrame(drafts_picks_response)
    drafts_picks_response['draft_id'] = draft_id
    drafts_picks_response['user_id'] = user_id
    df_picks = pd.concat([df_picks, drafts_picks_response], axis=0)



df_picks = df_picks[df_picks['user_id'] == df_picks['picked_by']]
df_picks = df_picks[['draft_id', 'round', 'player_id', 'pick_no', 'user_id']]
df_picks = pd.merge(df_picks, df_drafts[['draft_id', 'teams', 'format']], how='left', on='draft_id')
df_picks = pd.merge(df_picks, df_users[['user_id', 'display_name']], how='left', on='user_id')

sleeper = pd.DataFrame(json.loads(requests.get('https://api.sleeper.app/v1/players/nfl').text))
sleeper = sleeper.transpose()

df_picks = pd.merge(df_picks, sleeper[['full_name', 'player_id', 'position']], how='left', on='player_id')
df_picks.to_excel('league_picks.xlsx', index=False)
