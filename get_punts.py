from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup as soup
import os
import csv
import sqlite3
import time
import sindex_lib

# def get_url(year,week,quarter):
#     year = str(year)
#     week = str(week)
#     quarter = str(quarter)
#     return 'https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&year_min=' + year + '&year_max=' + year + '&game_type=R&game_num_min=0&game_num_max=99&week_num_min=' + week + '&week_num_max=' + week + '&quarter%5B%5D=' + quarter + '&minutes_max=15&seconds_max=00&minutes_min=00&seconds_min=00&down%5B%5D=0&down%5B%5D=1&down%5B%5D=2&down%5B%5D=3&down%5B%5D=4&field_pos_min_field=team&field_pos_max_field=team&end_field_pos_min_field=team&end_field_pos_max_field=team&type%5B%5D=PUNT&no_play=N&turnover_type%5B%5D=interception&turnover_type%5B%5D=fumble&score_type%5B%5D=touchdown&score_type%5B%5D=field_goal&score_type%5B%5D=safety&rush_direction%5B%5D=LE&rush_direction%5B%5D=LT&rush_direction%5B%5D=LG&rush_direction%5B%5D=M&rush_direction%5B%5D=RG&rush_direction%5B%5D=RT&rush_direction%5B%5D=RE&pass_location%5B%5D=SL&pass_location%5B%5D=SM&pass_location%5B%5D=SR&pass_location%5B%5D=DL&pass_location%5B%5D=DM&pass_location%5B%5D=DR&order_by=yards'


start_time = time.time()

# d = webdriver.Chrome(os.getcwd() + "/chromedriver")
conn = sqlite3.connect('punts.db')
c = conn.cursor()
c2 = conn.cursor()

# c.execute("""CREATE TABLE punts (
#     date text,
#     team text,
#     opp text,
#     quarter integer,
#     time text,
#     down integer
#     to_go integer,
#     location text,
#     score text,
#     detail text,
#     yds integer,
#     epb real,
#     epa real,
#     pyds integer,
#     pryds integer,
#     tweet_id text
#     )""")

# c.execute("""ALTER TABLE punts ADD surrender_index real""")
c.execute("""SELECT * FROM punts""")
for row in c:
    row_sindex = sindex_lib.surrender_index(row[6], row[1], row[7],row[4], row[3], row[15])
    c2.execute("""SELECT * FROM punts""")
    c2.execute("""
        UPDATE punts
        SET surrender_index = ?
        WHERE pk = ?
        """, (row_sindex, row[16]))
    print(row_sindex)


conn.commit()


# for i in range(2000,2019):
#     for j in range(1,21):
#         for k in range(1,6):
#             d.get(get_url(i,j,k))
#             try:
#                 reveal_csv_button = d.find_element_by_xpath('//*[@id="all_all_plays"]/div[1]/div/ul/li[1]/span')
#                 hover = ActionChains(d).move_to_element(reveal_csv_button)
#                 hover.perform()
#                 csv_button = d.find_element_by_xpath('//*[@id="all_all_plays"]/div[1]/div/ul/li[1]/div/ul/li[4]/button')
#                 click = ActionChains(d).click(csv_button)
#                 click.perform()
#                 csv_data = soup(d.page_source, 'html.parser').find('pre', {'id':'csv_all_plays'}).text
#                 file1 = open("punt_csv.csv","w")
#                 file1.write(csv_data)
#                 with open('punt_csv.csv', 'r') as fin:
#                     data = fin.read().splitlines(True)
#                 with open('punt_csv.csv', 'w') as fout:
#                     fout.writelines(data[1:])
#                 with open ('punt_csv.csv') as fin:
#                     dr = csv.DictReader(fin)
#                     to_db = [(i['Date'], i['Tm'], i['Opp'], i['Quarter'], i['Time'], i['Down'], i['ToGo'], i['Location'], i['Score'], i['Detail'], i['Yds'], i['EPB'], i['EPA'], i['Diff'], i['PYds'], i['PRYds']) for i in dr]
#                 c.executemany("INSERT INTO punts (date, team, opp, quarter, time, down, to_go, location, score, detail, yds, epb, epa, diff, pyds, pryds) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
#                 conn.commit()
#             except NoSuchElementException:
#                 print("No punts for season {}, week {}, quarter {}.".format(i,j,k))
#                 pass

conn.close()
print("--- %s seconds ---" % (time.time() - start_time))