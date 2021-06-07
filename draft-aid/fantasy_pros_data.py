import requests
from bs4 import BeautifulSoup
import pandas as pd


url_dict = {
'pat_fitz' : 'https://www.fantasypros.com/nfl/rankings/pat-fitzmaurice.php?type=dynasty&scoring=PPR&position=OP',
'dan_harris' : 'https://www.fantasypros.com/nfl/rankings/dan-harris.php?type=dynasty&scoring=PPR&position=OP',
'mike_tag' : 'https://www.fantasypros.com/nfl/rankings/mike-tagliere.php?type=dynasty&scoring=PPR&position=OP',
'rich_pizza' : 'https://www.fantasypros.com/nfl/rankings/rich-piazza-fantasy-shed.php?type=dynasty&scoring=PPR&position=OP',
'kyle_yates' : 'https://www.fantasypros.com/nfl/rankings/kyle-yates.php?type=dynasty&scoring=PPR&position=OP',
'mario_gut' : 'https://www.fantasypros.com/nfl/rankings/mauricio-gutierrez.php?type=dynasty&scoring=PPR&position=OP',
'fran_romero' : 'https://www.fantasypros.com/nfl/rankings/francisco-(chato)-romero.php?type=dynasty&scoring=PPR&position=OP',
'branden_much' : 'https://www.fantasypros.com/nfl/raon-murnkings/brandchison.php?type=dynasty&scoring=PPR&position=OP',
'joe_pep' : 'https://www.fantasypros.com/nfl/rankings/joe-pisapia.php?type=dynasty&scoring=PPR&position=OP',
}

all_rankings = pd.DataFrame()

for pro in url_dict:
    try:
        response = requests.get(url_dict[pro]).text
        
        soup = BeautifulSoup(response)
        
        table = soup.find_all('td')    
        table[0].text
        
        ranks = []
        count = 0
        player = []
        
        for i in range(len(table)):
            text = table[i].text
            if count == 6:
                ranks.append(player) 
                player=[]
                count=0
            player.append(text)
            count += 1
            
        df = pd.DataFrame(ranks, columns = ['rank', 'player', 'team', 'bye', 'ecr', 'vs_ecr'])
        df['pro'] = pro
        all_rankings = pd.concat([all_rankings, df], axis=0)
    except:
        print(pro + ' rankings failed to read')

all_rankings['rank'] = all_rankings['rank'].astype(int)

rank_min = all_rankings[['player', 'rank', 'team']].groupby(['player', 'team']).min()
rank_max = all_rankings[['player', 'rank', 'team']].groupby(['player', 'team']).max()
rank_mean = all_rankings[['player', 'rank', 'team']].groupby(['player', 'team']).mean()

rank_std = all_rankings[['player', 'rank', 'team']].groupby(['player', 'team']).std()

df_rankings = pd.concat([rank_min, rank_max, rank_mean, rank_std], axis=1)
df_rankings = df_rankings.reset_index()
df_rankings.columns = ['player', 'team', 'best', 'worst', 'avg', 'stddev']
df_rankings = df_rankings.sort_values('avg')
df_rankings = df_rankings.reset_index(drop=True)
df_rankings = df_rankings.reset_index()
df_rankings = df_rankings.rename(columns={'index':'rank'})
df_rankings['rank'] = df_rankings['rank'] + 1

df_rankings.to_excel('rankings.xlsx', index=False)

