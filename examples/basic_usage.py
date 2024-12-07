# examples/basic_usage.py
from algo_matchmaking import MatchMaker
from algo_matchmaking.core import Player
from algo_matchmaking.analysis import PerformanceAnalyzer

def basic_matchmaking_example():
    """Demonstrate basic matchmaking functionality"""
    # Initialize matchmaker
    matchmaker = MatchMaker()
    
    # Create some test players
    players = []
    for i in range(20):
        player = Player(f"player_{i}", initial_mmr=2000 + i * 100)
        player.preferred_roles = ['carry', 'mid']
        players.append(player)
        matchmaker.add_to_pool(player)
    
    # Find a match
    match = matchmaker.find_match()
    if match:
        print("Match found!")
        print(f"Team 1 average MMR: {match.get_team1_mmr()}")
        print(f"Team 2 average MMR: {match.get_team2_mmr()}")
        print(f"Match quality score: {match.quality_score}")

def exceptional_performance_example():
    """Demonstrate exceptional performance handling"""
    analyzer = PerformanceAnalyzer()
    
    # Create a test player with exceptional performance
    player = Player("exceptional_player", initial_mmr=3000)
    player.stats.kills = 15
    player.stats.deaths = 2
    player.stats.assists = 20
    player.stats.last_hits = 400
    player.stats.damage_dealt = 45000
    player.stats.teamfight_participation = 0.9
    
    # Create match data
    match_data = {
        'duration': 2400,
        'team_total_damage': 100000,
        'team_gold_difference': 10000,
        'winner': 'dire'
    }
    
    # Analyze performance
    result = analyzer.analyze_performance(player, match_data)
    
    print("Performance Analysis Results:")
    print(f"Overall Score: {result['overall_score']}")
    print(f"Base Metrics: {result['base_metrics']}")
    print(f"Impact Scores: {result['impact_scores']}")

if __name__ == "__main__":
    print("Running basic matchmaking example...")
    basic_matchmaking_example()
    
    print("\nRunning exceptional performance example...")
    exceptional_performance_example()

# examples/advanced_scenarios.py
from moba_matchmaking import MatchMaker
from moba_matchmaking.core import Player
from moba_matchmaking.analysis import PerformanceAnalyzer
from datetime import datetime, timedelta

def simulate_comeback_scenario():
    """Simulate a comeback scenario with exceptional performance"""
    analyzer = PerformanceAnalyzer()
    
    # Create a player who performed exceptionally despite losing
    player = Player("comeback_player", initial_mmr=3500)
    player.stats.kills = 12
    player.stats.deaths = 3
    player.stats.assists = 18
    player.stats.last_hits = 350
    player.stats.damage_dealt = 55000
    player.stats.building_damage = 12000
    player.stats.teamfight_participation = 0.95
    
    # Create match data showing team was behind
    match_data = {
        'duration': 3600,  # 60 minute game
        'team_total_damage': 120000,
        'team_gold_difference': -15000,  # Team was behind in gold
        'winner': 'radiant',  # Player's team lost
        'team_kills': 25,
        'enemy_kills': 35
    }
    
    # Analyze the comeback performance
    result = analyzer.analyze_performance(player, match_data)
    
    print("Comeback Scenario Analysis:")
    print(f"Overall Score: {result['overall_score']}")
    print(f"Adjusted Metrics: {result['adjusted_metrics']}")
    print(f"Impact Scores: {result['impact_scores']}")

def simulate_support_excellence():
    """Simulate exceptional support play"""
    analyzer = PerformanceAnalyzer()
    
    # Create a support player with great utility
    player = Player("support_player", initial_mmr=4000)
    player.stats.kills = 3
    player.stats.deaths = 4
    player.stats.assists = 25
    player.stats.last_hits = 50  # Low CS is fine for support
    player.stats.damage_dealt = 15000
    player.stats.healing = 12000
    player.stats.vision_score = 35.5
    player.stats.teamfight_participation = 0.92
    
    # Match data showing high team coordination
    match_data = {
        'duration': 2400,
        'team_total_damage': 90000,
        'team_gold_difference': 5000,
        'winner': 'dire',
        'team_kills': 40,  # High kill game
        'enemy_kills': 25
    }
    
    # Analyze support performance
    result = analyzer.analyze_performance(player, match_data)
    
    print("\nSupport Excellence Analysis:")
    print(f"Overall Score: {result['overall_score']}")
    print(f"Support Impact Metrics:")
    print(f"- Vision Control: {result['impact_scores']['vision_control']}")
    print(f"- Team Fight Impact: {result['impact_scores']['teamfight_impact']}")
    print(f"- Save Rate: {result['impact_scores']['save_rate']}")

if __name__ == "__main__":
    print("Simulating comeback scenario...")
    simulate_comeback_scenario()
    
    print("\nSimulating support excellence...")
    simulate_support_excellence()