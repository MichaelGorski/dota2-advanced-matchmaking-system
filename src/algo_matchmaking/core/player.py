from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class PlayerStats:
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    last_hits: int = 0
    denies: int = 0
    gpm: float = 0
    xpm: float = 0
    damage_dealt: int = 0
    damage_taken: int = 0
    healing: int = 0
    building_damage: int = 0
    vision_score: float = 0
    teamfight_participation: float = 0

class Player:
    def __init__(self, id: str, initial_mmr: int = 2000):
        self.id = id
        self.mmr = initial_mmr
        self.role_ratings = {
            'carry': initial_mmr,
            'mid': initial_mmr,
            'offlane': initial_mmr,
            'soft_support': initial_mmr,
            'hard_support': initial_mmr
        }
        self.preferred_roles: List[str] = []
        self.hero_pool: Dict[int, int] = {}  # hero_id: games_played
        self.recent_matches: List[int] = []   # match_ids
        self.behavior_score: int = 10000
        self.stats = PlayerStats()
        self.last_update: datetime = datetime.now()
        self.tilt_factor: float = 0.0
        self.performance_history: List[Dict] = []

    def update_mmr(self, change: int, role: str):
        """Update MMR for specific role"""
        self.role_ratings[role] += change
        self.mmr = max(self.role_ratings.values())  # Main MMR is highest role MMR
        
    def add_match_performance(self, match_data: Dict):
        """Add match performance to history"""
        self.performance_history.append(match_data)
        if len(self.performance_history) > 20:  # Keep last 20 matches
            self.performance_history.pop(0)

    def calculate_tilt(self) -> float:
        """Calculate current tilt factor based on recent performance"""
        if not self.performance_history:
            return 0.0
            
        recent_losses = sum(1 for match in self.performance_history[-5:]
                          if not match.get('victory', False))
        return min(1.0, recent_losses * 0.2)