
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import logging

from src.algo_matchmaking.core.player import Player

class SafetyChecker:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self.default_config()
        self.logger = logging.getLogger(__name__)

    def default_config(self) -> Dict:
        return {
            'max_mmr_gain': 5,
            'max_consecutive_exceptional': 3,
            'time_window_hours': 24,
            'minimum_game_duration': 25,
            'required_teamfight_participation': 0.6,
            'maximum_tilt_factor': 0.3,
            'minimum_team_gold_difference': 5000,
            'suspicious_performance_threshold': 0.95,
            'maximum_daily_games': 30
        }

    def validate_performance(
        self,
        player: 'Player',
        match_data: Dict,
        performance_score: float
    ) -> Tuple[bool, str]:
        """
        Validate if a performance is legitimate and not suspicious
        Returns: (is_valid, reason_if_invalid)
        """
        checks = [
            self.check_game_duration(match_data),
            self.check_teamfight_participation(player, match_data),
            self.check_tilt_factor(player),
            self.check_game_balance(match_data),
            self.check_recent_performances(player),
            self.check_suspicious_patterns(player, performance_score)
        ]
        
        for is_valid, reason in checks:
            if not is_valid:
                self.logger.warning(f"Safety check failed for player {player.id}: {reason}")
                return False, reason
                
        return True, ""

    def check_game_duration(self, match_data: Dict) -> Tuple[bool, str]:
        """Check if game duration is sufficient"""
        min_duration = self.config['minimum_game_duration'] * 60  # Convert to seconds
        if match_data['duration'] < min_duration:
            return False, f"Game too short: {match_data['duration']}s"
        return True, ""

    def check_suspicious_patterns(
        self,
        player: 'Player',
        performance_score: float
    ) -> Tuple[bool, str]:
        """Check for suspicious performance patterns"""
        # Check for consistently extremely high performance
        if performance_score > self.config['suspicious_performance_threshold']:
            recent_scores = [p['score'] for p in player.performance_history[-5:]]
            if all(score > self.config['suspicious_performance_threshold'] 
                  for score in recent_scores):
                return False, "Suspiciously consistent high performance"
        
        # Check for unusual stat patterns
        if self.detect_unusual_patterns(player.stats):
            return False, "Unusual stat patterns detected"
            
        return True, ""

    def detect_unusual_patterns(self, stats: 'PlayerStats') -> bool:
        """Detect unusual statistical patterns"""
        patterns = [
            self.check_impossible_stats(stats),
            self.check_unusual_ratios(stats),
            self.check_consistency_patterns(stats)
        ]
        
        return any(patterns)
