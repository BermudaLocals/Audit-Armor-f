export default function Page() {
  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif', backgroundColor: '#0a0a0a', color: '#fff', minHeight: '100vh' }}>
      <h1 style={{ color: '#00ff88' }}>🛡️ AUDIT ARMOR DASHBOARD</h1>
      <p>Status: <span style={{ color: '#00ff88' }}>INSTITUTIONAL GRADE ACTIVE</span></p>
      <hr style={{ borderColor: '#333' }} />
      <div style={{ marginTop: '20px', padding: '20px', border: '1px solid #333', borderRadius: '8px' }}>
        <h3>System Overview</h3>
        <p>Bermuda PIPA Compliance: 🟢 Encrypted</p>
        <p>Backend Connection: 🟢 Connected to Railway</p>
      </div>
    </div>
  );
}
