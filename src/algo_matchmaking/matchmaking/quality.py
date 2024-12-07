from typing import Dict, List, Optional, Tuple
import numpy as np
from src.algo_matchmaking.core.player import Player

class QualityAssessment:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self.default_config()
        
    def default_config(self) -> Dict:
        return {
            'min_role_synergy': 0.6,
            'min_hero_synergy': 0.5,
            'min_skill_balance': 0.7,
            'min_communication': 0.6
        }

    def assess_match_quality(
        self,
        team1: List['Player'],
        team2: List['Player']
    ) -> Dict[str, float]:
        """Comprehensive match quality assessment"""
        quality_metrics = {
            'role_balance': self.assess_role_balance(team1, team2),
            'skill_balance': self.assess_skill_balance(team1, team2),
            'hero_synergy': self.assess_hero_synergy(team1, team2),
            'team_chemistry': self.assess_team_chemistry(team1, team2),
            'playstyle_compatibility': self.assess_playstyle_compatibility(team1, team2)
        }
        
        return {
            'metrics': quality_metrics,
            'overall_score': self.calculate_overall_quality(quality_metrics)
        }

    def assess_role_balance(
        self,
        team1: List['Player'],
        team2: List['Player']
    ) -> float:
        """Assess how well roles are balanced between teams"""
        def get_role_strength(team: List['Player'], role: str) -> float:
            players = [p for p in team if role in p.preferred_roles]
            if not players:
                return 0.0
            return max(p.role_ratings[role] for p in players)

        roles = ['carry', 'mid', 'offlane', 'soft_support', 'hard_support']
        role_differences = []

        for role in roles:
            team1_strength = get_role_strength(team1, role)
            team2_strength = get_role_strength(team2, role)
            role_differences.append(abs(team1_strength - team2_strength))

        return 1.0 - min(1.0, sum(role_differences) / (1000 * len(roles)))

    def assess_skill_balance(
        self,
        team1: List['Player'],
        team2: List['Player']
    ) -> float:
        """Assess skill balance between teams"""
        team1_skills = [p.mmr for p in team1]
        team2_skills = [p.mmr for p in team2]
        
        # Compare average MMR
        avg_diff = abs(np.mean(team1_skills) - np.mean(team2_skills))
        
        # Compare skill distribution
        std_diff = abs(np.std(team1_skills) - np.std(team2_skills))
        
        return 1.0 - min(1.0, (avg_diff / 500 + std_diff / 200) / 2)

    def assess_playstyle_compatibility(
        self,
        team1: List['Player'],
        team2: List['Player']
    ) -> float:
        """Assess if teams have compatible playstyles"""
        def get_team_playstyle(team: List['Player']) -> Dict[str, float]:
            return {
                'aggression': np.mean([p.stats.damage_dealt/p.stats.gpm 
                                     for p in team]),
                'objective_focus': np.mean([p.stats.building_damage/p.stats.damage_dealt 
                                          for p in team]),
                'teamfight': np.mean([p.stats.teamfight_participation 
                                    for p in team])
            }
        
        team1_style = get_team_playstyle(team1)
        team2_style = get_team_playstyle(team2)
        
        # Calculate style compatibility
        style_diff = sum(abs(team1_style[k] - team2_style[k]) 
                        for k in team1_style) / len(team1_style)
        
        return 1.0 - min(1.0, style_diff)

    def calculate_overall_quality(self, metrics: Dict[str, float]) -> float:
        """Calculate overall match quality score"""
        weights = {
            'role_balance': 0.25,
            'skill_balance': 0.25,
            'hero_synergy': 0.2,
            'team_chemistry': 0.15,
            'playstyle_compatibility': 0.15
        }
        
        return sum(metrics[key] * weights[key] for key in weights)