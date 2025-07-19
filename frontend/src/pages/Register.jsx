import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export function Register() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/usuarios/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nome: nome, email: email, senha: password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Falha ao registrar');
      }

      alert('Usuário registrado com sucesso! Faça o login para continuar.');
      navigate('/login');

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Registrar</h1>
      <p>Informe seus dados para criar uma conta.</p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Nome de Usuário</label>
          <input
            id="name"
            type="text"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Senha</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <button type="submit">Registrar</button>
      </form>
      <p>
        Já tem uma conta? <Link to="/login">Faça o login</Link>
      </p>
    </div>
  );
}