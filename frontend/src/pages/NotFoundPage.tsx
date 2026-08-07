import { useRouteError } from "react-router-dom";

export default function NotFoundPage() {
  const error = useRouteError() as { status?: number; statusText?: string; message?: string } | null;
  return (
    <div style={{
      display: 'flex', flexDirection: 'column', alignItems: 'center',
      justifyContent: 'center', minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
      color: '#f1f5f9', fontFamily: 'Inter, system-ui, sans-serif',
      textAlign: 'center', padding: '2rem'
    }}>
      <div style={{ fontSize: '6rem', marginBottom: '1rem' }}>🛡️</div>
      <h1 style={{ fontSize: '2.5rem', fontWeight: 700, marginBottom: '0.5rem', color: '#6366f1' }}>
        {error?.status === 404 ? '404' : 'Oops!'}
      </h1>
      <p style={{ fontSize: '1.25rem', color: '#94a3b8', marginBottom: '0.5rem' }}>
        {error?.status === 404 ? 'Page not found' : (error?.statusText || 'Unexpected error')}
      </p>
      <p style={{ color: '#64748b', marginBottom: '2rem' }}>
        {error?.message || 'The page you are looking for does not exist.'}
      </p>
      <a href="/dashboard" style={{
        background: '#6366f1', color: '#fff', padding: '0.75rem 2rem',
        borderRadius: '0.5rem', textDecoration: 'none', fontWeight: 600,
        fontSize: '1rem'
      }}>← Return to Dashboard</a>
    </div>
  );
}
