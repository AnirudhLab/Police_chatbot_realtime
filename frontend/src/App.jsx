
import { useState } from 'react';
import './App.css';

const API_URL = '/api/chat';

function App() {
  const [query, setQuery] = useState('');
  const [language, setLanguage] = useState('en');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, language })
      });
      if (!res.ok) throw new Error('Server error');
      const data = await res.json();
      setResult(data);
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
      {result && (
        <div className="result">
          <h2>Main Answer</h2>
          <div className="main-answer">{result.main_answer}</div>
          {result.legal_references && result.legal_references.length > 0 && (
            <div className="references">
              <h3>Legal References</h3>
              <ul>
                {result.legal_references.map((ref, i) => (
                  <li key={i}>
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
      <footer>
        <small>Powered by Tamil Nadu Police Legal Chatbot</small>
      </footer>
    </div>
  );
}

export default App;
