from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class ExceptionalMetrics:
    """Metrics for evaluating exceptional performances"""
    combat_score: float = 0.0
    farm_efficiency: float = 0.0
    map_impact: float = 0.0
    objective_control: float = 0.0
    teamfight_contribution: float = 0.0
    vision_control: float = 0.0
    utility_score: float = 0.0
    game_impact: float = 0.0

class ExceptionalAnalyzer:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self.default_config()
        
    def default_config(self) -> Dict:
        return {
            'exceptional_threshold': 0.90,
            'excellent_threshold': 0.80,
            'very_good_threshold': 0.70,
            'max_mmr_gain': 5,
            'min_game_duration': 1500,  # 25 minutes
            'min_teamfight_participation': 0.6,
            'max_consecutive_exceptional': 3
        }

    def analyze_exceptional_performance(
        self,
        player_stats: Dict,
        match_data: Dict,
        game_context: Dict
    ) -> Tuple[bool, str, float, Dict]:
        """
        Analyze if a performance qualifies as exceptional
        Returns: (is_exceptional, tier, mmr_adjustment, detailed_metrics)
        """
        # Calculate comprehensive metrics
        metrics = self.calculate_exceptional_metrics(
            player_stats,
            match_data,
            game_context
        )
        
        # Validate performance
        if not self.validate_performance(metrics, match_data):
            return False, "normal", 0.0, metrics

        # Calculate overall score
        overall_score = self.calculate_overall_score(metrics)
        
        # Determine performance tier and MMR adjustment
        tier, mmr_adj = self.determine_tier_and_adjustment(
            overall_score,
            metrics,
            match_data
        )
        
        return (tier != "normal"), tier, mmr_adj, metrics

    def calculate_exceptional_metrics(
        self,
        player_stats: Dict,
        match_data: Dict,
        game_context: Dict
    ) -> ExceptionalMetrics:
        """Calculate detailed exceptional performance metrics"""
        metrics = ExceptionalMetrics()
        
        # Combat performance considering game state
        metrics.combat_score = self.calculate_combat_score(
            player_stats,
            match_data,
            game_context
        )
        
        # Farm efficiency relative to game state
        metrics.farm_efficiency = self.calculate_farm_efficiency(
            player_stats,
            match_data,
            game_context
        )
        
        # Map presence and impact
        metrics.map_impact = self.calculate_map_impact(
            player_stats,
            match_data
        )
        
        # Objective control
        metrics.objective_control = self.calculate_objective_control(
            player_stats,
            match_data
        )
        
        # Teamfight contribution
        metrics.teamfight_contribution = self.calculate_teamfight_contribution(
            player_stats,
            match_data
        )
        
        # Vision control
        metrics.vision_control = self.calculate_vision_control(
            player_stats,
            match_data
        )
        
        # Utility score
        metrics.utility_score = self.calculate_utility_score(
            player_stats,
            match_data
        )
        
        # Overall game impact
        metrics.game_impact = self.calculate_game_impact(metrics)
        
        return metrics

    def determine_tier_and_adjustment(
        self,
        overall_score: float,
        metrics: ExceptionalMetrics,
        match_data: Dict
    ) -> Tuple[str, float]:
        """Determine performance tier and MMR adjustment"""
        # Check exceptional tier
        if overall_score >= self.config['exceptional_threshold']:
            # Verify all components meet minimum requirements
            if all(getattr(metrics, field) >= 0.85 
                  for field in ['combat_score', 'teamfight_contribution', 'game_impact']):
                return "exceptional", min(self.config['max_mmr_gain'],
                                       (overall_score - 0.9) * 50)
        
        # Check excellent tier
        if overall_score >= self.config['excellent_threshold']:
            return "excellent", 0.0
        
        # Check very good tier
        if overall_score >= self.config['very_good_threshold']:
            return "very_good", max(-10, (overall_score - 0.7) * -50)
        
        return "normal", -25.0

    def validate_performance(
        self,
        metrics: ExceptionalMetrics,
        match_data: Dict
    ) -> bool:
        """Validate if performance meets basic requirements"""
        # Check game duration
        if match_data['duration'] < self.config['min_game_duration']:
            return False
            
        # Check teamfight participation
        if metrics.teamfight_contribution < self.config['min_teamfight_participation']:
            return False
            
        # Additional validation logic
        if not self.validate_consistency(metrics):
            return False
            
        return True

    def validate_consistency(self, metrics: ExceptionalMetrics) -> bool:
        """Validate metric consistency to prevent exploitation"""
        # Check for unrealistic disparities between metrics
        metrics_list = [
            metrics.combat_score,
            metrics.farm_efficiency,
            metrics.map_impact,
            metrics.objective_control,
            metrics.teamfight_contribution
        ]
        
        # Calculate standard deviation of metrics
        std_dev = np.std(metrics_list)
        
        # If variance is too high, performance might be suspicious
        if std_dev > 0.3:  # Threshold for acceptable variance
            return False
            
        return True

    def calculate_game_impact(self, metrics: ExceptionalMetrics) -> float:
        """Calculate overall game impact score"""
        weights = {
            'combat': 0.25,
            'farm': 0.15,
            'map_impact': 0.15,
            'objective': 0.15,
            'teamfight': 0.15,
            'vision': 0.08,
            'utility': 0.07
        }
        
        return sum([
            metrics.combat_score * weights['combat'],
            metrics.farm_efficiency * weights['farm'],
            metrics.map_impact * weights['map_impact'],
            metrics.objective_control * weights['objective'],
            metrics.teamfight_contribution * weights['teamfight'],
            metrics.vision_control * weights['vision'],
            metrics.utility_score * weights['utility']
        ])