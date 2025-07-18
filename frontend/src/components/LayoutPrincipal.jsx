import { Outlet, Link } from 'react-router-dom';

export function LayoutPrincipal() {
  return (
    <div style={{ display: 'flex' }}>
      <aside style={{ width: '200px', borderRight: '1px solid #ccc', padding: '1rem' }}>
        <h2>Menu</h2>
        <nav>
          <ul>
            <li><Link to="/">Home</Link></li>
            <li><Link to="/grupos">Grupos</Link></li>
            {/* Adicione outros links aqui */}
          </ul>
        </nav>
      </aside>

      <main style={{ flex: 1, padding: '1rem' }}>
        {/* O <Outlet /> é o placeholder onde as páginas filhas serão renderizadas */}
        <Outlet />
      </main>
    </div>
  );
}