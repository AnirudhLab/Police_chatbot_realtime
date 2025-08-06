import React, { useState } from 'react';
import './App.css';
import './App.css';


function App() {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('ta');
  const [response, setResponse] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse(null);
    try {
      const apiUrl = process.env.NODE_ENV === 'production' 
        ? '/api/chat' 
        : 'http://127.0.0.1:5000/api/chat';
      
      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, language })
      });
      if (!res.ok) throw new Error('Server error');
      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError('Failed to get response. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chatbot-container">
      <h1>Police Chatbot</h1>
      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Type your question..."
          rows={3}
          required
        />
        <div className="form-row">
          <label>
            Language:
            <select value={language} onChange={e => setLanguage(e.target.value)}>
              <option value="en">English</option>
              <option value="ta">தமிழ் (Tamil)</option>
            </select>
          </label>
          <button type="submit" disabled={loading || !query.trim()}>
            {loading ? 'Loading...' : 'Ask'}
          </button>
        </div>
      </form>
      {error && <div className="error">{error}</div>}
      {response && (
        <div className="result">
          <h2 style={{marginBottom: '0.7rem', color:'#90caf9'}}>Main Answer</h2>
          <div className="main-answer">{response.main_answer}</div>
          {response.legal_references && response.legal_references.length > 0 && (
            <div className="references">
              <h3>Legal References</h3>
              <ul>
                {response.legal_references.map((ref, idx) => (
                  <li key={idx}>
                    <strong>{ref.name}</strong> <span className="category">({ref.category})</span>
                    <div><b>Summary:</b> {ref.summary}</div>
                    <div><b>When Applicable:</b> {ref.when_applicable}</div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
