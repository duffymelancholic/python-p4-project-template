import React, { useState, useEffect } from 'react';

const Gamification = () => {
  const [userProgress, setUserProgress] = useState({
    totalPoints: 0,
    level: 1,
    badgesEarned: [],
    streakDays: 0,
    currentChallenges: [],
    completedChallenges: []
  });
  const [badges, setBadges] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [language, setLanguage] = useState('english');

  // Mock data
  const mockBadges = [
    {
      id: 'first_steps',
      name_english: 'First Steps',
      name_swahili: 'Hatua za Kwanza',
      description_english: 'Log your first health reading',
      description_swahili: 'Rekodi kipimo chako cha kwanza cha afya',
      icon: '🌱',
      points_value: 50,
      rarity: 'common',
      earned: true
    },
    {
      id: 'week_warrior',
      name_english: 'Week Warrior',
      name_swahili: 'Shujaa wa Wiki',
      description_english: 'Log health data for 7 consecutive days',
      description_swahili: 'Rekodi data ya afya kwa siku 7 mfululizo',
      icon: '⚡',
      points_value: 200,
      rarity: 'rare',
      earned: true
    },
    {
      id: 'ugali_master',
      name_english: 'Ugali Master',
      name_swahili: 'Bwana Ugali',
      description_english: 'Track 10 traditional Kenyan meals',
      description_swahili: 'Fuatilia vyakula 10 vya kitamaduni vya Kenya',
      icon: '🌽',
      points_value: 150,
      rarity: 'rare',
      earned: false
    },
    {
      id: 'glucose_guardian',
      name_english: 'Glucose Guardian',
      name_swahili: 'Mlinzi wa Sukari',
      description_english: 'Keep glucose in target range for 5 days',
      description_swahili: 'Weka sukari katika kiwango cha lengo kwa siku 5',
      icon: '🎯',
      points_value: 300,
      rarity: 'epic',
      earned: false
    },
    {
      id: 'thousand_club',
      name_english: 'Thousand Club',
      name_swahili: 'Klabu ya Elfu',
      description_english: 'Earn 1000 total points',
      description_swahili: 'Pata jumla ya pointi 1000',
      icon: '💎',
      points_value: 0,
      rarity: 'legendary',
      earned: false
    }
  ];

  const mockChallenges = [
    {
      id: 'daily_reading',
      name_english: 'Daily Health Check',
      name_swahili: 'Uchunguzi wa Afya wa Kila Siku',
      description_english: 'Log at least one health reading today',
      description_swahili: 'Rekodi angalau kipimo kimoja cha afya leo',
      target_value: 1,
      current_progress: 0,
      points_reward: 25,
      type: 'daily',
      timeLeft: '18h 32m',
      active: true
    },
    {
      id: 'kenyan_foods_week',
      name_english: 'Kenyan Foods Week',
      name_swahili: 'Wiki ya Vyakula vya Kenya',
      description_english: 'Try 5 different traditional Kenyan foods this week',
      description_swahili: 'Jaribu vyakula 5 tofauti vya kitamaduni vya Kenya wiki hii',
      target_value: 5,
      current_progress: 2,
      points_reward: 150,
      type: 'weekly',
      timeLeft: '4d 12h',
      active: true
    },
    {
      id: 'glucose_stability',
      name_english: 'Glucose Stability Challenge',
      name_swahili: 'Changamoto ya Uthabiti wa Sukari',
      description_english: 'Keep glucose readings within target range for 2 weeks',
      description_swahili: 'Weka vipimo vya sukari katika kiwango cha lengo kwa wiki 2',
      target_value: 14,
      current_progress: 3,
      points_reward: 400,
      type: 'weekly',
      timeLeft: '9d 6h',
      active: true
    }
  ];

  const mockLeaderboard = [
    { rank: 1, name: 'Amina K.', points: 2450, level: 8, badges: 12 },
    { rank: 2, name: 'John M.', points: 2180, level: 7, badges: 10 },
    { rank: 3, name: 'Grace W.', points: 1920, level: 6, badges: 9 },
    { rank: 4, name: 'You', points: 850, level: 4, badges: 2, isCurrentUser: true },
    { rank: 5, name: 'Peter N.', points: 720, level: 3, badges: 5 }
  ];

  useEffect(() => {
    // Simulate loading data
    setTimeout(() => {
      setUserProgress({
        totalPoints: 850,
        level: 4,
        badgesEarned: ['first_steps', 'week_warrior'],
        streakDays: 12,
        currentChallenges: ['daily_reading', 'kenyan_foods_week', 'glucose_stability'],
        completedChallenges: ['beginner_challenge']
      });
      setBadges(mockBadges);
      setChallenges(mockChallenges);
      setLeaderboard(mockLeaderboard);
    }, 500);
  }, []);

  const getRarityColor = (rarity) => {
    switch(rarity) {
      case 'common': return '#4CAF50';
      case 'rare': return '#2196F3';
      case 'epic': return '#9C27B0';
      case 'legendary': return '#FF9800';
      default: return '#757575';
    }
  };

  const getChallengeTypeColor = (type) => {
    switch(type) {
      case 'daily': return '#4CAF50';
      case 'weekly': return '#2196F3';
      case 'monthly': return '#9C27B0';
      default: return '#757575';
    }
  };

  const calculateLevelProgress = () => {
    const levelThresholds = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500];
    const currentLevelThreshold = levelThresholds[userProgress.level - 1] || 0;
    const nextLevelThreshold = levelThresholds[userProgress.level] || levelThresholds[levelThresholds.length - 1];
    
    const progress = ((userProgress.totalPoints - currentLevelThreshold) / (nextLevelThreshold - currentLevelThreshold)) * 100;
    return Math.min(100, Math.max(0, progress));
  };

  const getNextLevelPoints = () => {
    const levelThresholds = [0, 100, 300, 600, 1000, 1500, 2200, 3000, 4000, 5500];
    const nextLevelThreshold = levelThresholds[userProgress.level] || levelThresholds[levelThresholds.length - 1];
    return nextLevelThreshold - userProgress.totalPoints;
  };

  const earnedBadges = badges.filter(badge => badge.earned);
  const availableBadges = badges.filter(badge => !badge.earned);

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>🎮 Health Gamification</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button
            onClick={() => setLanguage('english')}
            style={{
              padding: '8px 16px',
              backgroundColor: language === 'english' ? '#2196F3' : 'transparent',
              color: language === 'english' ? 'white' : '#2196F3',
              border: '1px solid #2196F3',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            English
          </button>
          <button
            onClick={() => setLanguage('swahili')}
            style={{
              padding: '8px 16px',
              backgroundColor: language === 'swahili' ? '#2196F3' : 'transparent',
              color: language === 'swahili' ? 'white' : '#2196F3',
              border: '1px solid #2196F3',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Kiswahili
          </button>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', borderBottom: '1px solid #ddd' }}>
        {['dashboard', 'badges', 'challenges', 'leaderboard'].map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            style={{
              padding: '10px 20px',
              backgroundColor: activeTab === tab ? '#2196F3' : 'transparent',
              color: activeTab === tab ? 'white' : '#2196F3',
              border: 'none',
              borderBottom: activeTab === tab ? '2px solid #2196F3' : '2px solid transparent',
              cursor: 'pointer',
              textTransform: 'capitalize'
            }}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Dashboard Tab */}
      {activeTab === 'dashboard' && (
        <div>
          {/* User Stats */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            <div style={{ padding: '20px', backgroundColor: '#e3f2fd', borderRadius: '8px', textAlign: 'center' }}>
              <h3>Level {userProgress.level}</h3>
              <div style={{
                width: '100%',
                height: '20px',
                backgroundColor: '#ddd',
                borderRadius: '10px',
                overflow: 'hidden',
                marginBottom: '10px'
              }}>
                <div style={{
                  width: `${calculateLevelProgress()}%`,
                  height: '100%',
                  backgroundColor: '#2196F3',
                  transition: 'width 0.3s ease'
                }} />
              </div>
              <p>{getNextLevelPoints()} points to next level</p>
            </div>

            <div style={{ padding: '20px', backgroundColor: '#fff3e0', borderRadius: '8px', textAlign: 'center' }}>
              <h3>{userProgress.totalPoints}</h3>
              <p>Total Points</p>
              <span style={{ fontSize: '24px' }}>🏆</span>
            </div>

            <div style={{ padding: '20px', backgroundColor: '#e8f5e8', borderRadius: '8px', textAlign: 'center' }}>
              <h3>{userProgress.streakDays}</h3>
              <p>Day Streak</p>
              <span style={{ fontSize: '24px' }}>🔥</span>
            </div>

            <div style={{ padding: '20px', backgroundColor: '#fce4ec', borderRadius: '8px', textAlign: 'center' }}>
              <h3>{earnedBadges.length}</h3>
              <p>Badges Earned</p>
              <span style={{ fontSize: '24px' }}>🏅</span>
            </div>
          </div>

          {/* Recent Achievements */}
          <div style={{ marginBottom: '30px' }}>
            <h3>🎉 Recent Achievements</h3>
            <div style={{ display: 'flex', gap: '15px', overflowX: 'auto', padding: '10px 0' }}>
              {earnedBadges.slice(0, 3).map(badge => (
                <div key={badge.id} style={{
                  minWidth: '200px',
                  padding: '15px',
                  backgroundColor: 'white',
                  border: `2px solid ${getRarityColor(badge.rarity)}`,
                  borderRadius: '8px',
                  textAlign: 'center'
                }}>
                  <div style={{ fontSize: '32px', marginBottom: '10px' }}>{badge.icon}</div>
                  <h4 style={{ margin: '0 0 5px 0' }}>
                    {language === 'swahili' ? badge.name_swahili : badge.name_english}
                  </h4>
                  <p style={{ fontSize: '12px', color: '#666', margin: '0' }}>
                    +{badge.points_value} points
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Active Challenges Preview */}
          <div>
            <h3>⚡ Active Challenges</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px' }}>
              {challenges.filter(c => c.active).slice(0, 3).map(challenge => (
                <div key={challenge.id} style={{
                  padding: '15px',
                  backgroundColor: 'white',
                  border: `2px solid ${getChallengeTypeColor(challenge.type)}`,
                  borderRadius: '8px'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                    <h4 style={{ margin: 0 }}>
                      {language === 'swahili' ? challenge.name_swahili : challenge.name_english}
                    </h4>
                    <span style={{
                      backgroundColor: getChallengeTypeColor(challenge.type),
                      color: 'white',
                      padding: '2px 8px',
                      borderRadius: '12px',
                      fontSize: '12px'
                    }}>
                      {challenge.type}
                    </span>
                  </div>
                  <p style={{ fontSize: '14px', color: '#666', marginBottom: '10px' }}>
                    {language === 'swahili' ? challenge.description_swahili : challenge.description_english}
                  </p>
                  <div style={{ marginBottom: '10px' }}>
                    <div style={{
                      width: '100%',
                      height: '8px',
                      backgroundColor: '#ddd',
                      borderRadius: '4px',
                      overflow: 'hidden'
                    }}>
                      <div style={{
                        width: `${(challenge.current_progress / challenge.target_value) * 100}%`,
                        height: '100%',
                        backgroundColor: getChallengeTypeColor(challenge.type)
                      }} />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginTop: '5px' }}>
                      <span>{challenge.current_progress}/{challenge.target_value}</span>
                      <span>{challenge.timeLeft} left</span>
                    </div>
                  </div>
                  <div style={{ textAlign: 'center', color: '#FF9800', fontWeight: 'bold' }}>
                    🏆 {challenge.points_reward} points
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Badges Tab */}
      {activeTab === 'badges' && (
        <div>
          <h3>🏅 Your Badge Collection</h3>
          
          {/* Earned Badges */}
          <div style={{ marginBottom: '30px' }}>
            <h4>Earned Badges ({earnedBadges.length})</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '15px' }}>
              {earnedBadges.map(badge => (
                <div key={badge.id} style={{
                  padding: '20px',
                  backgroundColor: 'white',
                  border: `3px solid ${getRarityColor(badge.rarity)}`,
                  borderRadius: '8px',
                  textAlign: 'center',
                  boxShadow: '0 4px 8px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>{badge.icon}</div>
                  <h4 style={{ margin: '0 0 5px 0', color: getRarityColor(badge.rarity) }}>
                    {language === 'swahili' ? badge.name_swahili : badge.name_english}
                  </h4>
                  <p style={{ fontSize: '14px', color: '#666', marginBottom: '10px' }}>
                    {language === 'swahili' ? badge.description_swahili : badge.description_english}
                  </p>
                  <div style={{
                    backgroundColor: getRarityColor(badge.rarity),
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    display: 'inline-block'
                  }}>
                    {badge.rarity.toUpperCase()} • {badge.points_value} pts
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Available Badges */}
          <div>
            <h4>Available Badges ({availableBadges.length})</h4>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minWidth(250px, 1fr))', gap: '15px' }}>
              {availableBadges.map(badge => (
                <div key={badge.id} style={{
                  padding: '20px',
                  backgroundColor: '#f5f5f5',
                  border: '2px dashed #ddd',
                  borderRadius: '8px',
                  textAlign: 'center',
                  opacity: 0.7
                }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px', filter: 'grayscale(100%)' }}>
                    {badge.icon}
                  </div>
                  <h4 style={{ margin: '0 0 5px 0', color: '#666' }}>
                    {language === 'swahili' ? badge.name_swahili : badge.name_english}
                  </h4>
                  <p style={{ fontSize: '14px', color: '#666', marginBottom: '10px' }}>
                    {language === 'swahili' ? badge.description_swahili : badge.description_english}
                  </p>
                  <div style={{
                    backgroundColor: '#ddd',
                    color: '#666',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    display: 'inline-block'
                  }}>
                    {badge.rarity.toUpperCase()} • {badge.points_value} pts
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Challenges Tab */}
      {activeTab === 'challenges' && (
        <div>
          <h3>⚡ Health Challenges</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minWidth(350px, 1fr))', gap: '20px' }}>
            {challenges.map(challenge => (
              <div key={challenge.id} style={{
                padding: '20px',
                backgroundColor: 'white',
                border: `2px solid ${getChallengeTypeColor(challenge.type)}`,
                borderRadius: '8px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                  <h4 style={{ margin: 0 }}>
                    {language === 'swahili' ? challenge.name_swahili : challenge.name_english}
                  </h4>
                  <span style={{
                    backgroundColor: getChallengeTypeColor(challenge.type),
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '12px'
                  }}>
                    {challenge.type.toUpperCase()}
                  </span>
                </div>
                
                <p style={{ color: '#666', marginBottom: '15px' }}>
                  {language === 'swahili' ? challenge.description_swahili : challenge.description_english}
                </p>
                
                <div style={{ marginBottom: '15px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                    <span>Progress</span>
                    <span>{Math.round((challenge.current_progress / challenge.target_value) * 100)}%</span>
                  </div>
                  <div style={{
                    width: '100%',
                    height: '12px',
                    backgroundColor: '#ddd',
                    borderRadius: '6px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${(challenge.current_progress / challenge.target_value) * 100}%`,
                      height: '100%',
                      backgroundColor: getChallengeTypeColor(challenge.type),
                      transition: 'width 0.3s ease'
                    }} />
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginTop: '5px' }}>
                    <span>{challenge.current_progress} / {challenge.target_value}</span>
                    <span>⏰ {challenge.timeLeft}</span>
                  </div>
                </div>
                
                <div style={{ textAlign: 'center', padding: '10px', backgroundColor: '#fff3e0', borderRadius: '4px' }}>
                  <span style={{ fontSize: '18px', fontWeight: 'bold', color: '#FF9800' }}>
                    🏆 {challenge.points_reward} Points Reward
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Leaderboard Tab */}
      {activeTab === 'leaderboard' && (
        <div>
          <h3>🏆 Community Leaderboard</h3>
          <div style={{ backgroundColor: 'white', borderRadius: '8px', overflow: 'hidden' }}>
            {leaderboard.map(user => (
              <div key={user.rank} style={{
                padding: '15px 20px',
                borderBottom: '1px solid #eee',
                backgroundColor: user.isCurrentUser ? '#e3f2fd' : 'white',
                display: 'flex',
                alignItems: 'center',
                gap: '15px'
              }}>
                <div style={{
                  width: '40px',
                  height: '40px',
                  borderRadius: '50%',
                  backgroundColor: user.rank <= 3 ? '#FFD700' : '#ddd',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 'bold',
                  color: user.rank <= 3 ? 'white' : '#666'
                }}>
                  {user.rank <= 3 ? ['🥇', '🥈', '🥉'][user.rank - 1] : user.rank}
                </div>
                
                <div style={{ flex: 1 }}>
                  <h4 style={{ margin: '0 0 5px 0', color: user.isCurrentUser ? '#2196F3' : 'black' }}>
                    {user.name} {user.isCurrentUser && '(You)'}
                  </h4>
                  <div style={{ display: 'flex', gap: '15px', fontSize: '14px', color: '#666' }}>
                    <span>Level {user.level}</span>
                    <span>{user.badges} badges</span>
                  </div>
                </div>
                
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#FF9800' }}>
                    {user.points.toLocaleString()}
                  </div>
                  <div style={{ fontSize: '12px', color: '#666' }}>points</div>
                </div>
              </div>
            ))}
          </div>
          
          <div style={{ marginTop: '20px', textAlign: 'center', color: '#666' }}>
            <p>Compete with friends and the community to stay motivated!</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default Gamification;
