#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import math
import requests
import pandas as pd
import json
from collections import Counter

app = dash.Dash(__name__)
app.title = "Draft Things"

position_select = 'SFLEX'
my_username = ''
draft_id = ''
players_all = pd.DataFrame(columns = ['player', 'tier', 'value', 'pick', 'rank_diff', 'best', 'avg_plot', 'colors', 'adp'])
players_rb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_qb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_wr = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_te = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
players_flex = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
next_round = pd.DataFrame(columns = ['pick', 'user_name', 'pick_players', 'round_players', 'pick_position', 'round_position'])
players_drafted = pd.DataFrame(columns=['player', 'tier', 'player_id'])

players_all_initial = pd.read_excel('draft_tiers.xlsx')
my_guys = pd.read_excel('my_guys.xlsx')
league_picks = pd.read_excel('league_picks.xlsx')
league_picks['user_id'] = league_picks['user_id'].astype(str)
players_all_initial['player'][players_all_initial['player'].isin(my_guys['player'].to_list())] = '****   ' + players_all_initial['player'] + '  ****'
league_users = league_picks[['user_id', 'display_name']].drop_duplicates()
unique_colors = players_all_initial[['tier', 'colors']].drop_duplicates()
 

app.layout = html.Div([
dcc.Interval(id = 'data-update', interval = 10000, n_intervals = 0),

html.Div([
    
html.Div([
dcc.RadioItems(id='radio-button-position',
options=[{'label': 'SFLEX', 'value': 'SFLEX'},
         {'label': 'FLEX', 'value': 'FLEX'},
         {'label': 'QB', 'value': 'QB'},
         {'label': 'RB', 'value': 'RB'},
         {'label': 'WR', 'value': 'WR'},
         {'label': 'TE', 'value': 'TE'}],
value='SFLEX')],style={'display': 'inline-block', "margin-left": "200px", "margin-top": "50px", "verticalAlign": "top"}),

html.Div([
dcc.Input(
id="input-draft-id",
type="text",
style={'height': '50px','width': '500px', 'textAlign': 'center'},
placeholder="Sleeper Draft ID Hurr")
],style={'display': 'inline-block', "margin-left": "350px", "margin-top": "50px", "verticalAlign": "top"}),

html.Div([
dcc.Input(
id="input-username",
type="text",
style={'height': '50px','width': '500px', 'textAlign': 'center'},
placeholder="Sleeper Username Hurr")
],style={'display': 'inline-block', "margin-left": "200px", "margin-top": "50px", "verticalAlign": "top"})
    
]),

html.Div([

    html.Div([   
    dcc.Graph(id='graph')
    ],style={'display': 'inline-block', "margin-right": "15px"}),
    
    
    html.Div([
        
        html.Div([
        html.Label("ALL"),
        dash_table.DataTable(
        id='table_players_all',
        columns=[{"name": i, "id": i} for i in ['player', 'tier']],
        data=players_all.iloc[:41][['player', 'tier']].to_dict('records'),
        style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                               [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors['colors'][unique_colors['tier'] == i].iloc[0], 'color': 'white'} for i in unique_colors['tier'].tolist()]),           
        style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},),    
        ],style={'display': 'inline-block', "margin-right": "15px", "margin-top": "110px", "verticalAlign": "top"}),
        
        html.Div([
        
            html.Div([
        
                html.Div([
                html.Label("RB"),
                dash_table.DataTable(
                id='table_players_rb',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_rb.iloc[:20][['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors['colors'][unique_colors['tier'] == i].iloc[0], 'color': 'white'} for i in unique_colors['tier'].tolist()]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
                style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
                
                html.Div([
                html.Label("WR"),
                dash_table.DataTable(
                id='table_players_wr',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_wr.iloc[:20][['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors['colors'][unique_colors['tier'] == i].iloc[0], 'color': 'white'} for i in unique_colors['tier'].tolist()]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
                style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
            
            ]),
             
            html.Div([
            
                html.Div([
                html.Label("QB"),
                dash_table.DataTable(
                id='table_players_qb',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_qb.iloc[:20][['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] +
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors['colors'][unique_colors['tier'] == i].iloc[0], 'color': 'white'} for i in unique_colors['tier'].tolist()]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],      
                style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
                
                html.Div([
                html.Label("TE"),
                dash_table.DataTable(
                id='table_players_te',
                columns=[{"name": i, "id": i} for i in ['player', 'tier']],
                data=players_te.iloc[:20][['player', 'tier']].to_dict('records'),
                style_data_conditional=([{'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}] + 
                                       [{'if': {'filter_query': '{{tier}} = {}'.format(i), 'column_id': ['player', 'tier']}, 'background-color': unique_colors['colors'][unique_colors['tier'] == i].iloc[0], 'color': 'white'} for i in unique_colors['tier'].tolist()]),           
                style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'tier'},'width': '75px'}],
                style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},),
                ],style={'display': 'inline-block', "margin-right": "15px"}),
                
            ]),
            
        ],style={'display': 'inline-block', "margin-top": "100px", "verticalAlign": "top"}),
            
        html.Div([
        html.Label("VALUE"),
        dash_table.DataTable(
        id='table_players_value',
        columns=[{"name": i, "id": i} for i in ['player', 'value', 'pick']],
        data=players_all.iloc[:50][['player', 'value', 'pick']][players_all['value'] < -5].iloc[:41].to_dict('records'),
        style_data_conditional=[{'if': {'column_id': ['player', 'value', 'pick']},'backgroundColor': 'mediumseagreen','color': 'white'},
                                {'if': {'filter_query': '{pick} > 12','column_id': ['player', 'value', 'pick']},'backgroundColor': 'goldenrod','color': 'white'},
                                {'if': {'filter_query': '{pick} > 24','column_id': ['player', 'value', 'pick']},'backgroundColor': 'indianred','color': 'white'},
                                {'if': {'filter_query': '{player} contains "*"','column_id': ['player']},'textAlign': 'left'}],           
        style_cell_conditional=[{'if': {'column_id': 'player'}, 'width': '200px'}, {'if': {'column_id': 'pick'},'width': '75px'}, {'if': {'column_id': 'value'},'width': '75px'}],
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},),
        ],style={'display': 'inline-block', "margin-right": "15px", "margin-top": "110px", "verticalAlign": "top"})
    
    ],style={'display': 'inline-block', "verticalAlign": "top"}),
    
]),
    
    html.Div([
        
        html.Div([
        html.Label("USER"),
        dash_table.DataTable(
        id='table_league_pick_user',
        columns=[{"name": i, "id": i} for i in ['pick', 'user_name']],
        data=next_round[['pick', 'user_name']].to_dict('records'),        
        style_cell_conditional=[{'if': {'column_id': 'user_name'}, 'width': '150px'},  
                                {'if': {'column_id': 'pick'},'width': '50px'}],
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'color' : 'black'},
        style_cell={'backgroundColor': 'rgb(229,236,246)', 'color': 'black'}),
        ],style={'display': 'inline-block',"margin-left": "50px", "verticalAlign": "top"}),
        
        html.Div([
        html.Label("LEAGUE PICK PLAYERS"),
        dash_table.DataTable(
        id='table_league_pick_players',
        columns=[{"name": i, "id": i} for i in ['pick_players', 'round_players']],
        data=next_round[['pick_players', 'round_players']].to_dict('records'),        
        style_cell_conditional=[{'if': {'column_id': 'pick_players'},'width': '500px'}, 
                                {'if': {'column_id': 'round_players'},'width': '500px'}],
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'color' : 'black'},
        style_cell={'backgroundColor': 'rgb(229,236,246)', 'color': 'black'}),
        ],style={'display': 'inline-block',"margin-left": "50px", "verticalAlign": "top"}),
        
        html.Div([
        html.Label("LEAGUE PICK POSITION"),
        dash_table.DataTable(
        id='table_league_pick_position',
        columns=[{"name": i, "id": i} for i in ['pick_position', 'round_position']],
        data=next_round[['pick_position', 'round_position']].to_dict('records'),        
        style_cell_conditional=[ {'if': {'column_id': 'pick_position'},'width': '200px'}, 
                                {'if': {'column_id': 'round_position'},'width': '200px'}],
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold', 'color' : 'black'},
        style_cell={'backgroundColor': 'rgb(229,236,246)', 'color': 'black'}),
        ],style={'display': 'inline-block', "margin-left": "50px", "margin-right": "15px", "verticalAlign": "top"})
        
    ],style={'display': 'inline-block', "margin-top": "50px", "margin-bottom": "200px"}),

    dcc.Store(id='json-data')
    
])

@app.callback(dash.dependencies.Output('json-data', 'data'), [dash.dependencies.Input('data-update', 'n_intervals'), dash.dependencies.Input('input-draft-id', 'value'), dash.dependencies.Input('input-username', 'value')])
def clean_data(value, draft_id, my_username):
     # some expensive clean data step
    

    try:

        draft_info_url = f'https://api.sleeper.app/v1/draft/{draft_id}'
        response = json.loads(requests.get(draft_info_url).text)
        draft_teams = response['settings']['teams']
        draft_rounds = response['settings']['rounds']
        draft_format = response['metadata']['scoring_type']
        draft_order = response['draft_order']
        draft_reversal = response['settings']['reversal_round']
        
        inv_map_draft_order = {v: k for k, v in draft_order.items()}
        cpu_number = 0
        for i in range(draft_teams):
            if i+1 not in inv_map_draft_order.keys():
                inv_map_draft_order[i+1] = 'cpu' + str(cpu_number)
                cpu_number += 1
                
        draft_order_picks = []
        reverse = False
        for i in range(draft_rounds):
            if reverse == False:
                for j in range(1,draft_teams+1):
                    draft_order_picks.append(inv_map_draft_order[j])
            else:
                for j in list(range(1,draft_teams+1))[::-1]:
                    draft_order_picks.append(inv_map_draft_order[j])
        
            if i == draft_reversal-2: 
                reverse = True
            else:
                reverse = not reverse    
            
        draft_order_picks = pd.DataFrame(draft_order_picks, index=range(len(draft_order_picks)))
        draft_order_picks = draft_order_picks.reset_index()
        draft_order_picks.columns = ['pick', 'user_id']
        draft_order_picks['pick'] = draft_order_picks['pick'] + 1  
        global league_picks
        league_picks = league_picks[league_picks['teams'] == draft_teams]
        league_picks = league_picks[league_picks['format'] == draft_format]
        
        draft_order_picks = pd.merge(draft_order_picks, league_users, how='left', on='user_id')
        draft_order_picks = draft_order_picks.rename(columns={'display_name':'user_name'})
        
        draft_order_picks['3_pick_spread'] = draft_order_picks.apply(lambda x: league_picks['full_name'][(league_picks['user_id'] == x['user_id']) & (league_picks['pick_no'].isin([x['pick'], x['pick']+1, x['pick']-1, x['pick']+2, x['pick']-2]))].to_list(), axis=1)
        draft_order_picks['3_pick_spread_position'] = draft_order_picks.apply(lambda x: league_picks['position'][(league_picks['user_id'] == x['user_id']) & (league_picks['pick_no'].isin([x['pick'], x['pick']+1, x['pick']-1, x['pick']+2, x['pick']-2]))].to_list(), axis=1)
        round_spread = draft_teams / 2
        draft_order_picks['round_pick_spread'] = draft_order_picks.apply(lambda x: league_picks['full_name'][(league_picks['user_id'] == x['user_id']) & (league_picks['pick_no'] > x['pick']-round_spread) & (league_picks['pick_no'] < x['pick']+round_spread)].to_list(), axis=1)
        draft_order_picks['round_pick_spread_position'] = draft_order_picks.apply(lambda x: league_picks['position'][(league_picks['user_id'] == x['user_id']) & (league_picks['pick_no'] > x['pick']-round_spread) & (league_picks['pick_no'] < x['pick']+round_spread)].to_list(), axis=1)
        
        draft_order_picks['3_pick_spread_counter'] = draft_order_picks['3_pick_spread'].apply(lambda x: Counter(x))
        draft_order_picks['pick_players'] = draft_order_picks['3_pick_spread_counter'].apply(lambda x: x.most_common(3))
        draft_order_picks['round_pick_spread_counter'] = draft_order_picks['round_pick_spread'].apply(lambda x: Counter(x))
        draft_order_picks['round_players'] = draft_order_picks['round_pick_spread_counter'].apply(lambda x: x.most_common(3))
        
        draft_order_picks['3_pick_spread_position_counter'] = draft_order_picks['3_pick_spread_position'].apply(lambda x: Counter(x))
        draft_order_picks['pick_position'] = draft_order_picks['3_pick_spread_position_counter'].apply(lambda x: x.most_common(3))
        draft_order_picks['round_pick_spread_position_counter'] = draft_order_picks['round_pick_spread_position'].apply(lambda x: Counter(x))
        draft_order_picks['round_position'] = draft_order_picks['round_pick_spread_position_counter'].apply(lambda x: x.most_common(3))
    
        def clean_top_three(x):
            x_string = ''
            for i in x:
                string_add = str(i[1]) + ' ' + str(i[0])
                if x_string == '':
                    x_string = string_add
                else:
                    x_string = x_string + ' | ' + string_add
            return x_string
        
        draft_order_picks['pick_players'] = draft_order_picks['pick_players'].apply(lambda x: clean_top_three(x))
        draft_order_picks['round_players'] = draft_order_picks['round_players'].apply(lambda x: clean_top_three(x))
        draft_order_picks['pick_position'] = draft_order_picks['pick_position'].apply(lambda x: clean_top_three(x))
        draft_order_picks['round_position'] = draft_order_picks['round_position'].apply(lambda x: clean_top_three(x))   
        
        draft_url = f"https://api.sleeper.app/v1/draft/{draft_id}/picks"
        response = json.loads(requests.get(draft_url).text)
        drafted = pd.DataFrame(response)
        
        
        try:
            drafted_more = pd.DataFrame.from_dict(drafted['metadata'].to_list())
            drafted_more = drafted_more.drop(columns=['player_id'])
            drafted = pd.concat([drafted, drafted_more], axis=1)
            drafted['player_id'] = drafted['player_id'].astype(int)
            players_drafted = pd.merge(drafted, players_all_initial, how='left', on='player_id')
            players_drafted['tier'] = players_drafted['tier'].fillna('N/A')
            players_drafted['player'] = players_drafted['first_name'] + ' ' + players_drafted['last_name']
            players_all = players_all_initial[~players_all_initial['player_id'].isin(drafted['player_id'])].reset_index(drop=True)
        except:
            players_drafted = pd.DataFrame(columns=['player', 'tier', 'player_id'])
            players_all = players_all_initial
        players_qb = players_all[players_all['position'] == 'QB'].reset_index(drop=True)
        players_rb = players_all[players_all['position'] == 'RB'].reset_index(drop=True)
        players_wr = players_all[players_all['position'] == 'WR'].reset_index(drop=True)
        players_te = players_all[players_all['position'] == 'TE'].reset_index(drop=True)
        players_flex = players_all[players_all['position'] != 'QB'].reset_index(drop=True)
    except:
        players_all = pd.DataFrame(columns = ['player', 'tier', 'value', 'pick', 'rank_diff', 'best', 'avg_plot', 'colors', 'adp'])
        players_rb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_qb = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_wr = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_te = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_flex = pd.DataFrame(columns = ['player', 'tier', 'rank_diff', 'best', 'avg_plot', 'colors'])
        players_drafted = pd.DataFrame(columns=['player', 'tier', 'player_id'])

    try:
        my_user_id = league_users['user_id'][league_users['display_name'].str.lower().str.strip() == my_username.lower().strip()].iloc[0]
        current_pick = len(players_drafted)

        next_round = draft_order_picks.iloc[current_pick + 1:]
        my_next_pick = next_round[next_round['user_id'] == my_user_id].iloc[1][0]
        if my_next_pick - current_pick < draft_teams:
            my_next_pick = current_pick + draft_teams + 1
        next_round = draft_order_picks.iloc[current_pick:my_next_pick-1]
    except:
        next_round = pd.DataFrame(columns = ['pick', 'user_name', 'pick_players', 'round_players', 'pick_position', 'round_position'])
    
    players_drafted = players_drafted.to_json()
    players_all = players_all.to_json()
    players_qb = players_qb.to_json()
    players_rb = players_rb.to_json()
    players_wr = players_wr.to_json()
    players_te = players_te.to_json()
    players_flex = players_flex.to_json()
    next_round = next_round.to_json()
    
    players_dict = {
                    'all':players_all,
                    'drafted':players_drafted,
                    'qb':players_qb,
                    'rb':players_rb,
                    'wr':players_wr,
                    'te':players_te,
                    'next':next_round,
                    'flex':players_flex,
                    }
    return players_dict

@app.callback(dash.dependencies.Output('table_players_all','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_all(players_dict):
    players_all = pd.read_json(players_dict['all'])
    return players_all.iloc[:41][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_qb','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_qb(players_dict):
    players_qb = pd.read_json(players_dict['qb'])
    return players_qb.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_rb','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_rb(players_dict):
    players_rb = pd.read_json(players_dict['rb'])
    return players_rb.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_wr','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_wr(players_dict):
    players_wr = pd.read_json(players_dict['wr'])
    return players_wr.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_te','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_te(players_dict):
    players_te = pd.read_json(players_dict['te'])
    return players_te.iloc[:20][['player', 'tier']].to_dict('records')

@app.callback(dash.dependencies.Output('table_players_value','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_players_value(players_dict):
    players_drafted = pd.read_json(players_dict['drafted'])
    pick_number = len(players_drafted)
    players_all = pd.read_json(players_dict['all'])
    players_all['pick'] = players_all['adp'] - pick_number
    players_all['pick'] = players_all['pick'].round(2)
    return players_all.iloc[:50][['player', 'value', 'pick']][players_all['value'] < -5].iloc[:41].to_dict('records')

@app.callback(dash.dependencies.Output('table_league_pick_user','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_league_pick_user(players_dict):
    next_round = pd.read_json(players_dict['next'])
    return next_round[['pick', 'user_name']].to_dict('records')

@app.callback(dash.dependencies.Output('table_league_pick_players','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_league_pick_players(players_dict):
    next_round = pd.read_json(players_dict['next'])
    return next_round[['pick_players', 'round_players']].to_dict('records')

@app.callback(dash.dependencies.Output('table_league_pick_position','data'), dash.dependencies.Input('json-data', 'data'))
def update_table_league_pick_position(players_dict):
    next_round = pd.read_json(players_dict['next'])
    return next_round[['pick_position', 'round_position']].to_dict('records')

@app.callback(dash.dependencies.Output('graph', 'figure'), [dash.dependencies.Input('json-data', 'data'), dash.dependencies.Input('radio-button-position', 'value')])
def network_graph(players_dict, position_select):
    players_drafted = pd.read_json(players_dict['drafted'])
    players_all = pd.read_json(players_dict['all'])
    players_qb = pd.read_json(players_dict['qb'])
    players_rb = pd.read_json(players_dict['rb'])
    players_wr = pd.read_json(players_dict['wr'])
    players_te = pd.read_json(players_dict['te'])
    players_flex = pd.read_json(players_dict['flex'])

    position_select_dataframes = {
                        'SFLEX':players_all,
                        'FLEX':players_flex,
                        'RB':players_rb,
                        'QB':players_qb,
                        'WR':players_wr,
                        'TE':players_te,
                        'DRAFT':players_drafted,
                        }

    dataframe = position_select_dataframes[position_select][:50]
    #dataframe = scope_dataframes[networkScope]
    best_ranks = dataframe['best'].astype(int).tolist()[::-1]
    worst_ranks = dataframe['rank_diff'].astype(int).tolist()[::-1]
    average_ranks = dataframe['avg_plot'].tolist()[::-1]
    players = dataframe['player'].tolist()[::-1]
    
    figure = go.Figure(
                        data=[
                            go.Bar(
                                    x = worst_ranks,
                                    base = best_ranks,
                                    hovertext = dataframe['tier'].to_list()[::-1],
                                    text = players,
                                    textposition = 'outside',
                                    marker = dict(color=dataframe['colors'].to_list()[::-1]),
                                    orientation = 'h',
                                    width = .5),
                            go.Bar(
                                    x = [1]*len(dataframe),
                                    base = average_ranks,
                                    hoverinfo = 'skip',
                                    marker = dict(color=['black']*len(dataframe)),
                                    orientation = 'h',
                                    width = .5)
                             ]
                      )
    figure.update_layout(
                        barmode='stack',
                        autosize=False,
                        width=1500,
                        height=1500,
                        )
    return figure


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
