import { useState, useEffect } from 'react';
import UsuarioForm from '../components/UsuarioForm';

export function ListaUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingUsuario, setEditingUsuario] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [creating, setCreating] = useState(false);

  const fetchUsuarios = async () => {
    const token = localStorage.getItem('authToken');
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/usuarios/', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Você não tem permissão para ver esta página.');
      const data = await response.json();
      setUsuarios(data);
    } catch (err) {
      setUsuarios([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchUsuarios(); }, []);

  const handleDeleteUsuario = async (usuarioId) => {
    if (!window.confirm('Tem certeza que deseja excluir este usuário?')) return;
    const token = localStorage.getItem('authToken');
    try {
      const resp = await fetch(`http://127.0.0.1:5000/usuarios/${usuarioId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!resp.ok) throw new Error('Erro ao excluir usuário.');
      fetchUsuarios();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleUsuarioUpdated = () => {
    setEditingUsuario(null);
    setModalOpen(false);
    fetchUsuarios();
  };

  if (loading) return <p>Carregando usuários...</p>;

  return (
    <div>
      <h1>Gerenciamento de Usuários</h1>
      <button onClick={() => { setCreating(true); setEditingUsuario(null); setModalOpen(true); }} style={{ marginBottom: 16 }}>
        Criar Novo Usuário
      </button>
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Email</th>
            <th>Admin?</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map(usuario => (
            <tr key={usuario.id}>
              <td>{usuario.nome}</td>
              <td>{usuario.email}</td>
              <td>{usuario.is_superuser ? 'Sim' : 'Não'}</td>
              <td>
                <button onClick={() => { setEditingUsuario(usuario); setModalOpen(true); }}>Editar</button>
                <button style={{ marginLeft: '5px' }} onClick={() => handleDeleteUsuario(usuario.id)}>Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {modalOpen && (
        <div style={{
          position: 'fixed', top: 0, left: 0, width: '100vw', height: '100vh',
          background: 'rgba(0,0,0,0.3)', display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          <div style={{ background: 'white', padding: 24, borderRadius: 8, minWidth: 350 }}>
            <UsuarioForm usuarioToEdit={creating ? null : editingUsuario} onUsuarioUpdated={handleUsuarioUpdated} />
            <button onClick={() => { setModalOpen(false); setEditingUsuario(null); setCreating(false); }} style={{ marginTop: 16 }}>Fechar</button>
          </div>
        </div>
      )}
    </div>
  );
}