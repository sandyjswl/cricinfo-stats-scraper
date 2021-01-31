class Constants:
    STATS_ANALYSIS = "statsAnalysis"
    PLAYER_ID = 'player_id'


class RunsByYear:
    TEST = "runs_by_year_tests"
    ODI = "runs_by_year_odi"
    T20 = "runs_by_year_t20"


class AverageByGame:
    TEST = "average_by_game_tests"
    ODI = "average_by_game_odi"
    T20 = "average_by_game_t20"


class AverageByYear:
    TEST = "average_by_year_tests"
    ODI = "average_by_year_odi"
    T20 = "average_by_year_t20"


from enum import Enum


class Formats(Enum):
    Tests = "Tests"
    ODIs = "ODIs"
    T20Is = "T20Is"


class BattingHistoryCollections(Enum):
    Tests = "battingHistoryTest"
    ODIs = "battingHistoryODI"
    T20Is = "battingHistoryT20"


class AverageByGameComparison:
    TEST = "average_by_game_comparison_tests"
    ODI = "average_by_game_comparison_odi"
    T20 = "average_by_game_comparison_t20"


class ComparisonTypes(Enum):
    AverageByGame = "average_by_game"
    AverageByYear = "average_by_year"
