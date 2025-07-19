import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { GrupoForm } from '../components/GrupoForm';

export function ListaGrupos() {
  const [grupos, setGrupos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingGrupo, setEditingGrupo] = useState(null);
  const navigate = useNavigate();

  const fetchGrupos = async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      navigate('/login');
      return;
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/grupos/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.status === 401) {
        localStorage.removeItem('authToken');
        navigate('/login');
        return;
      }
      if (!response.ok) {
        throw new Error('Falha ao buscar os grupos');
      }
      const data = await response.json();
      setGrupos(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    fetchGrupos();
  }, []);

  const handleGroupCreated = () => {
    setIsModalOpen(false);
    fetchGrupos();
  };
  
  const handleGroupUpdated = () => {
    setEditingGrupo(null);
    fetchGrupos();
  };

  const handleDeleteGrupo = async (grupoId) => {
    if (!window.confirm("Tem certeza que deseja excluir este grupo?")) return;
    
    const token = localStorage.getItem('authToken');
    try {
      const response = await fetch(`http://127.0.0.1:5000/grupos/${grupoId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Falha ao deletar o grupo.");
      fetchGrupos();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Carregando grupos...</p>;
  if (error) return <p style={{ color: 'red' }}>Erro: {error}</p>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Lista de Grupos</h1>
        <button onClick={() => setIsModalOpen(true)}>Adicionar novo Grupo</button> 
      </div>

      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Nº de Pessoas</th>
            <th>Nº de Despesas</th>
            <th>Valor Total</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {grupos.map(grupo => (
            <tr key={grupo.id}>
              <td><Link to={`/grupos/${grupo.id}`}>{grupo.nome}</Link></td>
              <td>{grupo.qtd_pessoas}</td>
              <td>{grupo.qtd_despesas}</td>
              <td>R$ {grupo.total_despesas?.toFixed(2) || '0.00'}</td>
              <td>
                <button onClick={() => setEditingGrupo(grupo)}>Editar</button>
                <button onClick={() => handleDeleteGrupo(grupo.id)} style={{marginLeft: "5px"}}>Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {isModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button onClick={() => setIsModalOpen(false)} className="close-button">X</button>
            <GrupoForm onGroupCreated={handleGroupCreated} />
          </div>
        </div>
      )}

      {editingGrupo && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button onClick={() => setEditingGrupo(null)} className="close-button">X</button>
            <GrupoForm grupoToEdit={editingGrupo} onGroupUpdated={handleGroupUpdated} />
          </div>
        </div>
      )}
    </div>
  );
}