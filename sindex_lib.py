from team_dict import team_abbr
import datetime
import time

def field_pos_mult(loc, punt_team):
    if loc == '50':
        return 1.1**(10)
    else:
        abr,yds_str = loc.split()
        yds = int(yds_str)
        if team_abbr[abr] == punt_team:
            if yds < 41:
                return 1
            else:
                return 1.1**(yds-40)
        elif yds == 50:
            return 1.1**(yds-40)
        else:
            return 2.594*(1.2**(50-yds))

def dist_from_first_mult(dist):
    if dist > 9:
        return .2
    elif dist > 6:
        return .4
    elif dist > 3:
        return .6
    elif dist > 1:
        return .8
    else:
        return 1

def score_mult(score, punt_team):
    if score == '-':
        return 1
    else:
        punt_score_str,opp_score_str = score.split('-')
        punt_score = int(punt_score_str)
        opp_score = int(opp_score_str)
        punt_behind_by = opp_score - punt_score
        if punt_behind_by < 0:
            return 1
        else:
            if punt_behind_by == 0:
                return 2
            elif punt_behind_by > 8:
                return 3
            elif punt_behind_by > 0:
                return 4
            else:
                print("You shouldn't have gotten here!!!!")
    


def clock_mult(time, quarter, score):
    if score == '-':
        return 1
    else:
        punt_score_str,opp_score_str = score.split('-')
        punt_score = int(punt_score_str)
        opp_score = int(opp_score_str)
        punt_behind_by = opp_score - punt_score
        if punt_behind_by >= 0 and quarter > 2: 
            sec_quarter = 15*60
            sec_ot = 15*60
            sec_gameclock = int(time.split(':')[0])*60+int(time.split(':')[1])
            if quarter == 3:
                seconds_elapsed_since_half = sec_quarter - sec_gameclock 
            elif quarter == 4:
                seconds_elapsed_since_half = 2*sec_quarter - sec_gameclock 
            elif quarter == 5:
                seconds_elapsed_since_half = (2*sec_quarter) + (sec_ot - sec_gameclock)
            return ((seconds_elapsed_since_half*.001)**3)+1
        else:
            return 1

def surrender_index(location, punt_team, score, time, quarter, dist):
    return field_pos_mult(location,punt_team)*dist_from_first_mult(dist)*score_mult(score,punt_team)*clock_mult(time,quarter,score)
