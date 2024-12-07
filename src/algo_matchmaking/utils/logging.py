import logging
from datetime import datetime
from typing import Dict, Any
import json

class MatchLogger:
    def __init__(self, log_file: str = 'match_history.log'):
        self.logger = logging.getLogger('MatchLogger')
        self.setup_logger(log_file)

    def setup_logger(self, log_file: str):
        """Setup logging configuration"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def log_match_creation(self, match: 'Match'):
        """Log match creation details"""
        match_data = {
            'match_id': id(match),
            'timestamp': datetime.now().isoformat(),
            'team1_avg_mmr': self.calculate_team_mmr(match.team1),
            'team2_avg_mmr': self.calculate_team_mmr(match.team2),
            'match_quality': match.match_quality
        }
        
        self.logger.info(f"Match created: {json.dumps(match_data)}")

    def log_performance_analysis(
        self,
        player_id: str,
        performance_data: Dict[str, Any]
    ):
        """Log performance analysis results"""
        log_data = {
            'player_id': player_id,
            'timestamp': datetime.now().isoformat(),
            'performance_metrics': performance_data
        }
        
        self.logger.info(f"Performance analysis: {json.dumps(log_data)}")

    def log_exceptional_performance(
        self,
        player_id: str,
        match_id: str,
        performance_data: Dict[str, Any]
    ):
        """Log exceptional performance details"""
        log_data = {
            'player_id': player_id,
            'match_id': match_id,
            'timestamp': datetime.now().isoformat(),
            'performance_type': 'exceptional',
            'details': performance_data
        }
        
        self.logger.info(f"Exceptional performance: {json.dumps(log_data)}")

    def log_safety_violation(
        self,
        player_id: str,
        violation_type: str,
        details: Dict[str, Any]
    ):
        """Log safety check violations"""
        log_data = {
            'player_id': player_id,
            'violation_type': violation_type,
            'timestamp': datetime.now().isoformat(),
            'details': details
        }
        
        self.logger.warning(f"Safety violation: {json.dumps(log_data)}")

    def log_mmr_adjustment(
        self,
        player_id: str,
        mmr_change: float,
        reason: str,
        performance_metrics: Dict[str, Any]
    ):
        """Log MMR adjustments with detailed reasoning"""
        log_data = {
            'player_id': player_id,
            'mmr_change': mmr_change,
            'reason': reason,
            'timestamp': datetime.now().isoformat(),
            'metrics': performance_metrics
        }
        
        self.logger.info(f"MMR adjustment: {json.dumps(log_data)}")