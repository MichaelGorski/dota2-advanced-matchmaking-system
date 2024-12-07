
__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

# For convenient imports
__all__ = [
    'Player',
    'Match',
    'MetricsCalculator',
    'PerformanceAnalyzer',
    'ExceptionalAnalyzer',
    'MatchMaker'
]

# src/moba_matchmaking/core/__init__.py

__all__ = [
    'Player',
    'Match',
    'MetricsCalculator',
    'GameMetrics'
]

# src/moba_matchmaking/analysis/__init__.py

__all__ = [
    'PerformanceAnalyzer',
    'ExceptionalAnalyzer'
]

# src/moba_matchmaking/matchmaking/__init__.py

__all__ = [
    'MatchMaker',
    'QualityAssessment'
]

# src/moba_matchmaking/utils/__init__.py
from .safety import SafetyChecker
from .logging import MatchLogger

__all__ = [
    'SafetyChecker',
    'MatchLogger'
]