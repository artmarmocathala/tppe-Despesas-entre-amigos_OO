import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';

export function Configuracoes() {
  const navigate = useNavigate();
  
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [loading, setLoading] = useState(true);

  const getUserIdFromToken = () => {
    const token = localStorage.getItem('authToken');
    if (!token) return null;
    try {
      return jwtDecode(token).sub;
    } catch (e) {
      return null;
    }
  };

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('authToken');
      if (!token) { 
        navigate('/login'); 
        return; 
      }
      try {
        const response = await fetch(`http://127.0.0.1:5000/usuarios/me`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Falha ao buscar dados do perfil.');
        const data = await response.json();
        setNome(data.nome);
        setEmail(data.email);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [navigate]);

  const handleUpdateProfile = async (event) => {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    
    const token = localStorage.getItem('authToken');
    const userId = getUserIdFromToken();
    if (!userId) return;

    try {
      const response = await fetch(`http://127.0.0.1:5000/usuarios/${userId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ nome, email }),
      });

      if (!response.ok) throw new Error('Falha ao atualizar perfil.');
      
      setSuccess('Perfil atualizado com sucesso!');
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDeleteAccount = async () => {
    if (!window.confirm("ATENÇÃO: Esta ação é irreversível. Tem certeza que deseja excluir sua conta e todos os seus dados?")) {
      return;
    }

    setError(null);
    const token = localStorage.getItem('authToken');
    const userId = getUserIdFromToken();
    if (!userId) return;

    try {
      const response = await fetch(`http://127.0.0.1:5000/usuarios/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (!response.ok) throw new Error('Falha ao excluir a conta.');

      localStorage.removeItem('authToken');
      localStorage.removeItem('isSuperuser');
      alert('Conta excluída com sucesso.');
      navigate('/login');

    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Carregando configurações...</p>;

  return (
    <div>
      <h1>Configurações da Conta</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {success && <p style={{ color: 'green' }}>{success}</p>}

      <form onSubmit={handleUpdateProfile} style={{ marginBottom: '2rem' }}>
        <h3>Alterar Perfil</h3>
        <div>
          <label htmlFor="nome">Nome de Usuário</label>
          <input id="nome" type="text" value={nome} onChange={e => setNome(e.target.value)} />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input id="email" type="email" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <button type="submit">Salvar Alterações do Perfil</button>
      </form>

      <hr />

      <div style={{ marginTop: '2rem', border: '1px solid red', padding: '1rem' }}>
        <h3>Área de Perigo</h3>
        <p>A exclusão da sua conta é permanente e removerá todos os seus grupos e dados associados.</p>
        <button onClick={handleDeleteAccount} style={{ backgroundColor: '#dc3545', color: 'white' }}>
          Excluir Minha Conta
        </button>
      </div>
    </div>
  );
}