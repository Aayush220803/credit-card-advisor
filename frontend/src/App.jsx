import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [income, setIncome] = useState('');
  const [spending, setSpending] = useState('');
  const [preferences, setPreferences] = useState('');
  const [cards, setCards] = useState([]);

  const handleSubmit = async () => {
    const message = `Use the tool with this input: {
      "income": "${income}",
      "spending": "${spending}",
      "preferences": "${preferences}"
    }`;

    try {
      const res = await axios.post('http://127.0.0.1:8000/chat', { message });

      const json = JSON.parse(res.data.response); //
      setCards(json);
    } catch (err) {
      setCards([]);
      console.error("Error parsing recommendation:", err);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Credit Card Advisor</h1>

      <div className="form-card">
        <label>Monthly Income:</label>
        <input
          type="number"
          value={income}
          onChange={(e) => setIncome(e.target.value)}
          placeholder="e.g. 70000"
        />
        <label>Spending Categories (comma-separated):</label>
        <input
          type="text"
          value={spending}
          onChange={(e) => setSpending(e.target.value)}
          placeholder="e.g. travel, fuel"
        />
        <label>Preferences (comma-separated):</label>
        <input
          type="text"
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
          placeholder="e.g. cashback, lounge access"
        />
        <button onClick={handleSubmit}>Get Recommendations</button>
      </div>

      <div className="cards-wrapper">
        {cards.map((card, index) => (
          <div key={index} className="card">
            <img src={card.image} alt={card.name} className="card-img" />
            <h3>{card.name}</h3>
            <p><strong>Issuer:</strong> {card.issuer}</p>
            <p><strong>Reward Rate:</strong> {card.reward_rate}</p>
            <p><strong>Annual Fee:</strong> ₹{card.annual_fee}</p>
            <p><strong>Perks:</strong> {card.perks.join(', ')}</p>
            <p><strong>Estimated Savings:</strong> {card.estimated_savings}</p>
            <a href={card.apply_link} target="_blank" rel="noreferrer" className="apply-btn">Apply Now</a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
