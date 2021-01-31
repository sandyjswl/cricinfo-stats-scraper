from com.cricket.stats.batting_history import BattingHistoryDownloader

player_id = input("Enter player id:  ")
format = input("Enter format (Tests|ODIs|T20Is) :  ")

stats_downloader = BattingHistoryDownloader()
player_stats = stats_downloader.download_stats_as_dataframe(player_id, format)
file_name = input("Download success,\n Enter filename to save as:  ")
player_stats.to_csv(file_name)
