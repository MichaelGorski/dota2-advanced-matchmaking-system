
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import itertools
import numpy as np
from datetime import datetime

@dataclass
class MatchQuality:
    team_balance: float
    role_synergy: float
    skill_distribution: float
    communication_compatibility: float
    hero_synergy: float
    overall_score: float

class MatchMaker:
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self.default_config()
        self.player_pool = []
        self.recent_matches = []
        self.quality_threshold = 0.8

    def default_config(self) -> Dict:
        return {
            'team_size': 5,
            'max_mmr_spread': 1000,
            'min_quality_threshold': 0.8,
            'role_importance': 0.3,
            'skill_importance': 0.3,
            'synergy_importance': 0.2,
            'communication_importance': 0.2
        }

    def find_match(self) -> Optional['Match']:
        """Find the best possible match from current player pool"""
        if len(self.player_pool) < self.config['team_size'] * 2:
            return None

        best_match = None
        best_quality = 0.0

        # Generate all possible team combinations
        possible_matches = self.generate_possible_matches()

        for match in possible_matches:
            quality = self.evaluate_match_quality(match)
            if quality.overall_score > best_quality and \
               quality.overall_score >= self.quality_threshold:
                best_quality = quality.overall_score
                best_match = match

        if best_match:
            self.remove_players_from_pool(best_match)
            self.recent_matches.append(best_match)

        return best_match

    def generate_possible_matches(self) -> List['Match']:
        """Generate all possible valid team combinations"""
        team_size = self.config['team_size']
        possible_matches = []

        # Get all possible player combinations for team size
        player_combinations = list(itertools.combinations(
            self.player_pool, 
            team_size * 2
        ))

        for players in player_combinations:
            # Try different team splits
            for team_split in self.generate_team_splits(players):
                if self.is_valid_team_composition(team_split[0]) and \
                   self.is_valid_team_composition(team_split[1]):
                    possible_matches.append(
                        Match(
                            team1=team_split[0],
                            team2=team_split[1]
                        )
                    )

        return possible_matches

    def evaluate_match_quality(self, match: 'Match') -> MatchQuality:
        """Evaluate the quality of a potential match"""
        # Calculate various quality metrics
        team_balance = self.calculate_team_balance(match)
        role_synergy = self.calculate_role_synergy(match)
        skill_distribution = self.calculate_skill_distribution(match)
        communication = self.evaluate_communication_compatibility(match)
        hero_synergy = self.calculate_hero_synergy(match)

        # Weight the different factors
        overall_score = (
            team_balance * self.config['skill_importance'] +
            role_synergy * self.config['role_importance'] +
            skill_distribution * self.config['skill_importance'] +
            communication * self.config['communication_importance'] +
            hero_synergy * self.config['synergy_importance']
        )

        return MatchQuality(
            team_balance=team_balance,
            role_synergy=role_synergy,
            skill_distribution=skill_distribution,
            communication_compatibility=communication,
            hero_synergy=hero_synergy,
            overall_score=overall_score
        )

    def calculate_team_balance(self, match: 'Match') -> float:
        """Calculate how well balanced the teams are"""
        team1_mmr = self.calculate_team_mmr(match.team1)
        team2_mmr = self.calculate_team_mmr(match.team2)
        
        # Calculate MMR difference and normalize
        mmr_difference = abs(team1_mmr - team2_mmr)
        balance_score = max(0, 1 - (mmr_difference / self.config['max_mmr_spread']))
        
        return balance_score

    def is_valid_team_composition(self, team: List['Player']) -> bool:
        """Check if team composition is valid"""
        if len(team) != self.config['team_size']:
            return False
            
        # Check if all roles can be filled
        required_roles = {'carry', 'mid', 'offlane', 'soft_support', 'hard_support'}
        available_roles = set()
        for player in team:
            available_roles.update(player.preferred_roles)
            
        return required_roles.issubset(available_roles)