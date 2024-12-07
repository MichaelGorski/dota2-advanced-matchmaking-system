# tests/test_performance.py

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from src.algo_matchmaking.analysis.metrics import GameMetrics
from src.algo_matchmaking.analysis.performance import PerformanceAnalyzer

class TestPerformanceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = PerformanceAnalyzer()
        self.sample_stats = GameMetrics(
            kills=10,
            deaths=2,
            assists=15,
            last_hits=300,
            denies=20,
            gpm=650,
            xpm=750,
            hero_damage=25000,
            tower_damage=5000,
            hero_healing=1500,
            teamfight_participation=0.8
        )
        
        self.sample_match_data = {
            'duration': 2400,  # 40 minutes
            'team_total_damage': 100000,
            'team_gold_difference': 8000,
            'winner': 'radiant',
            'team_kills': 30,
            'enemy_kills': 20,
            'team_fights': 12
        }

    def test_analyze_performance(self):
        """Test complete performance analysis"""
        context = Mock(
            game_state='winning',
            game_time=35,
            team_networth=50000,
            enemy_networth=42000,
            team_kills=30,
            enemy_kills=20,
            structures_standing={'radiant': 6, 'dire': 3}
        )

        result = self.analyzer.analyze_performance(
            self.sample_stats,
            self.sample_match_data,
            context
        )

        # Verify result structure
        self.assertIn('base_metrics', result)
        self.assertIn('adjusted_metrics', result)
        self.assertIn('impact_scores', result)
        self.assertIn('overall_score', result)

        # Verify score ranges
        self.assertGreaterEqual(result['overall_score'], 0.0)
        self.assertLessEqual(result['overall_score'], 1.0)

    def test_losing_game_performance(self):
        """Test performance evaluation in losing game"""
        losing_context = Mock(
            game_state='losing',
            game_time=35,
            team_networth=42000,
            enemy_networth=55000,
            team_kills=15,
            enemy_kills=30,
            structures_standing={'radiant': 2, 'dire': 6}
        )

        result = self.analyzer.analyze_performance(
            self.sample_stats,
            self.sample_match_data,
            losing_context
        )

        # Verify higher scoring for good performance while losing
        self.assertGreater(
            result['adjusted_metrics']['combat_score'],
            result['base_metrics']['combat_score']
        )

    def test_support_performance(self):
        """Test support-specific performance metrics"""
        support_stats = GameMetrics(
            kills=2,
            deaths=5,
            assists=25,
            last_hits=50,
            gpm=300,
            hero_damage=12000,
            hero_healing=5000,
            wards_placed=20,
            wards_destroyed=8,
            teamfight_participation=0.9
        )

        context = Mock(game_state='winning', game_time=30)
        result = self.analyzer.analyze_performance(
            support_stats,
            self.sample_match_data,
            context
        )

        # Verify support-specific metrics
        self.assertIn('vision_control', result['impact_scores'])
        self.assertIn('utility_score', result['impact_scores'])
        self.assertGreater(result['impact_scores']['utility_score'], 0.6)

    def test_carry_performance(self):
        """Test carry-specific performance metrics"""
        carry_stats = GameMetrics(
            kills=15,
            deaths=2,
            assists=10,
            last_hits=400,
            gpm=800,
            hero_damage=35000,
            tower_damage=8000,
            teamfight_participation=0.7
        )

        context = Mock(game_state='winning', game_time=35)
        result = self.analyzer.analyze_performance(
            carry_stats,
            self.sample_match_data,
            context
        )

        # Verify carry-specific metrics
        self.assertIn('farm_efficiency', result['impact_scores'])
        self.assertIn('damage_output', result['impact_scores'])
        self.assertGreater(result['impact_scores']['farm_efficiency'], 0.7)

    def test_performance_consistency(self):
        """Test consistency checking in performance evaluation"""
        inconsistent_stats = GameMetrics(
            kills=20,  # Suspiciously high
            deaths=0,  # Perfect score
            assists=30,
            last_hits=500,  # Unrealistic
            gpm=1000,  # Too high
            hero_damage=50000,
            teamfight_participation=1.0  # Perfect score
        )

        context = Mock(game_state='winning', game_time=35)
        result = self.analyzer.analyze_performance(
            inconsistent_stats,
            self.sample_match_data,
            context
        )

        # Should flag suspicious performance
        self.assertLess(result['overall_score'], 0.9)