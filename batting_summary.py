from com.cricket.stats.batting_stats_downloader import BattingHistoryDownloader

player_id = input("Enter player id:  ")

stats_downloader = BattingHistoryDownloader()
player_stats = stats_downloader.get_career_summary(player_id)
file_name = input("Download success,\nEnter filename with csv extension:  ")
player_stats.to_csv(file_name)