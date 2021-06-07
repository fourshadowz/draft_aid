https://www.reddit.com/r/fantasyfootball/comments/nqvens/hey_rfantasyfootball_i_work_on_the_product_team/
https://docs.google.com/spreadsheets/d/1wmjxi3K5rjIYME_lskUvquLbN331YV0vi-kg5VakpdY/edit#gid=0

I got the current adp for sleeper from the post/google sheets above rankings are as of June 1, 2021.
If they decide to update it grab a new one from there and save it in the folder renamed as "Sleeper ADP.xlsx"

step 1:
  run fantasy_pros_data.py to pull data from a few experts that I was able to see with individuals ranking available.
  the url I pulled the data from looked like this
  https://www.fantasypros.com/nfl/rankings/pat-fitzmaurice.php?type=dynasty&scoring=PPR&position=OP
  if you would like rankings other than dynasty you would need to find the correct url and replace it in the .py file (probably just replaceing "dynasty" and "PPR")
  this will update the excel file "rankings.xlsx"
  
  alternatively you can just update the file yourelf with your own rankings, just match the formatting and make sure names are similar to what they were originally (name matching was not somthing I spent much time on)

step 2:
  open "tiers.py" and "Sleeper ADP.xlsx" and check that the adp column you want to use in the excel sheet matches the "adp_column =" name you see in line 12 of the py file (I have it set to dynasty)
  run "tiers.py" to add to the rankings excel sheet
  tiers, graph colors, player position, sleeper id, sleeper adp, wort-best ranking, avg-.5, avg-sleeper adp, sleeper adp(a second time) 
  after its run, if you choose to add your own rankings just go through and make sure all the sleeper id's are filled in
  these id's will be used to match when the app is running rather than the names
  use "sleeper_players.xlsx" to find those sleeper id's
  this will update the excel file "draft_tiers.xlsx"

  same idea as above if you want to edit this feel free, just make sure if you update tier, update the color to match (currently tier 0 is "indianred", if you update it to tier 1 then update color to "orchid") 
  also feel free to update all the colors to something you like better. colors should match what is in the link below
  https://www.google.com/url?sa=i&url=https%3A%2F%2Fmatplotlib.org%2Fstable%2Fgallery%2Fcolor%2Fnamed_colors.html&psig=AOvVaw3dS2R3fLjkSGfi7sWX4tsQ&ust=1623123816115000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJDewcLNhPECFQAAAAAdAAAAABAD

step 3:
  fill in "my_guys.xlsx" if you want
  just copy paste the names as you see them on "draft_tiers.xlsx"  
  I was pretty lazy so it's looking for exact matches
  This just adds some ***** to the names and left aligns them in the table, nothing crazy

step 4:
  kinda spicey don't do it if you don't want to know
  open "league_picks.py" and your league on the sleeper web app. the url when you click you league should look like 
  https://sleeper.app/leagues/688639493300912128
  copy the numbers at the end and paste it after "league_id =" on line 5 of "league_picks.py"
  run "league_picks.py" and it will update "league_picks.xlsx"
  this is a sheet of all the mock and real drafts done by anyone in your league in 2021.

step 5:
  Finally run app.py
  go to the url Dash says its running on
  open the draft you want to track
  https://sleeper.app/draft/nfl/706258148431831040
  copy the last numbers in the draft and paste them in the left input that is asking you for draft id
  type your sleeper username in the right input
  success


 
  all visuals will update every 10 seconds with data from the draft, you can also refresh if you're really impatient 

  graph on the left is top 50 players ranges are best to worst ranking, black bar is the average
  color will match tiers on the right
  can update the graph by position above

  next is the list of all players by tier, and the list broken out into positions
  nothing you can really do here but watch

  next is value table
  this will show the diff between sleeper adp and yours as well has how many picks we are away from their sleeper adp
  the row will change color based on how close to the pick we are getting.  
  within 12 picks will be green, within 24 yellow, otherwise red
  
  last section is the league mock data
  this will show the picks coming up between now and your next 2 picks
  if for any of those picks the person is in your league, this table will show their name and the pick number
  the top 3 players they pick at this pick number as well as 1 pick above and 1 pick below this number
  the top 3 players they pick at this pick number as well as (the number of teams in your draft / 2) above and below this pick
  the top 3 positions they pick at this pick number as well as 1 pick above and 1 pick below this number
  the top 3 positions they pick at this pick number as well as (the number of teams in your draft / 2) above and below this pick

  





