class Game:
    def __init__(self, eid):
        self.eid = eid
        self.url = "http://www.nfl.com/liveupdate/game-center/{}/{}_gtd.json".format(eid,eid)
        self.dcount = 0
        self.last_punt_drive = 0
        