import ssl
import urllib.error
import urllib.parse
import urllib.request
from collections import OrderedDict

import pandas as pd
from bs4 import BeautifulSoup

from com.cricket.stats.formats import Formats


class BattingHistoryDownloader:
    def __init__(self):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE

    def get_career_stats(self, player_id, format_str):
        format_stats_url = self.__create_url(player_id, Formats[format_str])
        data_frame = self.__download_batting_stats_dataframe(format_stats_url)
        return data_frame

    def get_career_summary(self, player_id):
        try:
            html = urllib.request.urlopen(self.__create__profile_url(player_id), context=self.ctx).read()
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
            return batting_stats_data_frame
        except:
            raise RuntimeError("Error downloading stats")

    def __download_batting_stats_dataframe(self, player_profile_link):
        try:
            html = urllib.request.urlopen(player_profile_link, context=self.ctx).read()
            bs = BeautifulSoup(html, "lxml")
            headers_soup = bs.find_all("tr", {"class": "headlinks"})
            headers_tag = headers_soup[0].find_all("th")
            list_of_headers = []
            for header in headers_tag:
                list_of_headers.append(header.text)
            list_of_headers[-1] = 'Match No'
            bs = BeautifulSoup(html, "lxml")
            table_body = bs.find_all('tbody')
            stats_table = table_body[1]
            rows = stats_table.find_all("tr")
            table_data_list = []
            for row in rows:
                col = row.find_all("td")
                row_data = [c.text.strip() for c in col]
                table_data_list.append(row_data)

            data_frame = pd.DataFrame(table_data_list)
            data_frame.columns = list_of_headers
            data_frame = data_frame.drop('', 1)
            return data_frame
        except:
            raise RuntimeError("Error downloading stats")

    @staticmethod
    def __create_url(player_id, format: Formats):
        format_class_map = {Formats.Tests: "1", Formats.ODIs: "2", Formats.T20Is: "3"}
        if format == Formats.Tests:
            return "http://stats.espncricinfo.com/ci/engine/player/" + player_id + ".html?class=1;template=results;type=batting;view=match"
        return "http://stats.espncricinfo.com/ci/engine/player/" + player_id + ".html?class=" + format_class_map[
            format] + ";template=results;type=batting;view=innings"

    @staticmethod
    def __create__profile_url(player_id, ):
        return "https://www.espncricinfo.com/india/content/player/" + player_id + ".html"
