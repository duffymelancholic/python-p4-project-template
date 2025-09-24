import React, { useState, useEffect } from 'react';

const FoodInsights = () => {
  const [kenyanFoods, setKenyanFoods] = useState([]);
  const [selectedFood, setSelectedFood] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('all');
  const [glucosePrediction, setGlucosePrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  // Mock Kenyan foods data (in real app, this would come from API)
  const mockKenyanFoods = [
    {
      id: 'ugali',
      name_english: 'Ugali',
      name_swahili: 'Ugali',
      category: 'staples',
      diabetes_friendly: false,
      nutritional_info: {
        calories_per_100g: 112,
        carbohydrates_g: 24.0,
        protein_g: 2.3,
        fiber_g: 1.2,
        glycemic_index: 72
      },
      description_english: 'Traditional cornmeal staple, served with vegetables and meat',
      description_swahili: 'Chakula cha msingi kinachotengenezwa na unga wa mahindi',
      health_benefits: ['Good source of energy', 'Contains some protein', 'Gluten-free option'],
      preparation_tips: ['Serve smaller portions', 'Combine with high-fiber vegetables']
    },
    {
      id: 'githeri',
      name_english: 'Githeri',
      name_swahili: 'Githeri',
      category: 'staples',
      diabetes_friendly: true,
      nutritional_info: {
        calories_per_100g: 130,
        carbohydrates_g: 22.0,
        protein_g: 6.5,
        fiber_g: 5.8,
        glycemic_index: 45
      },
      description_english: 'Traditional mix of boiled maize and beans',
      description_swahili: 'Mchanganyiko wa mahindi na maharagwe',
      health_benefits: ['High in protein and fiber', 'Low glycemic index', 'Helps control blood sugar'],
      preparation_tips: ['Soak beans overnight', 'Add vegetables for extra nutrients']
    },
    {
      id: 'sukuma_wiki',
      name_english: 'Collard Greens',
      name_swahili: 'Sukuma Wiki',
      category: 'vegetables',
      diabetes_friendly: true,
      nutritional_info: {
        calories_per_100g: 35,
        carbohydrates_g: 7.3,
        protein_g: 3.3,
        fiber_g: 3.6,
        glycemic_index: 15
      },
      description_english: 'Popular leafy green vegetable, often sautéed with onions',
      description_swahili: 'Mboga za majani yanayoliwa sana Kenya',
      health_benefits: ['Very low glycemic index', 'High in vitamins A, C, K', 'Rich in antioxidants'],
      preparation_tips: ['Don\'t overcook to retain nutrients', 'Add minimal oil']
    }
  ];

  useEffect(() => {
    // Simulate loading data
    setLoading(true);
    setTimeout(() => {
      setKenyanFoods(mockKenyanFoods);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredFoods = kenyanFoods.filter(food => {
    const matchesSearch = food.name_english.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         food.name_swahili.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = category === 'all' || food.category === category;
    return matchesSearch && matchesCategory;
  });

  const handleFoodSelect = (food) => {
    setSelectedFood(food);
    // Simulate glucose prediction
    setLoading(true);
    setTimeout(() => {
      const mockPrediction = {
        predicted_peak_glucose: food.nutritional_info.glycemic_index + Math.random() * 20 + 80,
        risk_level: food.diabetes_friendly ? 'normal' : 'elevated',
        recommendations: food.preparation_tips
      };
      setGlucosePrediction(mockPrediction);
      setLoading(false);
    }, 800);
  };

  const getGIColor = (gi) => {
    if (gi < 55) return '#4CAF50'; // Green for low GI
    if (gi < 70) return '#FF9800'; // Orange for medium GI
    return '#F44336'; // Red for high GI
  };

  const getRiskColor = (risk) => {
    switch(risk) {
      case 'normal': return '#4CAF50';
      case 'elevated': return '#FF9800';
      case 'high': return '#F44336';
      default: return '#757575';
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>🍽️ Kenyan Food Insights</h1>
      <p>Discover traditional Kenyan foods and their health impacts</p>

      {/* Search and Filter */}
      <div style={{ marginBottom: '20px', display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="Search foods (English or Swahili)..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '5px',
            flex: '1',
            minWidth: '200px'
          }}
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          style={{
            padding: '10px',
            border: '1px solid #ddd',
            borderRadius: '5px'
          }}
        >
          <option value="all">All Categories</option>
          <option value="staples">Staples</option>
          <option value="vegetables">Vegetables</option>
          <option value="proteins">Proteins</option>
          <option value="fruits">Fruits</option>
        </select>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Food List */}
        <div>
          <h2>Traditional Foods</h2>
          {loading && !selectedFood ? (
            <div>Loading foods...</div>
          ) : (
            <div style={{ display: 'grid', gap: '10px' }}>
              {filteredFoods.map(food => (
                <div
                  key={food.id}
                  onClick={() => handleFoodSelect(food)}
                  style={{
                    padding: '15px',
                    border: selectedFood?.id === food.id ? '2px solid #2196F3' : '1px solid #ddd',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    backgroundColor: selectedFood?.id === food.id ? '#E3F2FD' : 'white',
                    transition: 'all 0.2s'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <h3 style={{ margin: '0 0 5px 0' }}>{food.name_english}</h3>
                      <p style={{ margin: '0', color: '#666', fontStyle: 'italic' }}>
                        {food.name_swahili}
                      </p>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      {food.diabetes_friendly && (
                        <span style={{
                          backgroundColor: '#4CAF50',
                          color: 'white',
                          padding: '2px 8px',
                          borderRadius: '12px',
                          fontSize: '12px'
                        }}>
                          Diabetes Friendly
                        </span>
                      )}
                      <div style={{
                        backgroundColor: getGIColor(food.nutritional_info.glycemic_index),
                        color: 'white',
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontSize: '12px',
                        fontWeight: 'bold'
                      }}>
                        GI: {food.nutritional_info.glycemic_index}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Food Details and Prediction */}
        <div>
          {selectedFood ? (
            <div>
              <h2>Food Analysis</h2>
              <div style={{
                padding: '20px',
                border: '1px solid #ddd',
                borderRadius: '8px',
                backgroundColor: '#f9f9f9'
              }}>
                <h3>{selectedFood.name_english} ({selectedFood.name_swahili})</h3>
                
                {/* Description */}
                <div style={{ marginBottom: '15px' }}>
                  <p><strong>English:</strong> {selectedFood.description_english}</p>
                  <p><strong>Swahili:</strong> {selectedFood.description_swahili}</p>
                </div>

                {/* Nutritional Info */}
                <div style={{ marginBottom: '15px' }}>
                  <h4>Nutritional Information (per 100g)</h4>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                    <div>Calories: {selectedFood.nutritional_info.calories_per_100g}</div>
                    <div>Carbs: {selectedFood.nutritional_info.carbohydrates_g}g</div>
                    <div>Protein: {selectedFood.nutritional_info.protein_g}g</div>
                    <div>Fiber: {selectedFood.nutritional_info.fiber_g}g</div>
                  </div>
                  <div style={{
                    marginTop: '10px',
                    padding: '10px',
                    backgroundColor: getGIColor(selectedFood.nutritional_info.glycemic_index),
                    color: 'white',
                    borderRadius: '5px',
                    textAlign: 'center'
                  }}>
                    Glycemic Index: {selectedFood.nutritional_info.glycemic_index}
                  </div>
                </div>

                {/* Health Benefits */}
                <div style={{ marginBottom: '15px' }}>
                  <h4>Health Benefits</h4>
                  <ul>
                    {selectedFood.health_benefits.map((benefit, index) => (
                      <li key={index}>{benefit}</li>
                    ))}
                  </ul>
                </div>

                {/* Glucose Prediction */}
                {loading && selectedFood ? (
                  <div>Analyzing glucose impact...</div>
                ) : glucosePrediction ? (
                  <div style={{
                    padding: '15px',
                    backgroundColor: 'white',
                    border: '1px solid #ddd',
                    borderRadius: '5px'
                  }}>
                    <h4>🔮 Glucose Impact Prediction</h4>
                    <div style={{
                      fontSize: '24px',
                      fontWeight: 'bold',
                      color: getRiskColor(glucosePrediction.risk_level),
                      marginBottom: '10px'
                    }}>
                      Peak Glucose: {Math.round(glucosePrediction.predicted_peak_glucose)} mg/dL
                    </div>
                    <div style={{
                      padding: '8px',
                      backgroundColor: getRiskColor(glucosePrediction.risk_level),
                      color: 'white',
                      borderRadius: '4px',
                      textAlign: 'center',
                      marginBottom: '10px'
                    }}>
                      Risk Level: {glucosePrediction.risk_level.toUpperCase()}
                    </div>
                    
                    <h5>💡 Recommendations:</h5>
                    <ul>
                      {glucosePrediction.recommendations.map((rec, index) => (
                        <li key={index}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                ) : null}

                {/* Preparation Tips */}
                <div>
                  <h4>Preparation Tips</h4>
                  <ul>
                    {selectedFood.preparation_tips.map((tip, index) => (
                      <li key={index}>{tip}</li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            <div style={{
              padding: '40px',
              textAlign: 'center',
              color: '#666',
              border: '2px dashed #ddd',
              borderRadius: '8px'
            }}>
              <h3>Select a food to see detailed analysis</h3>
              <p>Click on any food from the list to see nutritional information, health benefits, and glucose impact predictions.</p>
            </div>
          )}
        </div>
      </div>

      {/* Quick Stats */}
      <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
        <h3>📊 Quick Stats</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '15px' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#4CAF50' }}>
              {kenyanFoods.filter(f => f.diabetes_friendly).length}
            </div>
            <div>Diabetes-Friendly Foods</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#2196F3' }}>
              {kenyanFoods.filter(f => f.nutritional_info.glycemic_index < 55).length}
            </div>
            <div>Low GI Foods</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#FF9800' }}>
              {kenyanFoods.filter(f => f.nutritional_info.fiber_g > 5).length}
            </div>
            <div>High Fiber Foods</div>
          </div>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#9C27B0' }}>
              {kenyanFoods.length}
            </div>
            <div>Total Foods</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FoodInsights;
