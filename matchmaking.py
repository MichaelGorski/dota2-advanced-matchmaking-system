class TeamSynergyMetrics:
    def __init__(self):
        self.support_enabling_factors = {
            'lane_control': 0,      # Harass, pulls, stacks
            'vision_impact': 0,     # Vision leading to core survival
            'space_creation': 0,    # Rotations that allow core farming
            'save_frequency': 0,    # Successful saves of cores
            'item_timing_enable': 0 # Supporting core item timings
        }
        
        self.core_utilization = {
            'space_usage': 0,       # Efficiency in using space created
            'vision_usage': 0,      # Kills/escapes from support vision
            'stack_farming': 0,     # Efficiency in farming stacks
            'team_play': 0,        # Fighting when team is ready
            'resource_sharing': 0   # Leaving farm for position priority
        }
        
        self.team_coordination = {
            'smoke_coordination': 0, # Successful smoke ganks
            'objective_timing': 0,   # Taking objectives at power spikes
            'rosh_timing': 0,       # Roshan attempts at team peaks
            'defense_coordination': 0,# Coordinated base defense
            'push_timing': 0        # Pushing when team is strongest
        }

class EnhancedMatchmaking:
    def __init__(self):
        self.target_metrics = {
            'game_quality': 0.0,    # Overall game satisfaction
            'role_performance': 0.0, # Role fulfillment rating
            'team_synergy': 0.0,    # Team coordination rating
            'skill_balance': 0.0    # Skill matchup fairness
        }
        
    def find_optimal_match(self, player_pool):
        best_matches = []
        
        for potential_match in generate_match_combinations(player_pool):
            match_quality = self.evaluate_match_quality(potential_match)
            if match_quality.game_quality > 0.8:  # High quality threshold
                best_matches.append((match_quality, potential_match))
        
        return self.select_best_match(best_matches)
    
    def evaluate_match_quality(self, match):
        team1, team2 = match
        quality = MatchQuality()
        
        # Evaluate team compositions
        quality.role_synergy = evaluate_role_synergy(team1, team2)
        quality.playstyle_compatibility = evaluate_playstyle_fit(team1, team2)
        
        # Check skill balance without forcing 50/50
        quality.skill_balance = evaluate_skill_balance(team1, team2)
        
        # Evaluate potential for good game
        quality.game_potential = evaluate_game_potential(team1, team2)
        
        return quality

def evaluate_carry_performance(game_data, player):
    """Evaluate carry performance considering support enabling"""
    metrics = CarryMetrics()
    
    # Base performance
    metrics.farm_efficiency = calculate_farm_efficiency(game_data, player)
    metrics.fight_impact = calculate_fight_impact(game_data, player)
    
    # Support-enabled performance
    support_impact = calculate_support_impact(game_data, player)
    
    # Adjust metrics based on support impact
    adjusted_metrics = adjust_carry_metrics(metrics, support_impact)
    
    return adjusted_metrics

def calculate_support_impact(game_data, player):
    """Calculate how much supports enabled the carry"""
    impact = SupportImpact()
    
    # Vision impact
    impact.vision = sum(ward.value_generated for ward in game_data.wards
                       if ward.beneficiary == player)
    
    # Lane support
    impact.lane = calculate_lane_support(game_data, player)
    
    # Stack impact
    impact.stacks = calculate_stack_value(game_data, player)
    
    # Save impact
    impact.saves = calculate_save_value(game_data, player)
    
    return impact

def calculate_team_contribution(game_data, player):
    """Calculate how player's actions benefited team"""
    contribution = TeamContribution()
    
    # Space creation
    contribution.space = calculate_space_created(game_data, player)
    
    # Objective setup
    contribution.objectives = calculate_objective_contribution(game_data, player)
    
    # Team fight setup
    contribution.teamfight = calculate_teamfight_contribution(game_data, player)
    
    return contribution

class MatchQuality:
    def __init__(self):
        self.game_factors = {
            'draft_synergy': 0.0,    # How well heroes work together
            'timing_windows': 0.0,    # Team power spike alignment
            'playstyle_match': 0.0,   # Compatible playstyles
            'communication': 0.0,     # Team communication history
            'role_comfort': 0.0       # Players in preferred roles
        }
        
        self.skill_factors = {
            'mechanical_skill': 0.0,  # Raw mechanical ability
            'strategic_skill': 0.0,   # Game understanding
            'role_skill': 0.0,        # Role-specific skill
            'hero_proficiency': 0.0   # Hero pool compatibility
        }
        
        self.environmental_factors = {
            'ping_balance': 0.0,      # Server connection quality
            'language_match': 0.0,    # Communication capability
            'behavior_score': 0.0,    # Player conduct alignment
            'party_balance': 0.0      # Party size balance
        }

def calculate_mmr_adjustment(player, game_data):
    """Calculate MMR change with comprehensive factors"""
    base_mmr = 25
    
    # Victory/Loss base (-80%)
    game_outcome = 0.8 * (base_mmr if game_data.victory else -base_mmr)
    
    # Performance metrics (20%)
    performance = calculate_performance_score(player, game_data)
    performance_modifier = 0.2 * (performance - 0.5) * base_mmr
    
    # Additional modifiers
    team_play = calculate_team_play_bonus(player, game_data)
    role_execution = calculate_role_execution(player, game_data)
    behavior_modifier = calculate_behavior_modifier(player, game_data)
    
    # Final MMR change
    mmr_change = (game_outcome + performance_modifier) * \
                 (1 + team_play) * \
                 (1 + role_execution) * \
                 behavior_modifier
    
    return mmr_change

def find_balanced_match(player_pool):
    """Find match without forcing 50/50 win rate"""
    matches = []
    
    for potential_match in generate_potential_matches(player_pool):
        quality = evaluate_match_quality(potential_match)
        if quality.score > QUALITY_THRESHOLD:
            matches.append((quality, potential_match))
    
    # Sort by quality, not by forcing win rates
    matches.sort(key=lambda x: x[0].score, reverse=True)
    return matches[0] if matches else None