import { Outlet, Link, useNavigate } from 'react-router-dom';

export function LayoutPrincipal() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/login');
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <aside style={{ width: '220px', background: '#f4f4f4', padding: '1rem', borderRight: '1px solid #ddd' }}>
        <h2>Despesas</h2>
        <nav>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            <li style={{ marginBottom: '1rem' }}><Link to="/">Home</Link></li>
            <li style={{ marginBottom: '1rem' }}><Link to="/grupos">Grupos</Link></li>
            <li style={{ marginBottom: '1rem' }}><Link to="/usuarios">Usuários</Link></li>
            <li style={{ marginBottom: '1rem' }}><Link to="/configuracoes">Configurações</Link></li>
          </ul>
        </nav>
        
        <button onClick={handleLogout} style={{ position: 'absolute', bottom: '20px' }}>
          Sair
        </button>
      </aside>

      <main style={{ flex: 1, padding: '2rem' }}>
        <Outlet />
      </main>
    </div>
  );
}