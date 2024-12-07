from dataclasses import dataclass
from typing import Dict


@dataclass
class GameMetrics:
    """Core game metrics tracked for each match"""
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    last_hits: int = 0
    denies: int = 0
    gpm: float = 0.0
    xpm: float = 0.0
    hero_damage: int = 0
    tower_damage: int = 0
    hero_healing: int = 0
    stun_duration: float = 0.0
    camps_stacked: int = 0
    runes_collected: int = 0
    wards_placed: int = 0
    wards_destroyed: int = 0
    teamfight_participation: float = 0.0


class MetricsCalculator:
    """Calculates various performance metrics from game data"""
    
    def __init__(self):
        self.role_weights = {
            'carry': {
                'farm_efficiency': 0.3,
                'damage_output': 0.3,
                'survival': 0.2,
                'objective_focus': 0.2
            },
            'mid': {
                'farm_efficiency': 0.25,
                'damage_output': 0.3,
                'map_presence': 0.25,
                'objective_focus': 0.2
            },
            'offlane': {
                'space_creation': 0.3,
                'survival': 0.25,
                'damage_output': 0.25,
                'objective_focus': 0.2
            },
            'soft_support': {
                'map_presence': 0.3,
                'utility': 0.3,
                'teamfight_impact': 0.2,
                'vision_control': 0.2
            },
            'hard_support': {
                'vision_control': 0.3,
                'utility': 0.3,
                'survival': 0.2,
                'teamfight_impact': 0.2
            }
        }

    def calculate_farming_efficiency(
        self,
        metrics: GameMetrics,
        game_duration: int,
        role: str
    ) -> float:
        """Calculate farming efficiency score"""
        minutes = game_duration / 60
        
        # Base expectations per role
        role_expectations = {
            'carry': {'cs': 10, 'gpm': 600},
            'mid': {'cs': 8, 'gpm': 550},
            'offlane': {'cs': 6, 'gpm': 450},
            'soft_support': {'cs': 2, 'gpm': 300},
            'hard_support': {'cs': 1, 'gpm': 250}
        }
        
        expected = role_expectations[role]
        cs_score = min(1.0, metrics.last_hits / (expected['cs'] * minutes))
        gpm_score = min(1.0, metrics.gpm / expected['gpm'])
        
        return (cs_score + gpm_score) / 2

    def calculate_combat_efficiency(
        self,
        metrics: GameMetrics,
        team_damage: int,
        role: str
    ) -> float:
        """Calculate combat efficiency score"""
        # Calculate damage share
        damage_share = metrics.hero_damage / max(1, team_damage)
        
        # Calculate KDA ratio
        kda = (metrics.kills + metrics.assists) / max(1, metrics.deaths)
        
        # Role-specific expectations
        role_damage_expectations = {
            'carry': 0.35,
            'mid': 0.30,
            'offlane': 0.20,
            'soft_support': 0.10,
            'hard_support': 0.05
        }
        
        damage_score = min(1.0, damage_share / role_damage_expectations[role])
        kda_score = min(1.0, kda / 4)  # Normalize KDA
        
        return (damage_score * 0.6 + kda_score * 0.4)

    def calculate_vision_score(
        self,
        metrics: GameMetrics,
        game_duration: int
    ) -> float:
        """Calculate vision control score"""
        minutes = game_duration / 60
        
        # Calculate ward efficiency
        ward_score = (metrics.wards_placed / minutes) * 0.6 + \
                    (metrics.wards_destroyed / minutes) * 0.4
                    
        return min(1.0, ward_score / 2)  # Normalize to 0-1

    def calculate_utility_score(
        self,
        metrics: GameMetrics,
        team_fights: int
    ) -> float:
        """Calculate utility contribution score"""
        # Evaluate stun efficiency
        stun_score = min(1.0, metrics.stun_duration / (team_fights * 5))
        
        # Evaluate healing efficiency
        healing_score = min(1.0, metrics.hero_healing / 5000)
        
        # Evaluate teamfight participation
        teamfight_score = min(1.0, metrics.teamfight_participation)
        
        return (stun_score * 0.4 + healing_score * 0.3 + teamfight_score * 0.3)

    def calculate_survival_score(
        self,
        metrics: GameMetrics,
        game_duration: int,
        role: str
    ) -> float:
        """Calculate survival score based on deaths and game time"""
        minutes = game_duration / 60
        
        # Role-specific death thresholds per minute
        role_death_thresholds = {
            'carry': 0.12,      # ~1 death per 8 minutes
            'mid': 0.14,        # ~1 death per 7 minutes
            'offlane': 0.16,    # ~1 death per 6 minutes
            'soft_support': 0.2, # ~1 death per 5 minutes
            'hard_support': 0.25 # ~1 death per 4 minutes
        }
        
        death_rate = metrics.deaths / minutes
        threshold = role_death_thresholds[role]
        
        # Calculate base survival score
        survival_score = max(0, 1 - (death_rate / threshold))
        
        # Adjust for high-impact deaths (if data available)
        if hasattr(metrics, 'death_impact_score'):
            survival_score *= (1 + metrics.death_impact_score)
        
        return min(1.0, survival_score)

    def calculate_map_presence(
        self,
        metrics: GameMetrics,
        game_data: Dict
    ) -> float:
        """Calculate map presence and rotation effectiveness"""
        # Base metrics from teleport usage
        tp_score = min(1.0, game_data.get('teleports_used', 0) / 10)
        
        # Participation in kills across different lanes
        lane_participation = game_data.get('lane_participation', {})
        lane_presence = sum(lane_participation.values()) / 3  # Average across lanes
        
        # Movement between objectives
        objective_presence = game_data.get('objective_presence', 0.5)
        
        return (tp_score * 0.3 + lane_presence * 0.4 + objective_presence * 0.3)

    def calculate_space_creation(
        self,
        metrics: GameMetrics,
        game_data: Dict
    ) -> float:
        """Calculate space creation score"""
        # Attention drawn from enemies
        attention_score = game_data.get('enemy_attention_score', 0.5)
        
        # Tower pressure created
        tower_pressure = metrics.tower_damage / max(1, game_data['duration'])
        
        # Enemy rotations forced
        rotations_forced = game_data.get('rotations_forced', 0) / 10
        
        # Combine scores
        space_score = (
            attention_score * 0.4 +
            min(1.0, tower_pressure / 100) * 0.3 +
            min(1.0, rotations_forced) * 0.3
        )
        
        return min(1.0, space_score)

    def calculate_objective_focus(
        self,
        metrics: GameMetrics,
        game_data: Dict
    ) -> float:
        """Calculate objective focus score"""
        # Tower damage contribution
        tower_contribution = metrics.tower_damage / max(1, game_data.get('team_tower_damage', 1))
        
        # Roshan participation
        roshan_score = game_data.get('roshan_participation', 0.0)
        
        # Objective control (outposts, bounties)
        objective_control = game_data.get('objective_control', 0.0)
        
        # Combine scores
        return (
            tower_contribution * 0.5 +
            roshan_score * 0.3 +
            objective_control * 0.2
        )

    def calculate_teamfight_impact(
        self,
        metrics: GameMetrics,
        game_data: Dict
    ) -> float:
        """Calculate teamfight impact score"""
        # Participation score
        participation = metrics.teamfight_participation
        
        # Impact during fights
        fight_impact = game_data.get('teamfight_damage_share', 0.0)
        
        # Utility during fights (stuns, slows, etc.)
        utility_impact = (metrics.stun_duration / 
                        max(1, game_data.get('total_fight_duration', 1)))
        
        return (
            participation * 0.4 +
            fight_impact * 0.3 +
            utility_impact * 0.3
        )

    def calculate_overall_performance(
        self,
        metrics: GameMetrics,
        game_data: Dict,
        role: str
    ) -> Dict[str, float]:
        """Calculate overall performance metrics"""
        # Calculate all possible scores
        base_scores = {
            'farm_efficiency': self.calculate_farming_efficiency(
                metrics, 
                game_data['duration'], 
                role
            ),
            'damage_output': self.calculate_combat_efficiency(
                metrics,
                game_data['team_damage'],
                role
            ),
            'vision_control': self.calculate_vision_score(
                metrics,
                game_data['duration']
            ),
            'utility': self.calculate_utility_score(
                metrics,
                game_data['team_fights']
            ),
            'survival': self.calculate_survival_score(
                metrics,
                game_data['duration'],
                role
            ),
            'map_presence': self.calculate_map_presence(
                metrics,
                game_data
            ),
            'space_creation': self.calculate_space_creation(
                metrics,
                game_data
            ),
            'objective_focus': self.calculate_objective_focus(
                metrics,
                game_data
            ),
            'teamfight_impact': self.calculate_teamfight_impact(
                metrics,
                game_data
            )
        }
        
        # Apply role-specific weights
        weights = self.role_weights[role]
        final_score = sum(
            base_scores[metric] * weight
            for metric, weight in weights.items()
        )
        
        return {
            'detailed_scores': base_scores,
            'overall_score': final_score,
            'weighted_scores': {
                metric: base_scores[metric] * weight
                for metric, weight in weights.items()
            }
        }