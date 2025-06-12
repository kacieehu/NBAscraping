from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd

def get_latest_per_game_stats_with_name(player_name):
    # Find player info by full name
    player_list = players.find_players_by_full_name(player_name)
    if not player_list:
        raise ValueError(f"Player '{player_name}' not found")
    player = player_list[0]
    player_id = player['id']
    full_name = player['full_name']

    # Get career stats dataframe
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]

    # Filter to NBA regular season only (LEAGUE_ID = '00')
    regular_season_df = df[(df['LEAGUE_ID'] == '00') & (df['SEASON_ID'].str.startswith('2'))]

    # Sort descending by season and get latest season stats
    latest_season_stats = regular_season_df.sort_values('SEASON_ID', ascending=False).iloc[0]

    # Convert Series to dict and add player name
    stats_dict = latest_season_stats.to_dict()
    stats_dict['PLAYER_NAME'] = full_name

    return stats_dict

# Example usage:
player_name = "LeBron James"
latest_stats = get_latest_per_game_stats_with_name(player_name)

print(f"Latest stats for {latest_stats['PLAYER_NAME']}:")
for stat, value in latest_stats.items():
    if stat != 'PLAYER_NAME':
        print(f"{stat}: {value}")
