from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
from src.algo_matchmaking.core.player import Player

@dataclass
class TeamComposition:
    players: List[Player]
    total_mmr: int
    roles: Dict[str, Player]
    hero_synergy: float
    communication_rating: float

class Match:
    def __init__(self, team1: TeamComposition, team2: TeamComposition):
        self.team1 = team1
        self.team2 = team2
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.winner: Optional[str] = None
        self.match_quality: float = 0.0
        self.events: List[Dict] = []
        self.metrics: Dict = {}

    def start_match(self):
        """Initialize match start"""
        self.start_time = datetime.now()
        self.initialize_metrics()

    def end_match(self, winner: str):
        """Record match end and winner"""
        self.end_time = datetime.now()
        self.winner = winner
        self.calculate_final_metrics()

    def add_event(self, event: Dict):
        """Add game event to match history"""
        self.events.append({
            'timestamp': datetime.now(),
            **event
        })

    def calculate_final_metrics(self):
        """Calculate final match metrics"""
        self.metrics['duration'] = (self.end_time - self.start_time).seconds
        self.metrics['quality'] = self.calculate_match_quality()
        self.metrics['balance'] = self.calculate_team_balance()
        self.calculate_player_performances()
