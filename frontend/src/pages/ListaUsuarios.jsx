import { useState, useEffect } from 'react';

export function ListaUsuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsuarios = async () => {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch('http://127.0.0.1:5000/usuarios/', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) {
          throw new Error('Você não tem permissão para ver esta página.');
        }
        const data = await response.json();
        setUsuarios(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchUsuarios();
  }, []);

  if (loading) return <p>Carregando usuários...</p>;

  return (
    <div>
      <h1>Gerenciamento de Usuários</h1>
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
                <button>Editar</button>
                <button style={{ marginLeft: '5px' }}>Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}