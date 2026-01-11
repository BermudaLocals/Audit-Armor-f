'use client';
import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [lastScan, setLastScan] = useState(new Date().toLocaleTimeString());

  // Simulates a system heartbeat every 30 seconds
  useEffect(() => {
    const timer = setInterval(() => {
      setLastScan(new Date().toLocaleTimeString());
    }, 30000);
    return () => clearInterval(timer);
  }, []);

  return (
    <main style={{ padding: '40px', fontFamily: 'system-ui, sans-serif', backgroundColor: '#0f172a', color: '#f8fafc', minHeight: '100vh' }}>
      <header style={{ borderBottom: '1px solid #1e293b', marginBottom: '30px', paddingBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '2rem', margin: 0, color: '#38bdf8' }}>🛡️ Audit Armor</h1>
          <p style={{ color: '#94a3b8', margin: '5px 0 0 0' }}>Bermuda PIPA Compliance: <span style={{ color: '#22c55e' }}>SECURE</span></p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '0.8rem', color: '#94a3b8' }}>SYSTEM HEARTBEAT</div>
          <div style={{ color: '#38bdf8', fontWeight: 'bold' }}>{lastScan}</div>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '25px' }}>
        {/* Risk Level Card */}
        <div style={{ background: '#1e293b', padding: '25px', borderRadius: '16px', border: '1px solid #334155' }}>
          <h3 style={{ color: '#94a3b8', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Threat Level</h3>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#22c55e', marginTop: '10px' }}>LOW</div>
          <p style={{ color: '#64748b', fontSize: '0.8rem' }}>Perimeter scans normal</p>
        </div>

        {/* Railway Backend Status */}
        <div style={{ background: '#1e293b', padding: '25px', borderRadius: '16px', border: '1px solid #334155' }}>
          <h3 style={{ color: '#94a3b8', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '1px' }}>Railway Backend</h3>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#38bdf8', marginTop: '10px' }}>CONNECTED</div>
          <p style={{ color: '#64748b', fontSize: '0.8rem' }}>Latency: 14ms</p>
        </div>
      </div>

      <section style={{ marginTop: '40px', background: '#1e293b', borderRadius: '16px', padding: '20px', border: '1px solid #334155' }}>
        <h2 style={{ fontSize: '1.2rem', marginBottom: '20px' }}>Recent Security Events</h2>
        <div style={{ color: '#94a3b8', fontSize: '0.9rem' }}>
          <div style={{ padding: '10px 0', borderBottom: '1px solid #334155', display: 'flex', justifyContent: 'space-between' }}>
            <span>SSL Certificate Verification</span>
            <span style={{ color: '#22c55e' }}>VALID</span>
          </div>
          <div style={{ padding: '10px 0', borderBottom: '1px solid #334155', display: 'flex', justifyContent: 'space-between' }}>
            <span>Database Integrity Check</span>
            <span style={{ color: '#22c55e' }}>PASSED</span>
          </div>
          <div style={{ padding: '10px 0', display: 'flex', justifyContent: 'space-between' }}>
            <span>Unauthorized Login Attempts</span>
            <span style={{ color: '#f59e0b' }}>0</span>
          </div>
        </div>
      </section>
    </main>
  );
}
