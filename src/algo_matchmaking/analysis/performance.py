from typing import Dict
from dataclasses import dataclass

@dataclass
class PerformanceContext:
    game_state: str  # winning/losing/even
    game_time: int   # minutes
    team_networth: int
    enemy_networth: int
    team_kills: int
    enemy_kills: int
    structures_standing: Dict[str, int]

class PerformanceAnalyzer:
    def __init__(self):
        self.role_expectations = {
            'carry': {
                'early_game': {'gpm': 500, 'xpm': 600, 'lh': 50},
                'mid_game': {'gpm': 650, 'xpm': 750, 'lh': 160},
                'late_game': {'gpm': 800, 'xpm': 850, 'lh': 300}
            },
            'mid': {
                'early_game': {'gpm': 450, 'xpm': 550, 'rotations': 1},
                'mid_game': {'gpm': 600, 'xpm': 700, 'rotations': 3},
                'late_game': {'gpm': 700, 'xpm': 800, 'impact': 0.7}
            },
            'offlane': {
                'early_game': {'gpm': 400, 'xpm': 500, 'space': 0.6},
                'mid_game': {'gpm': 500, 'xpm': 600, 'space': 0.7},
                'late_game': {'gpm': 600, 'xpm': 700, 'impact': 0.6}
            },
            'soft_support': {
                'early_game': {'impact': 0.6, 'rotations': 2},
                'mid_game': {'impact': 0.7, 'vision': 0.7},
                'late_game': {'impact': 0.7, 'saves': 0.6}
            },
            'hard_support': {
                'early_game': {'vision': 0.7, 'harass': 0.6},
                'mid_game': {'vision': 0.8, 'saves': 0.6},
                'late_game': {'vision': 0.8, 'positioning': 0.7}
            }
        }

    def analyze_performance(
        self,
        player: 'Player',
        match_data: Dict,
        context: PerformanceContext
    ) -> Dict:
        """Analyze player performance considering game context"""
        
        phase = self.determine_game_phase(context.game_time)
        role_metrics = self.role_expectations[player.role][phase]
        
        # Calculate base performance metrics
        base_metrics = self.calculate_base_metrics(player, match_data)
        
        # Adjust for game state
        adjusted_metrics = self.adjust_for_game_state(
            base_metrics,
            context,
            player.role
        )
        
        # Calculate impact scores
        impact_scores = self.calculate_impact_scores(
            adjusted_metrics,
            role_metrics,
            context
        )
        
        return {
            'base_metrics': base_metrics,
            'adjusted_metrics': adjusted_metrics,
            'impact_scores': impact_scores,
            'overall_score': self.calculate_overall_score(impact_scores)
        }

    def calculate_base_metrics(self, player: 'Player', match_data: Dict) -> Dict:
        """Calculate base performance metrics"""
        return {
            'kda': (player.stats.kills + player.stats.assists) / 
                   max(1, player.stats.deaths),
            'cs_per_min': player.stats.last_hits / (match_data['duration'] / 60),
            'damage_share': player.stats.damage_dealt / 
                          match_data['team_total_damage'],
            'vision_score': self.calculate_vision_score(player, match_data),
            'objective_score': self.calculate_objective_score(player, match_data)
        }

    def adjust_for_game_state(
        self,
        metrics: Dict,
        context: PerformanceContext,
        role: str
    ) -> Dict:
        """Adjust metrics based on game state"""
        state_multiplier = {
            'winning': 0.9,  # Harder to stand out when winning
            'losing': 1.2,   # Outstanding performance while losing
            'even': 1.0      # Baseline
        }
        
        multiplier = state_multiplier[context.game_state]
        adjusted = {}
        
        for metric, value in metrics.items():
            # Adjust differently based on role and metric
            role_modifier = self.get_role_state_modifier(role, metric)
            adjusted[metric] = value * multiplier * role_modifier
            
        return adjusted

    def calculate_impact_scores(
        self,
        metrics: Dict,
        expectations: Dict,
        context: PerformanceContext
    ) -> Dict:
        """Calculate impact scores relative to expectations"""
        scores = {}
        
        for metric, value in metrics.items():
            if metric in expectations:
                expected = expectations[metric]
                # Higher score for exceeding expectations while losing
                modifier = 1.2 if context.game_state == 'losing' else 1.0
                scores[metric] = min(1.0, (value / expected) * modifier)
            
        return scores

    def determine_game_phase(self, game_time: int) -> str:
        """Determine game phase based on time"""
        if game_time < 15:
            return 'early_game'
        elif game_time < 30:
            return 'mid_game'
        else:
            return 'late_game'
        
    def calculate_vision_score(self, player: 'Player', match_data: Dict) -> float:
        """Calculate vision score based on ward placement, dewarding, and vision uptime"""
        game_duration_minutes = match_data['duration'] / 60
        
        # Calculate ward efficiency
        ward_score = (player.stats.wards_placed / game_duration_minutes) * 0.4
        deward_score = (player.stats.wards_destroyed / game_duration_minutes) * 0.3
        
        # Calculate vision uptime score
        vision_uptime = player.stats.vision_uptime if hasattr(player.stats, 'vision_uptime') else 0.5
        uptime_score = vision_uptime * 0.3
        
        # Combine scores
        total_score = ward_score + deward_score + uptime_score
        
        return min(1.0, total_score)

    def calculate_objective_score(self, player: 'Player', match_data: Dict) -> float:
        """Calculate objective control score based on building damage and objective participation"""
        # Calculate building damage contribution
        team_building_damage = match_data.get('team_building_damage', 1)  # Avoid division by zero
        building_damage_share = player.stats.building_damage / team_building_damage
        
        # Calculate objective participation
        objective_participation = getattr(player.stats, 'objective_participation', 0.5)
        
        # Calculate Roshan participation
        roshan_participation = getattr(player.stats, 'roshan_participation', 0.0)
        
        # Weight the components
        score = (
            building_damage_share * 0.4 +
            objective_participation * 0.4 +
            roshan_participation * 0.2
        )
        
        return min(1.0, score)

    def get_role_state_modifier(self, role: str, metric: str) -> float:
        """Get role-specific state modifier for different metrics"""
        role_modifiers = {
            'carry': {
                'kda': 1.0,
                'cs_per_min': 1.2,
                'damage_share': 1.1,
                'vision_score': 0.8,
                'objective_score': 1.1
            },
            'mid': {
                'kda': 1.1,
                'cs_per_min': 1.0,
                'damage_share': 1.1,
                'vision_score': 0.9,
                'objective_score': 1.0
            },
            'offlane': {
                'kda': 0.9,
                'cs_per_min': 0.8,
                'damage_share': 1.0,
                'vision_score': 1.0,
                'objective_score': 1.2
            },
            'soft_support': {
                'kda': 0.8,
                'cs_per_min': 0.6,
                'damage_share': 0.8,
                'vision_score': 1.2,
                'objective_score': 0.9
            },
            'hard_support': {
                'kda': 0.7,
                'cs_per_min': 0.5,
                'damage_share': 0.7,
                'vision_score': 1.3,
                'objective_score': 0.8
            }
        }
        
        return role_modifiers.get(role, {}).get(metric, 1.0)

    def calculate_overall_score(self, impact_scores: Dict) -> float:
        """Calculate overall performance score from impact scores"""
        weights = {
            'kda': 0.2,
            'cs_per_min': 0.15,
            'damage_share': 0.25,
            'vision_score': 0.2,
            'objective_score': 0.2
        }
        
        # Calculate weighted sum
        total_score = 0.0
        total_weight = 0.0
        
        for metric, score in impact_scores.items():
            weight = weights.get(metric, 0.0)
            total_score += score * weight
            total_weight += weight
        
        # Normalize if we don't have all metrics
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 0.0
            
        return min(1.0, final_score)