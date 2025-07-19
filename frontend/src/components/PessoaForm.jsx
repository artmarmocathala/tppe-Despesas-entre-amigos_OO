import { useState, useEffect } from 'react';

/**
 * Formulário para criar ou editar uma pessoa.
 * @param {string} grupoId
 * @param {function} onPessoaCreated
 * @param {object} pessoaToEdit
 * @param {function} onPessoaUpdated
 */
export function PessoaForm({ grupoId, onPessoaCreated, pessoaToEdit, onPessoaUpdated }) {
  const [nome, setNome] = useState('');
  const [cpf, setCpf] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (pessoaToEdit) {
      setNome(pessoaToEdit.nome);
      setCpf(pessoaToEdit.cpf);
    }
  }, [pessoaToEdit]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    const token = localStorage.getItem('authToken');

    const pessoaData = { nome, cpf };
    
    const isEditing = !!pessoaToEdit;
    const method = isEditing ? 'PUT' : 'POST';
    const endpoint = isEditing 
      ? `http://127.0.0.1:5000/pessoas/${pessoaToEdit.id}`
      : `http://127.0.0.1:5000/grupos/${grupoId}/pessoas`;

    try {
      const response = await fetch(endpoint, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(pessoaData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.description || `Falha ao ${isEditing ? 'atualizar' : 'adicionar'} pessoa`);
      }
      
      if (isEditing) {
        if (onPessoaUpdated) onPessoaUpdated();
      } else {
        if (onPessoaCreated) onPessoaCreated();
      }
      
    } catch (err) {
      setError(err.message);
      console.error('Erro:', err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>{pessoaToEdit ? 'Editar Pessoa' : 'Adicionar Nova Pessoa'}</h3>
      
      <div>
        <label htmlFor="nome-pessoa">Nome:</label>
        <input
          id="nome-pessoa"
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="cpf-pessoa">CPF:</label>
        <input
          id="cpf-pessoa"
          type="text"
          value={cpf}
          onChange={(e) => setCpf(e.target.value)}
          required
        />
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Salvar</button>
    </form>
  );
}