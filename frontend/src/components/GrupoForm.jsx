import { useState } from 'react';

export function GrupoForm({ onGroupCreated }) {
  const [nome, setNome] = useState('');
  const [maxPessoas, setMaxPessoas] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    const token = localStorage.getItem('authToken');

    const newGroup = {
      nome: nome,
      max_pessoas: maxPessoas ? parseInt(maxPessoas, 10) : null,
    };

    try {
      const response = await fetch('http://localhost:5000/grupos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(newGroup),
      });

      if (!response.ok) {
        throw new Error('Falha ao criar o grupo');
      }
      
      if (onGroupCreated) {
        onGroupCreated();
      }
      
    } catch (error) {
      console.error('Erro ao criar grupo:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Cadastrar Novo Grupo</h2>
      <div>
        <label htmlFor="nome">Nome do Grupo:</label>
        <input
          id="nome"
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="max_pessoas">Máx. de Pessoas (opcional):</label>
        <input
          id="max_pessoas"
          type="number"
          value={maxPessoas}
          onChange={(e) => setMaxPessoas(e.target.value)}
        />
      </div>
      <button type="submit">Criar Grupo</button>
    </form>
  );
}