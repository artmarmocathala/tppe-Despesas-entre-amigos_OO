import { useState, useEffect } from 'react';

export function GrupoForm({ onGroupCreated, grupoToEdit, onGroupUpdated }) {
  const [nome, setNome] = useState('');
  const [maxPessoas, setMaxPessoas] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (grupoToEdit) {
      setNome(grupoToEdit.nome);
      setMaxPessoas(grupoToEdit.max_pessoas || '');
    }
  }, [grupoToEdit]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    const token = localStorage.getItem('authToken');

    const grupoData = {
      nome,
      max_pessoas: maxPessoas ? parseInt(maxPessoas, 10) : null,
    };

    const isEditing = !!grupoToEdit;
    const method = isEditing ? 'PUT' : 'POST';
    const endpoint = isEditing
      ? `http://127.0.0.1:5000/grupos/${grupoToEdit.id}`
      : 'http://127.0.0.1:5000/grupos/';

    try {
      const response = await fetch(endpoint, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(grupoData),
      });

      if (!response.ok) {
        throw new Error(`Falha ao ${isEditing ? 'atualizar' : 'criar'} grupo`);
      }

      if (isEditing) {
        if (onGroupUpdated) onGroupUpdated();
      } else {
        if (onGroupCreated) onGroupCreated();
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>{grupoToEdit ? 'Editar Grupo' : 'Adicionar Novo Grupo'}</h3>
      <div>
        <label htmlFor="nome-grupo">Nome do Grupo:</label>
        <input
          id="nome-grupo"
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="max_pessoas-grupo">Máx. de Pessoas (opcional):</label>
        <input
          id="max_pessoas-grupo"
          type="number"
          value={maxPessoas}
          onChange={(e) => setMaxPessoas(e.target.value)}
        />
      </div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Salvar</button>
    </form>
  );
}