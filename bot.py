import tweepy, time
import xml.etree.ElementTree as ET 
import requests
import json
import game
from config import key,key_secret,token,token_secret
from sindex_lib import surrender_index
from team_dict import team_abbr


def get_clean_time(game_clock):
        if game_clock[0] == "0":
            return game_clock[1:]
        else:
            return game_clock

def get_ordinal_indicator(quarter):
    if quarter == 1:
        return "the 1st quarter"
    elif quarter == 2:
        return "the 2nd quarter"
    elif quarter == 3:
        return "the 3rd quarter"
    elif quarter  == 4:
        return "the 4th quarter"
    else:
        return "overtime"

def get_punt_team_full_name(punt_team):
    return team_abbr[punt_team]

def get_nice_location(location, punt_team):
    if location == '50':
        return "the 50"
    half,yds = location.split()
    if punt_team == half:
        return "their own {}".format(yds)
    else:
        return "their opponent's {}".format(yds)



auth = tweepy.OAuthHandler(key,key_secret)
auth.set_access_token(token,token_secret)

api = tweepy.API(auth)

# the week #
c_week = "-1"
# the games being played this week
c_week_gms = {}
# the games currently being played
c_gms = {}
# the c_gms metadata
c_gms_md = {}
while True:

    # check if there have been any punts and if there have been tweet about it!
    for g in c_gms_md:
        resp = requests.get(c_gms_md[g].url)
        game_json = json.loads(resp.content)
        drivecount = game_json[g]["drives"]["crntdrv"]
        #there were some new drives since last time I checked
        if (drivecount != c_gms_md[g].dcount):
            c_gms_md[g].dcount = drivecount
            drive = game_json[g]["drives"][str(c_gms_md[g].dcount)]
            result = drive["result"] 
            plays = drive["plays"]
            if result == "" and not c_gms_md[g].dcount == 1:
                drive = game_json[g]["drives"][str(c_gms_md[g].dcount-1)]
                result = drive["result"] 
                plays = drive["plays"]
            if result == "Punt":
                last_play_key = list(plays)[-1]
                last_play = plays[last_play_key]
                location = last_play["yrdln"]
                punt_team = drive["posteam"]
                pt_score = game_json[g]["home"]["score"]["T"]
                opp_score = game_json[g]["away"]["score"]["T"]
                opp_team  = game_json[g]["away"]["abbr"]
                punt_team_home = True
                if punt_team != game_json[g]["home"]["abbr"]:
                    temp = pt_score
                    pt_score = opp_score
                    opp_score = temp
                    opp_team = game_json[g]["home"]["abbr"]
                    punt_team_home = False
                score = "{} - {}".format(pt_score,opp_score)
                game_clock = last_play["time"]
                quarter = last_play["qtr"]
                dist = last_play["ydstogo"]
                print("this is the distance {}".format(dist))
                sindex = surrender_index(location, punt_team, score, game_clock, quarter, dist)

                # tweet da ting
                punt_tweet = api.update_status(
                    status = "{} {}-{} {}\n{} in {}\n\n{} punt with {} yards to go at {} for a Surrender Index of {}".format(
                        punt_team,
                        pt_score,
                        opp_score,
                        opp_team,
                        get_clean_time(game_clock),
                        get_ordinal_indicator(quarter),
                        get_punt_team_full_name(punt_team),
                        dist,
                        get_nice_location(location, punt_team),
                        round(sindex,2)
                    )
                )


                
    #get xml with current week game data
    resp = requests.get("http://www.nfl.com/liveupdate/scorestrip/ss.xml")
    with open('week_games.xml', 'wb') as f:
        f.write(resp.content)

    #parse it 
    tree = ET.parse('week_games.xml')
    root = tree.getroot()

    #check if there are new games
    games = root.find('gms')
    if games.attrib['w'] != c_week:
        # new gameweek!
        # empty the current games directory and put all the new games in there.
        c_week_gms = {}
        c_week = games.attrib['w']
        print("this should only run once")

    # update the game statuses for this week (quarter, time, etc)
    for g in games:
        c_week_gms[g.attrib['eid']] = g.attrib
    
    # update the dictionary of currently played games
    for g in c_week_gms:
        if c_week_gms[g]['q'].isdigit() or c_week_gms[g]['q'] == "H":
            # if the quarter is a digit (1,2,3,4,5) that means there's a quarter in progress (the game isn't over/has started/is not in halftime)
            if not g in c_gms.keys():
                c_gms[g] = c_week_gms[g]
                print("new game added")
                print(c_gms[g]['h'])
                print(c_gms[g]['v'])
        else:
            # if the quarter is not a digit that means the game is not in play and thus we remove it from the dictionary of currently playing games
            if g in c_gms.keys():
                c_gms[g] = None
                c_gms_md[g] = None

    # make a Game object for each game that is currently being played.
    for g in c_gms:
        if not g in c_gms_md.keys():
            c_gms_md[g] = game.Game(g)
    
    
    time.sleep(60)

    
