"""
Gamification System - Engaging health tracking through points, badges, and challenges
specifically designed for Kenyan health and cultural context.
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import json

class BadgeType(Enum):
    CONSISTENCY = "consistency"
    HEALTH_GOALS = "health_goals"
    KENYAN_CULTURE = "kenyan_culture"
    SOCIAL = "social"
    EDUCATION = "education"
    MILESTONE = "milestone"

class ChallengeType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    SEASONAL = "seasonal"

@dataclass
class Badge:
    id: str
    name_english: str
    name_swahili: str
    description_english: str
    description_swahili: str
    badge_type: BadgeType
    icon: str
    points_value: int
    requirements: Dict
    rarity: str  # common, rare, epic, legendary

@dataclass
class Challenge:
    id: str
    name_english: str
    name_swahili: str
    description_english: str
    description_swahili: str
    challenge_type: ChallengeType
    start_date: datetime
    end_date: datetime
    target_value: float
    current_progress: float
    points_reward: int
    badge_reward: Optional[str]
    participants: List[str]
    is_active: bool

@dataclass
class UserProgress:
    user_id: str
    total_points: int
    level: int
    badges_earned: List[str]
    challenges_completed: List[str]
    current_challenges: List[str]
    streak_days: int
    last_activity: datetime
    achievements: Dict

class HealthGamification:
    """Comprehensive gamification system for health tracking"""
    
    def __init__(self):
        self.badges = self._initialize_badges()
        self.challenges = self._initialize_challenges()
        self.user_progress = {}  # In real app, this would be in database
        self.level_thresholds = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500, 7500]
    
    def _initialize_badges(self) -> List[Badge]:
        """Initialize all available badges"""
        return [
            # CONSISTENCY BADGES
            Badge(
                id="first_steps",
                name_english="First Steps",
                name_swahili="Hatua za Kwanza",
                description_english="Log your first health reading",
                description_swahili="Rekodi kipimo chako cha kwanza cha afya",
                badge_type=BadgeType.CONSISTENCY,
                icon="🌱",
                points_value=50,
                requirements={"readings_logged": 1},
                rarity="common"
            ),
            
            Badge(
                id="week_warrior",
                name_english="Week Warrior",
                name_swahili="Shujaa wa Wiki",
                description_english="Log health data for 7 consecutive days",
                description_swahili="Rekodi data ya afya kwa siku 7 mfululizo",
                badge_type=BadgeType.CONSISTENCY,
                icon="⚡",
                points_value=200,
                requirements={"consecutive_days": 7},
                rarity="rare"
            ),
            
            Badge(
                id="month_master",
                name_english="Month Master",
                name_swahili="Bwana wa Mwezi",
                description_english="Maintain daily logging for 30 days",
                description_swahili="Endelea kurekodi kila siku kwa siku 30",
                badge_type=BadgeType.CONSISTENCY,
                icon="👑",
                points_value=500,
                requirements={"consecutive_days": 30},
                rarity="epic"
            ),
            
            # KENYAN CULTURE BADGES
            Badge(
                id="ugali_master",
                name_english="Ugali Master",
                name_swahili="Bwana Ugali",
                description_english="Track 10 traditional Kenyan meals",
                description_swahili="Fuatilia vyakula 10 vya kitamaduni vya Kenya",
                badge_type=BadgeType.KENYAN_CULTURE,
                icon="🌽",
                points_value=150,
                requirements={"kenyan_foods_logged": 10},
                rarity="rare"
            ),
            
            Badge(
                id="sukuma_wiki_champion",
                name_english="Sukuma Wiki Champion",
                name_swahili="Bingwa wa Sukuma Wiki",
                description_english="Eat sukuma wiki 15 times this month",
                description_swahili="Kula sukuma wiki mara 15 mwezi huu",
                badge_type=BadgeType.KENYAN_CULTURE,
                icon="🥬",
                points_value=100,
                requirements={"sukuma_wiki_count": 15, "timeframe": "month"},
                rarity="common"
            ),
            
            Badge(
                id="githeri_guru",
                name_english="Githeri Guru",
                name_swahili="Mkuu wa Githeri",
                description_english="Choose githeri over high-GI foods 5 times",
                description_swahili="Chagua githeri badala ya vyakula vya GI ya juu mara 5",
                badge_type=BadgeType.KENYAN_CULTURE,
                icon="🫘",
                points_value=120,
                requirements={"healthy_substitutions": 5},
                rarity="common"
            ),
            
            # HEALTH GOALS BADGES
            Badge(
                id="glucose_guardian",
                name_english="Glucose Guardian",
                name_swahili="Mlinzi wa Sukari",
                description_english="Keep glucose in target range for 5 days",
                description_swahili="Weka sukari katika kiwango cha lengo kwa siku 5",
                badge_type=BadgeType.HEALTH_GOALS,
                icon="🎯",
                points_value=300,
                requirements={"glucose_in_range_days": 5},
                rarity="epic"
            ),
            
            Badge(
                id="fiber_friend",
                name_english="Fiber Friend",
                name_swahili="Rafiki wa Nyuzi",
                description_english="Consume 25g+ fiber daily for a week",
                description_swahili="Tumia nyuzi 25g+ kila siku kwa wiki",
                badge_type=BadgeType.HEALTH_GOALS,
                icon="🌾",
                points_value=200,
                requirements={"daily_fiber_g": 25, "consecutive_days": 7},
                rarity="rare"
            ),
            
            # SOCIAL BADGES
            Badge(
                id="community_helper",
                name_english="Community Helper",
                name_swahili="Msaidizi wa Jamii",
                description_english="Share 3 healthy recipes with friends",
                description_swahili="Shiriki mapishi 3 mazuri na marafiki",
                badge_type=BadgeType.SOCIAL,
                icon="🤝",
                points_value=150,
                requirements={"recipes_shared": 3},
                rarity="rare"
            ),
            
            # EDUCATION BADGES
            Badge(
                id="diabetes_scholar",
                name_english="Diabetes Scholar",
                name_swahili="Mwanafunzi wa Kisukari",
                description_english="Complete 5 diabetes education modules",
                description_swahili="Maliza moduli 5 za elimu ya kisukari",
                badge_type=BadgeType.EDUCATION,
                icon="📚",
                points_value=250,
                requirements={"education_modules": 5},
                rarity="epic"
            ),
            
            # MILESTONE BADGES
            Badge(
                id="thousand_club",
                name_english="Thousand Club",
                name_swahili="Klabu ya Elfu",
                description_english="Earn 1000 total points",
                description_swahili="Pata jumla ya pointi 1000",
                badge_type=BadgeType.MILESTONE,
                icon="💎",
                points_value=0,  # No additional points for milestone
                requirements={"total_points": 1000},
                rarity="legendary"
            )
        ]
    
    def _initialize_challenges(self) -> List[Challenge]:
        """Initialize sample challenges"""
        now = datetime.now()
        return [
            Challenge(
                id="daily_reading",
                name_english="Daily Health Check",
                name_swahili="Uchunguzi wa Afya wa Kila Siku",
                description_english="Log at least one health reading today",
                description_swahili="Rekodi angalau kipimo kimoja cha afya leo",
                challenge_type=ChallengeType.DAILY,
                start_date=now.replace(hour=0, minute=0, second=0),
                end_date=now.replace(hour=23, minute=59, second=59),
                target_value=1,
                current_progress=0,
                points_reward=25,
                badge_reward=None,
                participants=[],
                is_active=True
            ),
            
            Challenge(
                id="kenyan_foods_week",
                name_english="Kenyan Foods Week",
                name_swahili="Wiki ya Vyakula vya Kenya",
                description_english="Try 5 different traditional Kenyan foods this week",
                description_swahili="Jaribu vyakula 5 tofauti vya kitamaduni vya Kenya wiki hii",
                challenge_type=ChallengeType.WEEKLY,
                start_date=now - timedelta(days=now.weekday()),
                end_date=now - timedelta(days=now.weekday()) + timedelta(days=6),
                target_value=5,
                current_progress=0,
                points_reward=150,
                badge_reward="ugali_master",
                participants=[],
                is_active=True
            ),
            
            Challenge(
                id="glucose_stability",
                name_english="Glucose Stability Challenge",
                name_swahili="Changamoto ya Uthabiti wa Sukari",
                description_english="Keep glucose readings within target range for 2 weeks",
                description_swahili="Weka vipimo vya sukari katika kiwango cha lengo kwa wiki 2",
                challenge_type=ChallengeType.WEEKLY,
                start_date=now,
                end_date=now + timedelta(days=14),
                target_value=14,
                current_progress=0,
                points_reward=400,
                badge_reward="glucose_guardian",
                participants=[],
                is_active=True
            )
        ]
    
    def get_user_progress(self, user_id: str) -> UserProgress:
        """Get user's gamification progress"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = UserProgress(
                user_id=user_id,
                total_points=0,
                level=1,
                badges_earned=[],
                challenges_completed=[],
                current_challenges=[],
                streak_days=0,
                last_activity=datetime.now(),
                achievements={}
            )
        return self.user_progress[user_id]
    
    def award_points(self, user_id: str, points: int, reason: str) -> Dict:
        """Award points to user and check for level ups"""
        progress = self.get_user_progress(user_id)
        old_level = progress.level
        
        progress.total_points += points
        progress.last_activity = datetime.now()
        
        # Check for level up
        new_level = self._calculate_level(progress.total_points)
        level_up = new_level > old_level
        
        if level_up:
            progress.level = new_level
        
        # Check for milestone badges
        self._check_milestone_badges(user_id)
        
        return {
            'points_awarded': points,
            'total_points': progress.total_points,
            'old_level': old_level,
            'new_level': progress.level,
            'level_up': level_up,
            'reason': reason
        }
    
    def _calculate_level(self, total_points: int) -> int:
        """Calculate user level based on total points"""
        for level, threshold in enumerate(self.level_thresholds):
            if total_points < threshold:
                return level
        return len(self.level_thresholds)
    
    def check_badge_eligibility(self, user_id: str, activity_data: Dict) -> List[Badge]:
        """Check if user is eligible for any badges"""
        progress = self.get_user_progress(user_id)
        earned_badges = []
        
        for badge in self.badges:
            if badge.id in progress.badges_earned:
                continue  # Already earned
            
            if self._meets_badge_requirements(badge, activity_data, progress):
                progress.badges_earned.append(badge.id)
                progress.total_points += badge.points_value
                earned_badges.append(badge)
        
        return earned_badges
    
    def _meets_badge_requirements(self, badge: Badge, activity_data: Dict, progress: UserProgress) -> bool:
        """Check if user meets badge requirements"""
        requirements = badge.requirements
        
        for req_key, req_value in requirements.items():
            if req_key == "readings_logged":
                if activity_data.get("total_readings", 0) < req_value:
                    return False
            elif req_key == "consecutive_days":
                if progress.streak_days < req_value:
                    return False
            elif req_key == "kenyan_foods_logged":
                if activity_data.get("kenyan_foods_count", 0) < req_value:
                    return False
            elif req_key == "glucose_in_range_days":
                if activity_data.get("glucose_in_range_days", 0) < req_value:
                    return False
            elif req_key == "total_points":
                if progress.total_points < req_value:
                    return False
            # Add more requirement checks as needed
        
        return True
    
    def _check_milestone_badges(self, user_id: str):
        """Check for milestone badges based on total points"""
        progress = self.get_user_progress(user_id)
        
        for badge in self.badges:
            if (badge.badge_type == BadgeType.MILESTONE and 
                badge.id not in progress.badges_earned):
                
                if badge.requirements.get("total_points", 0) <= progress.total_points:
                    progress.badges_earned.append(badge.id)
    
    def update_challenge_progress(self, user_id: str, challenge_id: str, progress_increment: float) -> Dict:
        """Update user's progress on a specific challenge"""
        challenge = next((c for c in self.challenges if c.id == challenge_id), None)
        if not challenge or not challenge.is_active:
            return {"error": "Challenge not found or inactive"}
        
        user_progress = self.get_user_progress(user_id)
        
        # Add user to challenge if not already participating
        if user_id not in challenge.participants:
            challenge.participants.append(user_id)
            if challenge_id not in user_progress.current_challenges:
                user_progress.current_challenges.append(challenge_id)
        
        # Update progress
        challenge.current_progress += progress_increment
        
        # Check if challenge is completed
        if challenge.current_progress >= challenge.target_value:
            # Award points
            self.award_points(user_id, challenge.points_reward, f"Completed challenge: {challenge.name_english}")
            
            # Award badge if applicable
            if challenge.badge_reward:
                badge = next((b for b in self.badges if b.id == challenge.badge_reward), None)
                if badge and badge.id not in user_progress.badges_earned:
                    user_progress.badges_earned.append(badge.id)
                    user_progress.total_points += badge.points_value
            
            # Mark challenge as completed
            user_progress.challenges_completed.append(challenge_id)
            if challenge_id in user_progress.current_challenges:
                user_progress.current_challenges.remove(challenge_id)
            
            return {
                "challenge_completed": True,
                "points_awarded": challenge.points_reward,
                "badge_earned": challenge.badge_reward
            }
        
        return {
            "challenge_completed": False,
            "current_progress": challenge.current_progress,
            "target_value": challenge.target_value,
            "progress_percentage": (challenge.current_progress / challenge.target_value) * 100
        }
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users leaderboard"""
        users = list(self.user_progress.values())
        users.sort(key=lambda x: x.total_points, reverse=True)
        
        leaderboard = []
        for i, user in enumerate(users[:limit]):
            leaderboard.append({
                "rank": i + 1,
                "user_id": user.user_id,
                "total_points": user.total_points,
                "level": user.level,
                "badges_count": len(user.badges_earned),
                "streak_days": user.streak_days
            })
        
        return leaderboard
    
    def get_user_dashboard(self, user_id: str) -> Dict:
        """Get comprehensive user gamification dashboard"""
        progress = self.get_user_progress(user_id)
        
        # Get user's badges with details
        user_badges = [
            badge for badge in self.badges 
            if badge.id in progress.badges_earned
        ]
        
        # Get active challenges
        active_challenges = [
            challenge for challenge in self.challenges
            if challenge.id in progress.current_challenges
        ]
        
        # Calculate next level progress
        current_level_threshold = self.level_thresholds[progress.level - 1] if progress.level > 1 else 0
        next_level_threshold = self.level_thresholds[progress.level] if progress.level < len(self.level_thresholds) else None
        
        level_progress = 0
        if next_level_threshold:
            level_progress = ((progress.total_points - current_level_threshold) / 
                            (next_level_threshold - current_level_threshold)) * 100
        
        return {
            "user_id": user_id,
            "total_points": progress.total_points,
            "level": progress.level,
            "level_progress_percentage": round(level_progress, 1),
            "next_level_points": next_level_threshold - progress.total_points if next_level_threshold else 0,
            "badges_earned": [asdict(badge) for badge in user_badges],
            "badges_count": len(user_badges),
            "active_challenges": [asdict(challenge) for challenge in active_challenges],
            "challenges_completed_count": len(progress.challenges_completed),
            "streak_days": progress.streak_days,
            "last_activity": progress.last_activity.isoformat()
        }
    
    def get_available_badges(self) -> List[Dict]:
        """Get all available badges"""
        return [asdict(badge) for badge in self.badges]
    
    def get_active_challenges(self) -> List[Dict]:
        """Get all active challenges"""
        return [asdict(challenge) for challenge in self.challenges if challenge.is_active]
    
    def create_custom_challenge(self, challenge_data: Dict) -> Challenge:
        """Create a custom challenge"""
        challenge = Challenge(
            id=challenge_data['id'],
            name_english=challenge_data['name_english'],
            name_swahili=challenge_data['name_swahili'],
            description_english=challenge_data['description_english'],
            description_swahili=challenge_data['description_swahili'],
            challenge_type=ChallengeType(challenge_data['challenge_type']),
            start_date=datetime.fromisoformat(challenge_data['start_date']),
            end_date=datetime.fromisoformat(challenge_data['end_date']),
            target_value=challenge_data['target_value'],
            current_progress=0,
            points_reward=challenge_data['points_reward'],
            badge_reward=challenge_data.get('badge_reward'),
            participants=[],
            is_active=True
        )
        
        self.challenges.append(challenge)
        return challenge

# Global instance
gamification_system = HealthGamification()

def get_gamification_system() -> HealthGamification:
    """Get the global gamification system instance"""
    return gamification_system
