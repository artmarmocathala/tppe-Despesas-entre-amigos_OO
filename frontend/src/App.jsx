import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [grupos, setGrupos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchGrupos = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:5000/grupos');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setGrupos(data);
        setError(null);
      } catch (err) {
        setError(err.message);
        setGrupos([]);
      } finally {
        setLoading(false);
      }
    };

    fetchGrupos();
  }, []);

  return (
    <>
      <h1>Despesas entre Amigos</h1>
      <h2>Grupos existentes:</h2>
      {loading && <p>Carregando...</p>}
      {error && <p style={{ color: 'red' }}>Erro ao buscar dados: {error}</p>}
      <ul>
        {grupos.map(grupo => (
          <li key={grupo.id}>{grupo.nome}</li>
        ))}
      </ul>
    </>
  );
}

export default App
