import { useState } from 'react';

export default function UsuarioForm({ usuarioToEdit, onUsuarioUpdated }) {
  const isEdit = !!usuarioToEdit;
  const [nome, setNome] = useState(usuarioToEdit?.nome || '');
  const [email, setEmail] = useState(usuarioToEdit?.email || '');
  const [isSuperuser, setIsSuperuser] = useState(usuarioToEdit?.is_superuser || false);
  const [senha, setSenha] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    const token = localStorage.getItem('authToken');
    try {
      const url = isEdit
        ? `http://127.0.0.1:5000/usuarios/${usuarioToEdit.id}`
        : 'http://127.0.0.1:5000/usuarios/';
      const method = isEdit ? 'PUT' : 'POST';
      const bodyObj = { nome, email, is_superuser: isSuperuser };
      if (!isEdit || senha) bodyObj.senha = senha;
      const body = JSON.stringify(bodyObj);
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      };
      const resp = await fetch(url, { method, headers, body });
      if (!resp.ok) throw new Error('Erro ao salvar usuário.');
      onUsuarioUpdated && onUsuarioUpdated();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ minWidth: 300 }}>
      <h3>{isEdit ? 'Editar Usuário' : 'Criar Usuário'}</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <label>Nome:</label>
        <input value={nome} onChange={e => setNome(e.target.value)} required />
      </div>
      <div>
        <label>Email:</label>
        <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            checked={isSuperuser}
            onChange={e => setIsSuperuser(e.target.checked)}
          />{' '}
          Superusuário (Admin)?
        </label>
      </div>
      <div>
        <label>Senha:{!isEdit && <span style={{color:'red'}}> *</span>}</label>
        <input
          type="password"
          value={senha}
          onChange={e => setSenha(e.target.value)}
          placeholder={isEdit ? 'Deixe em branco para não alterar' : ''}
          required={!isEdit}
        />
      </div>
      <button type="submit" disabled={loading}>
        {isEdit ? 'Salvar Alterações' : 'Criar Usuário'}
      </button>
    </form>
  );
}
