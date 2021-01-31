from com.cricket.stats.batting_history import BattingHistoryDownloader
from com.cricket.stats.formats import Formats

ss = BattingHistoryDownloader()
rr = ss.download_stats_as_dataframe('398438', "ODIs")

print(rr.head())
