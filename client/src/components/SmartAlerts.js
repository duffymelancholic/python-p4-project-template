import React, { useState, useEffect } from 'react';

const SmartAlerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [preferences, setPreferences] = useState({
    glucoseAlerts: true,
    mealReminders: true,
    exercisePrompts: true,
    culturalTips: true,
    medicationReminders: true
  });
  const [userProfile, setUserProfile] = useState({
    targetGlucoseRange: [80, 140],
    preferredLanguage: 'english',
    diabetesType: 'type2',
    activityLevel: 'moderate'
  });

  // Mock alerts data
  const mockAlerts = [
    {
      id: 1,
      type: 'glucose_warning',
      priority: 'high',
      title_english: 'High Glucose Alert',
      title_swahili: 'Onyo la Sukari ya Juu',
      message_english: 'Your glucose level is predicted to be high after this meal. Consider reducing ugali portion.',
      message_swahili: 'Kiwango cha sukari yako kinatarajiwa kuwa juu baada ya chakula hiki. Fikiria kupunguza sehemu ya ugali.',
      timestamp: new Date(Date.now() - 30 * 60 * 1000), // 30 minutes ago
      actionable: true,
      actions: [
        { text: 'Take a 10-minute walk', text_swahili: 'Tembea kwa dakika 10' },
        { text: 'Drink water', text_swahili: 'Nywa maji' }
      ],
      icon: '⚠️',
      read: false
    },
    {
      id: 2,
      type: 'meal_suggestion',
      priority: 'medium',
      title_english: 'Healthy Meal Suggestion',
      title_swahili: 'Pendekezo la Chakula Chenye Afya',
      message_english: 'Try githeri today! It\'s diabetes-friendly and rich in fiber.',
      message_swahili: 'Jaribu githeri leo! Ni rafiki wa kisukari na ina nyuzi nyingi.',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      actionable: true,
      actions: [
        { text: 'View recipe', text_swahili: 'Ona mapishi' },
        { text: 'Add to meal plan', text_swahili: 'Ongeza kwenye mpango wa chakula' }
      ],
      icon: '🍽️',
      read: false
    },
    {
      id: 3,
      type: 'exercise_prompt',
      priority: 'low',
      title_english: 'Movement Reminder',
      title_swahili: 'Ukumbusho wa Mazoezi',
      message_english: 'You\'ve been sitting for 2 hours. A short walk can help with glucose control.',
      message_swahili: 'Umekuwa ukiketi kwa masaa 2. Kutembea kidogo kunaweza kusaidia kudhibiti sukari.',
      timestamp: new Date(Date.now() - 15 * 60 * 1000), // 15 minutes ago
      actionable: true,
      actions: [
        { text: 'Start 5-min walk', text_swahili: 'Anza kutembea kwa dakika 5' },
        { text: 'Do stretches', text_swahili: 'Fanya mazoezi ya kunyoosha' }
      ],
      icon: '🚶‍♂️',
      read: true
    },
    {
      id: 4,
      type: 'cultural_tip',
      priority: 'low',
      title_english: 'Cultural Health Tip',
      title_swahili: 'Kidokezo cha Afya cha Kitamaduni',
      message_english: 'Did you know? Traditional sukuma wiki is rich in antioxidants that help fight inflammation.',
      message_swahili: 'Je, ulijua? Sukuma wiki ya kitamaduni ina antioxidants nyingi zinazosaidia kupambana na uvimbe.',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
      actionable: false,
      icon: '💡',
      read: true
    },
    {
      id: 5,
      type: 'medication_reminder',
      priority: 'high',
      title_english: 'Medication Reminder',
      title_swahili: 'Ukumbusho wa Dawa',
      message_english: 'Time to take your evening medication.',
      message_swahili: 'Ni wakati wa kuchukua dawa yako ya jioni.',
      timestamp: new Date(Date.now() - 5 * 60 * 1000), // 5 minutes ago
      actionable: true,
      actions: [
        { text: 'Mark as taken', text_swahili: 'Weka alama kama umechukua' },
        { text: 'Snooze 15 min', text_swahili: 'Ahirisha dakika 15' }
      ],
      icon: '💊',
      read: false
    }
  ];

  useEffect(() => {
    // Simulate loading alerts
    setTimeout(() => {
      setAlerts(mockAlerts);
    }, 500);

    // Simulate real-time alerts
    const interval = setInterval(() => {
      if (Math.random() > 0.8) { // 20% chance every 10 seconds
        const newAlert = generateRandomAlert();
        setAlerts(prev => [newAlert, ...prev.slice(0, 9)]); // Keep only 10 most recent
      }
    }, 10000);

    return () => clearInterval(interval);
  }, []);

  const generateRandomAlert = () => {
    const alertTypes = [
      {
        type: 'hydration_reminder',
        title_english: 'Hydration Reminder',
        title_swahili: 'Ukumbusho wa Maji',
        message_english: 'Remember to drink water! Proper hydration helps with glucose control.',
        message_swahili: 'Kumbuka kunywa maji! Maji ya kutosha yanasaidia kudhibiti sukari.',
        icon: '💧',
        priority: 'low'
      },
      {
        type: 'glucose_check',
        title_english: 'Glucose Check Reminder',
        title_swahili: 'Ukumbusho wa Kupima Sukari',
        message_english: 'It\'s time for your routine glucose check.',
        message_swahili: 'Ni wakati wa kupima sukari yako kwa kawaida.',
        icon: '🩸',
        priority: 'medium'
      }
    ];

    const randomAlert = alertTypes[Math.floor(Math.random() * alertTypes.length)];
    
    return {
      id: Date.now(),
      ...randomAlert,
      timestamp: new Date(),
      actionable: true,
      actions: [
        { text: 'Done', text_swahili: 'Imekwisha' },
        { text: 'Remind later', text_swahili: 'Nikumbushe baadaye' }
      ],
      read: false
    };
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case 'high': return '#F44336';
      case 'medium': return '#FF9800';
      case 'low': return '#4CAF50';
      default: return '#757575';
    }
  };

  const getTypeColor = (type) => {
    switch(type) {
      case 'glucose_warning': return '#F44336';
      case 'meal_suggestion': return '#4CAF50';
      case 'exercise_prompt': return '#2196F3';
      case 'cultural_tip': return '#9C27B0';
      case 'medication_reminder': return '#FF5722';
      default: return '#757575';
    }
  };

  const markAsRead = (alertId) => {
    setAlerts(prev => prev.map(alert => 
      alert.id === alertId ? { ...alert, read: true } : alert
    ));
  };

  const dismissAlert = (alertId) => {
    setAlerts(prev => prev.filter(alert => alert.id !== alertId));
  };

  const handleAction = (alertId, action) => {
    console.log(`Action taken: ${action.text} for alert ${alertId}`);
    markAsRead(alertId);
    // In real app, this would trigger the actual action
  };

  const formatTimestamp = (timestamp) => {
    const now = new Date();
    const diff = now - timestamp;
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    return `${days}d ago`;
  };

  const unreadCount = alerts.filter(alert => !alert.read).length;
  const highPriorityCount = alerts.filter(alert => alert.priority === 'high' && !alert.read).length;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>🔔 Smart Health Alerts</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          <span style={{
            backgroundColor: '#2196F3',
            color: 'white',
            padding: '4px 12px',
            borderRadius: '12px',
            fontSize: '14px'
          }}>
            {unreadCount} unread
          </span>
          {highPriorityCount > 0 && (
            <span style={{
              backgroundColor: '#F44336',
              color: 'white',
              padding: '4px 12px',
              borderRadius: '12px',
              fontSize: '14px'
            }}>
              {highPriorityCount} urgent
            </span>
          )}
        </div>
      </div>

      {/* Alert Preferences */}
      <div style={{
        padding: '15px',
        backgroundColor: '#f5f5f5',
        borderRadius: '8px',
        marginBottom: '20px'
      }}>
        <h3>Alert Preferences</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px' }}>
          {Object.entries(preferences).map(([key, value]) => (
            <label key={key} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <input
                type="checkbox"
                checked={value}
                onChange={(e) => setPreferences(prev => ({ ...prev, [key]: e.target.checked }))}
              />
              <span>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</span>
            </label>
          ))}
        </div>
      </div>

      {/* Alerts List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {alerts.length === 0 ? (
          <div style={{
            padding: '40px',
            textAlign: 'center',
            color: '#666',
            border: '2px dashed #ddd',
            borderRadius: '8px'
          }}>
            <h3>No alerts at the moment</h3>
            <p>You're all caught up! New alerts will appear here.</p>
          </div>
        ) : (
          alerts.map(alert => (
            <div
              key={alert.id}
              style={{
                padding: '15px',
                border: `2px solid ${alert.read ? '#e0e0e0' : getTypeColor(alert.type)}`,
                borderRadius: '8px',
                backgroundColor: alert.read ? '#f9f9f9' : 'white',
                position: 'relative',
                opacity: alert.read ? 0.7 : 1
              }}
            >
              {/* Priority indicator */}
              <div style={{
                position: 'absolute',
                top: '10px',
                right: '10px',
                width: '12px',
                height: '12px',
                borderRadius: '50%',
                backgroundColor: getPriorityColor(alert.priority)
              }} />

              {/* Alert header */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
                <span style={{ fontSize: '24px' }}>{alert.icon}</span>
                <div style={{ flex: 1 }}>
                  <h4 style={{ margin: '0', color: getTypeColor(alert.type) }}>
                    {userProfile.preferredLanguage === 'swahili' ? alert.title_swahili : alert.title_english}
                  </h4>
                  <small style={{ color: '#666' }}>{formatTimestamp(alert.timestamp)}</small>
                </div>
                <button
                  onClick={() => dismissAlert(alert.id)}
                  style={{
                    background: 'none',
                    border: 'none',
                    fontSize: '18px',
                    cursor: 'pointer',
                    color: '#666'
                  }}
                >
                  ×
                </button>
              </div>

              {/* Alert message */}
              <p style={{ margin: '10px 0', lineHeight: '1.5' }}>
                {userProfile.preferredLanguage === 'swahili' ? alert.message_swahili : alert.message_english}
              </p>

              {/* Actions */}
              {alert.actionable && alert.actions && (
                <div style={{ display: 'flex', gap: '10px', marginTop: '15px', flexWrap: 'wrap' }}>
                  {alert.actions.map((action, index) => (
                    <button
                      key={index}
                      onClick={() => handleAction(alert.id, action)}
                      style={{
                        padding: '8px 16px',
                        backgroundColor: getTypeColor(alert.type),
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px'
                      }}
                    >
                      {userProfile.preferredLanguage === 'swahili' ? action.text_swahili : action.text}
                    </button>
                  ))}
                  {!alert.read && (
                    <button
                      onClick={() => markAsRead(alert.id)}
                      style={{
                        padding: '8px 16px',
                        backgroundColor: 'transparent',
                        color: '#666',
                        border: '1px solid #ddd',
                        borderRadius: '4px',
                        cursor: 'pointer',
                        fontSize: '14px'
                      }}
                    >
                      Mark as read
                    </button>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Language Toggle */}
      <div style={{
        marginTop: '30px',
        padding: '15px',
        backgroundColor: '#e3f2fd',
        borderRadius: '8px',
        textAlign: 'center'
      }}>
        <h4>Language / Lugha</h4>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '10px' }}>
          <button
            onClick={() => setUserProfile(prev => ({ ...prev, preferredLanguage: 'english' }))}
            style={{
              padding: '8px 16px',
              backgroundColor: userProfile.preferredLanguage === 'english' ? '#2196F3' : 'transparent',
              color: userProfile.preferredLanguage === 'english' ? 'white' : '#2196F3',
              border: '1px solid #2196F3',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            English
          </button>
          <button
            onClick={() => setUserProfile(prev => ({ ...prev, preferredLanguage: 'swahili' }))}
            style={{
              padding: '8px 16px',
              backgroundColor: userProfile.preferredLanguage === 'swahili' ? '#2196F3' : 'transparent',
              color: userProfile.preferredLanguage === 'swahili' ? 'white' : '#2196F3',
              border: '1px solid #2196F3',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Kiswahili
          </button>
        </div>
      </div>

      {/* Alert Statistics */}
      <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
        <h4>📊 Alert Summary</h4>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '15px' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#F44336' }}>
              {alerts.filter(a => a.priority === 'high').length}
            </div>
            <div style={{ fontSize: '14px' }}>High Priority</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#FF9800' }}>
              {alerts.filter(a => a.priority === 'medium').length}
            </div>
            <div style={{ fontSize: '14px' }}>Medium Priority</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#4CAF50' }}>
              {alerts.filter(a => a.priority === 'low').length}
            </div>
            <div style={{ fontSize: '14px' }}>Low Priority</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#2196F3' }}>
              {alerts.filter(a => a.actionable).length}
            </div>
            <div style={{ fontSize: '14px' }}>Actionable</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SmartAlerts;
