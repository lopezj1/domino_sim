import React, { useState } from 'react'
import './styles/App.css'

function App() {
  const [status, setStatus] = useState<string>('Checking...')

  React.useEffect(() => {
    // Test backend connection
    fetch('http://127.0.0.1:8001/health')
      .then(res => res.json())
      .then(data => setStatus(`Backend: ${data.status}`))
      .catch(() => setStatus('Backend: disconnected'))
  }, [])

  return (
    <div className="app">
      <header className="header">
        <h1>🎲 Domino Simulation</h1>
        <p className="subtitle">Monte Carlo Strategy Analysis with Visualization</p>
      </header>

      <main className="main">
        <div className="status-card">
          <h2>System Status</h2>
          <p className="status">{status}</p>
        </div>

        <div className="features">
          <div className="feature-card">
            <h3>🎮 Game Engine</h3>
            <p>Discrete Event Simulation with 3 strategies</p>
            <ul>
              <li>Greedy Strategy</li>
              <li>Random Strategy</li>
              <li>Blocking Strategy</li>
            </ul>
          </div>

          <div className="feature-card">
            <h3>📊 Monte Carlo Analysis</h3>
            <p>Statistical strategy comparison</p>
            <ul>
              <li>Batch simulation</li>
              <li>95% confidence intervals</li>
              <li>Full reproducibility</li>
            </ul>
          </div>

          <div className="feature-card">
            <h3>📈 Visualization</h3>
            <p>Convergence path analysis</p>
            <ul>
              <li>Multiple simulation paths</li>
              <li>Uncertainty quantification</li>
              <li>Convergence demonstration</li>
            </ul>
          </div>
        </div>

        <div className="quick-start">
          <h2>Quick Start</h2>
          <div className="api-info">
            <h3>Available API Endpoints:</h3>
            <ul>
              <li><code>GET /health</code> - Health check</li>
              <li><code>GET /visualization/strategies</code> - List strategies</li>
              <li><code>POST /visualization/monte-carlo-paths</code> - Generate visualization data</li>
            </ul>
            
            <h3>API Documentation:</h3>
            <p>
              <a href="http://127.0.0.1:8001/docs" target="_blank" rel="noopener noreferrer">
                Open Swagger UI →
              </a>
            </p>
          </div>
        </div>

        <div className="coming-soon">
          <h2>🚧 Coming Soon</h2>
          <p>Interactive UI components are being implemented:</p>
          <ul>
            <li>Strategy selector</li>
            <li>Game simulation controls</li>
            <li>Monte Carlo path chart (Recharts)</li>
            <li>Results dashboard</li>
          </ul>
          <p className="note">
            For now, you can use the API directly via the Swagger UI or command line tools.
          </p>
        </div>
      </main>

      <footer className="footer">
        <p>Domino Simulation MVP - Phase 3.5 Complete</p>
        <p>Backend: FastAPI | Frontend: React + TypeScript + Vite</p>
      </footer>
    </div>
  )
}

export default App
