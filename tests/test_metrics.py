# tests/test_metrics.py

import unittest
from unittest.mock import Mock, patch
from algo_matchmaking.core.metrics import MetricsCalculator, GameMetrics

class TestMetricsCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = MetricsCalculator()
        self.sample_metrics = GameMetrics(
            kills=10,
            deaths=3,
            assists=15,
            last_hits=300,
            denies=20,
            gpm=650,
            xpm=750,
            hero_damage=25000,
            tower_damage=5000,
            hero_healing=1500,
            stun_duration=100,
            camps_stacked=5,
            runes_collected=8,
            wards_placed=15,
            wards_destroyed=5,
            teamfight_participation=0.8
        )
        
    def test_farming_efficiency(self):
        efficiency = self.calculator.calculate_farming_efficiency(
            self.sample_metrics,
            2400,  # 40 minute game
            'carry'
        )
        
        self.assertGreaterEqual(efficiency, 0.0)
        self.assertLessEqual(efficiency, 1.0)
        
        # Test different roles
        for role in ['carry', 'mid', 'offlane', 'soft_support', 'hard_support']:
            efficiency = self.calculator.calculate_farming_efficiency(
                self.sample_metrics,
                2400,
                role
            )
            self.assertGreaterEqual(efficiency, 0.0)
            self.assertLessEqual(efficiency, 1.0)

    def test_combat_efficiency(self):
        efficiency = self.calculator.calculate_combat_efficiency(
            self.sample_metrics,
            100000,  # total team damage
            'carry'
        )
        
        self.assertGreaterEqual(efficiency, 0.0)
        self.assertLessEqual(efficiency, 1.0)
        
        # Test extreme cases
        low_damage_metrics = GameMetrics(
            hero_damage=5000,
            kills=2,
            deaths=10,
            assists=5
        )
        low_efficiency = self.calculator.calculate_combat_efficiency(
            low_damage_metrics,
            100000,
            'carry'
        )
        self.assertLess(low_efficiency, 0.5)

    def test_vision_score(self):
        vision_score = self.calculator.calculate_vision_score(
            self.sample_metrics,
            2400  # 40 minute game
        )
        
        self.assertGreaterEqual(vision_score, 0.0)
        self.assertLessEqual(vision_score, 1.0)
        
        # Test support expectations
        support_metrics = GameMetrics(
            wards_placed=25,
            wards_destroyed=10
        )
        support_score = self.calculator.calculate_vision_score(
            support_metrics,
            2400
        )
        self.assertGreater(support_score, 0.5)

    def test_utility_score(self):
        utility_score = self.calculator.calculate_utility_score(
            self.sample_metrics,
            10  # number of team fights
        )
        
        self.assertGreaterEqual(utility_score, 0.0)
        self.assertLessEqual(utility_score, 1.0)
        
        # Test high utility performance
        high_utility_metrics = GameMetrics(
            stun_duration=200,
            hero_healing=8000,
            teamfight_participation=0.9
        )
        high_score = self.calculator.calculate_utility_score(
            high_utility_metrics,
            10
        )
        self.assertGreater(high_score, 0.7)

    def test_overall_performance(self):
        game_data = {
            'duration': 2400,
            'team_damage': 100000,
            'team_fights': 10
        }
        
        result = self.calculator.calculate_overall_performance(
            self.sample_metrics,
            game_data,
            'carry'
        )
        
        self.assertIn('detailed_scores', result)
        self.assertIn('overall_score', result)
        self.assertGreaterEqual(result['overall_score'], 0.0)
        self.assertLessEqual(result['overall_score'], 1.0)

if __name__ == '__main__':
    unittest.main()