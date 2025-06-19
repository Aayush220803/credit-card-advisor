import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [income, setIncome] = useState('');
  const [spending, setSpending] = useState([]);
  const [preferences, setPreferences] = useState([]);
  const [creditScore, setCreditScore] = useState('');
  const [response, setResponse] = useState('');

  const toggleSelection = (value, list, setList) => {
    setList(
      list.includes(value)
        ? list.filter((v) => v !== value)
        : [...list, value]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const message = `Use the tool with this input: {"income": ${income}, "spending": "${spending.join(',')}", "preferences": "${preferences.join(',')}", "credit_score": "${creditScore}"}`;

    try {
      const res = await axios.post('http://127.0.0.1:8000/chat', { message });
      setResponse(res.data.response);
    } catch (err) {
      setResponse('An error occurred while getting recommendations.');
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="form-card">
        <div className="form-header">
          <img src="/logo.png" alt="Logo" className="logo" />
          <h1>Credit Card Recommendation</h1>
          <p>Let’s find the best credit card for you. Please answer a few questions to help us tailor our recommendation.</p>
        </div>

        <label>What is your monthly income?</label>
        <input
          type="number"
          value={income}
          onChange={(e) => setIncome(e.target.value)}
          placeholder="e.g. ₹50,000"
          required
        />

        <label>What are your spending habits?</label>
        <div className="checkbox-group">
          {['Fuel', 'Travel', 'Groceries', 'Dining'].map((item) => (
            <label key={item}>
              <input
                type="checkbox"
                checked={spending.includes(item.toLowerCase())}
                onChange={() => toggleSelection(item.toLowerCase(), spending, setSpending)}
              /> {item}
            </label>
          ))}
        </div>

        <label>What benefits do you prefer?</label>
        <div className="checkbox-group">
          {['Cashback', 'Travel points', 'Lounge access'].map((item) => (
            <label key={item}>
              <input
                type="checkbox"
                checked={preferences.includes(item.toLowerCase())}
                onChange={() => toggleSelection(item.toLowerCase(), preferences, setPreferences)}
              /> {item}
            </label>
          ))}
        </div>

        <label>What is your approximate credit score?</label>
        <div className="radio-group">
          {['Below 700', '700-750', 'Above 750'].map((item) => (
            <label key={item}>
              <input
                type="radio"
                value={item}
                checked={creditScore === item}
                onChange={(e) => setCreditScore(e.target.value)}
              /> {item}
            </label>
          ))}
        </div>

        <button type="submit">Submit</button>
      </form>

      {response && (
        <div className="response-card">
          <h2>Recommended Cards</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default App;