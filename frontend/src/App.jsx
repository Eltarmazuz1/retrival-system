import { useState } from 'react'
import axios from 'axios'
import { Search, Loader2, FileText, AlertCircle } from 'lucide-react'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setError(null)
    setResults([])

    try {
      const response = await axios.get('http://127.0.0.1:5000/api/search', {
        params: { q: query }
      })
      setResults(response.data.results)
    } catch (err) {
      console.error(err)
      setError(err.response?.data?.error || 'Failed to fetch results. Ensure backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <div className="container">
        <header>
          <h1>Semantic Search Engine</h1>
          <p className="subtitle">Powered by RAG & OpenAI Embeddings</p>
        </header>

        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-wrapper">
            <Search className="search-icon" size={20} />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask something (e.g., 'history of gymnastics')..."
            />
            <button type="submit" disabled={loading || !query.trim()}>
              {loading ? <Loader2 className="spin" size={20} /> : 'Search'}
            </button>
          </div>
        </form>

        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            {error}
          </div>
        )}

        <div className="results-list">
          {results.map((result) => (
            <div key={result.id} className="result-card">
              <div className="result-header">
                <div className="result-meta">
                  <span className="result-id">ID: {result.id}</span>
                  <span className="result-line">
                    <FileText size={14} style={{ display: 'inline', marginRight: '4px' }} />
                    Line {result.metadata.line_number}
                  </span>
                </div>
                <div className="result-score">
                  Score: {(result.score * 100).toFixed(1)}%
                </div>
              </div>
              <p className="result-text">{result.document}</p>
            </div>
          ))}

          {results.length === 0 && !loading && !error && query && (
            <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '2rem' }}>
              No results found. Try a different query.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
