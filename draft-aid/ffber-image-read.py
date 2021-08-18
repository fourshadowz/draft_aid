import cv2
import pytesseract
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = cv2.imread('ffbers-add-tier.png')
text = pytesseract.image_to_string(img)

text_list = text.split('\n')

positions = ['Quarterbacks', 'Running Backs', 'Wide Receivers', 'Tight Ends', 'Defense', 'Kickers']
for i in positions:
    if i in text_list:
        print(i)
 
text_list = [x for x in text_list if x.strip() != '']
    
for i in enumerate(text_list):
    if i[1] in positions:
        tier = 0
        position = i[1]
    elif i[1].strip() == 'Tier':
        tier += 1
        text_list[i[0]] = 'Tier ' + str(tier)
    else:
        text_list[i[0]] = [i[1], tier, position]
    
text_list = [x for x in text_list if isinstance(x, list) == True]
df = pd.DataFrame(text_list, columns=['player', 'tier', 'position'])
df['player'] = df['player'].str.split().str[1:-1]
df['team'] = df['player'].str[-1]
df['player'] = df['player'].str[:-1].str.join(' ')

positions_keep = {'Quarterbacks':'QB', 'Running Backs':'RB', 'Wide Receivers':'WR', 'Tight Ends':'TE'}
df = df[df['position'].isin(positions_keep.keys())]
df['position'] = df['position'].apply(lambda x: positions_keep[x])


clean_names = {'Hockenson':'T.J. Hockenson'
,'Dobbins':'J.K. Dobbins'
,'Williams':'Javonte Williams'
,'McCaffrey':'Christian McCaffrey'
,'Jefferson':'Justin Jefferson'
,'A. Robinson II':'Allen Robinson'
,'C. Edwards-Helaire':'Clyde Edwards-Helaire'
,'J. Smith-Schuster':'JuJu Smith-Schuster'
,'D. Montgomery':'David Montgomery'
,'M. Stafford':'Matthew Stafford'
,'D. Henderson Jr.':'Darrell Henderson'
,'C. Sutton':'Courtland Sutton'
,'0. Beckham Jr.':'Odell Beckham'
,'R. Fitzpatrick':'Ryan Fitzpatrick'
,'0.J. Howard':'O.J. Howard'
,'B. Roethlisberger':'Ben Roethlisberger'
,'Etienne Jr.':'Travis Etienne'
,'W. Fuller V':'Will Fuller'
,'M. Pittman Jr.':'Michael Pittman'
,'L. Shenault Jr.':'Laviska Shenault'
,'E. Sanders':'Emmanuel Sanders'
,'S. Shepard':'Sterling Shepard'
,'M. Jones Jr.':'Marvin Jones'
,'B. Perriman':'Breshad Perriman'
,'M. Gordon III':'Melvin Gordon'
,'T. Bridgewater':'Teddy Bridgewater'
,"Tre’'Quan Smith":"Tre'Quan Smith"
,'Marshall Jr.':'Terrace Marshall'
,'L. Fournette':'Leonard Fournette'
,'J. Williams':'Jamaal Williams'
,'D. Singletary':'Devin Singletary'
,'M. Valdes-Scantling':'Marquez Valdes-Scantling'
,'R. St. Brown':'Amon-Ra St. Brown'
,'R. Stevenson':'Rhamondre Stevenson'
,'A. Mattison':'Alexander Mattison'
,'K. Gainwell':'Kenneth Gainwell'
}

df['player'] = df['player'].apply(lambda x: clean_names[x] if x in clean_names.keys() else x)

df = df.sort_values('tier')
df = df[['player', 'team', 'tier', 'tier', 'tier']]
df.columns = ['player', 'team', 'best', 'worst', 'avg']
df['stddev'] = 1

df.to_excel('rankings.xlsx', index=False)
