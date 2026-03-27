import { useState, useEffect } from 'react'
import './App.css'

type Verdict = 'Kept' | 'Broken' | 'Pending' | 'Unverifiable'

interface EvidenceQuote {
  text: string
  date: string
  url: string
}

interface CheckResult {
  verdict: Verdict
  confidence: number
  reasoning: string
  evidence_quotes: EvidenceQuote[]
  scope_note: string
}

interface Promise {
  id: string
  politician: string
  promise: string
  source: string
  category: string
}

const VERDICT_COLOURS: Record<Verdict, string> = {
  Kept: '#22c55e',
  Broken: '#ef4444',
  Pending: '#f59e0b',
  Unverifiable: '#94a3b8',
}

export default function App() {
  const [promises, setPromises] = useState<Promise[]>([])
  const [selectedPromise, setSelectedPromise] = useState<Promise | null>(null)
  const [customPolitician, setCustomPolitician] = useState('')
  const [customPromise, setCustomPromise] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CheckResult | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('http://localhost:8000/promises')
      .then(r => r.json())
      .then(setPromises)
      .catch(() => {})
  }, [])

  const handleCheck = async () => {
    setError('')
    setResult(null)
    setLoading(true)

    const politician = selectedPromise?.politician || customPolitician
    const promise = selectedPromise?.promise || customPromise
    const source = selectedPromise?.source || ''

    if (!politician || !promise) {
      setError('Please enter a politician and a promise.')
      setLoading(false)
      return
    }

    try {
      const resp = await fetch('http://localhost:8000/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ politician_name: politician, promise, promise_source: source }),
      })
      if (!resp.ok) {
        const err = await resp.json()
        throw new Error(err.detail || 'Something went wrong')
      }
      setResult(await resp.json())
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectPromise = (p: Promise) => {
    setSelectedPromise(p)
    setCustomPolitician('')
    setCustomPromise('')
    setResult(null)
  }

  const handleCustomMode = () => {
    setSelectedPromise(null)
    setResult(null)
  }

  return (
    <div className="app">
      <header>
        <h1>Promise Tracker</h1>
        <p className="subtitle">Did they keep their word? Checked against the Dáil record.</p>
      </header>

      <main>
        <section className="input-section">
          <h2>Pick a promise</h2>
          <div className="promise-list">
            {promises.map(p => (
              <button
                key={p.id}
                className={`promise-card ${selectedPromise?.id === p.id ? 'selected' : ''}`}
                onClick={() => handleSelectPromise(p)}
              >
                <span className="category">{p.category}</span>
                <span className="politician">{p.politician}</span>
                <span className="promise-text">"{p.promise}"</span>
                <span className="source">{p.source}</span>
              </button>
            ))}
          </div>

          <div className="divider">or enter your own</div>

          <div className="custom-inputs">
            <input
              type="text"
              placeholder="Politician name"
              value={customPolitician}
              onChange={e => { setCustomPolitician(e.target.value); handleCustomMode() }}
            />
            <textarea
              placeholder="Enter a promise..."
              value={customPromise}
              onChange={e => { setCustomPromise(e.target.value); handleCustomMode() }}
              rows={3}
            />
          </div>

          <button className="check-btn" onClick={handleCheck} disabled={loading}>
            {loading ? 'Checking Dáil record...' : 'Check Promise'}
          </button>

          {error && <p className="error">{error}</p>}
        </section>

        {result && (
          <section className="result-section">
            <div className="verdict-card" style={{ borderColor: VERDICT_COLOURS[result.verdict] }}>
              <div className="verdict-badge" style={{ backgroundColor: VERDICT_COLOURS[result.verdict] }}>
                {result.verdict}
              </div>
              <div className="confidence">{result.confidence}% confidence</div>
            </div>

            <p className="reasoning">{result.reasoning}</p>

            {result.evidence_quotes.length > 0 && (
              <div className="quotes">
                <h3>Evidence from Dáil record</h3>
                {result.evidence_quotes.map((q, i) => (
                  <blockquote key={i}>
                    <p>"{q.text}"</p>
                    <footer>
                      {q.date}
                      {q.url && <> · <a href={q.url} target="_blank" rel="noopener noreferrer">Source</a></>}
                    </footer>
                  </blockquote>
                ))}
              </div>
            )}

            <p className="scope-note">{result.scope_note}</p>
          </section>
        )}
      </main>
    </div>
  )
}
