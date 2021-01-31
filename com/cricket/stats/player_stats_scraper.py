import ssl
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict

import pandas as pd
from bs4 import BeautifulSoup


class StatsDownloader:
    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def map_dataframe_columns(self, columns):
        columns_list = columns[:]

        colums_map = {"Mat": "matches", "Inns": "innings", "NO": "notOuts", "Runs": "runs",
                      "HS": "highest", "Ave": "average",
                      "BF": "ballsFaced", "SR": "strikeRate",
                      "100": "hundreds", "50": "fifties",
                      "4s": "fours", "6s": "sixes", "Ct": "caughtOut", "St": "stumpedOut"}
        result = []
        for column in columns_list:
            if column in colums_map:
                current_column = colums_map[column]
                result.append(current_column)
        return result

    def download_batting_stats(self, player_profile_link, player_name):
        html = urllib.request.urlopen(player_profile_link, context=self.ctx).read()
        print("Downloading batting stats for " + player_name)
        list_of_dict = []
        soup = BeautifulSoup(html, "lxml")
        table_body = soup.find_all('tbody')
        rows = table_body[0].find_all('tr')
        headings = soup.findAll('tr', {"class", "head"})

        tables_list = headings[:2]
        batting_table = tables_list[0]

        columns = batting_table.find_all("th")
        batting_columns_list = []
        for i in columns:
            batting_columns_list.append(i.text)
        for row in rows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            batting_data = OrderedDict()
            for col in range(len(cols)):
                batting_data[batting_columns_list[col]] = cols[col]
            list_of_dict.append(batting_data)
        batting_stats_data_frame = pd.DataFrame(list_of_dict)
        batting_stats_data_frame.set_index('', inplace=True)
        print(batting_stats_data_frame)
        df_columns = batting_stats_data_frame.columns
        columns = self.map_dataframe_columns(df_columns)
        batting_stats_data_frame.columns = columns
        print("Download Successful")
        print(5 * "- - -")
        return batting_stats_data_frame

    def downloadBowlingStats(self):
        html = ""
        temp_data = OrderedDict()
        list_of_dict = []
        bs = BeautifulSoup(html, "lxml")
        table_body = bs.find_all('tbody')
        rows = table_body[1].find_all('tr')
        headings = bs.findAll('tr', {"class", "head"})

        heads = headings[:2]
        vatting = heads[0]
        bowling = heads[1]

        batText = vatting.find_all("th")
        bowlText = bowling.find_all("th")
        bat = []
        for i in batText:
            bat.append(i.text)

        bowl = []
        for i in bowlText:
            bowl.append(i.text)

        # print(bat[1:])
        # print(bowl[1:])

        # bat = bat[1:]
        # bowl = bowl[1:]
        print(len(bat))

        for row in rows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            temp_data = OrderedDict()
            #     print(len(cols))
            #     print(cols)
            #     print(bat)
            for col in range(len(cols)):
                temp_data[bowl[col]] = cols[col]

            list_of_dict.append(temp_data)

        bowl_df = pd.DataFrame(list_of_dict)
        bowl_df.set_index('', inplace=True)
        return bowl_df

    def formatRuns(self, runs):
        runs = runs.replace("*", '')
        try:
            return int(runs)
        except:
            return 0

    def formatDate(self, date):
        year = date.split(" ")[-1]
        return year

    def formatUrl(self, playerID):
        url = "http://stats.espncricinfo.com/ci/engine/player/" + playerID + ".html?class=2;template=results;type=batting;view=innings"
        return url

    def download_batting_history_stats(self, player_name, player_id):
        player_url = self.formatUrl(player_id)
        html = urllib.request.urlopen(player_url, context=self.ctx).read()
        list_of_dict = []
        bs = BeautifulSoup(html, "lxml")

        mydivs = bs.findAll("div", {"class": "icc-home"})
        player_name = mydivs[0].findAll("a")[0].text.split("/")[2]
        table_body = bs.find_all('tbody')
        rows = table_body[1].find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [x.text.strip() for x in cols]
            temp_data = OrderedDict()
            for i in range(len(cols)):
                temp_data["Runs"] = cols[0]
                temp_data["Mins"] = cols[1]
                temp_data["BF"] = cols[2]
                temp_data["4s"] = cols[3]
                temp_data["6s"] = cols[4]
                temp_data["SR"] = cols[5]
                temp_data["POS"] = cols[6]
                temp_data["Dismissal"] = cols[7]
                temp_data["Inns"] = cols[8]
                temp_data["Opposition"] = cols[10]
                temp_data["Ground"] = cols[11]
                temp_data["Date"] = cols[12]
            list_of_dict.append(temp_data)
        df = pd.DataFrame(list_of_dict)
        df['Runs'] = df['Runs'].apply(lambda runs: self.formatRuns(runs))

        # In[ ]:

        # In[10]:

        # In[11]:

        df['Year'] = df['Date'].apply(lambda date: self.formatDate(date))

        # In[ ]:

        # In[12]:

        res = df.groupby(['Year']).agg({'Runs': 'sum', 'Opposition': 'count'})

        # In[13]:

        res = res.rename(columns={'Opposition': 'Matches'})

        # In[14]:
        dictionary_res = res.to_dict('index')
        res.reset_index(level=0, inplace=True)

        return res, dictionary_res
