import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';

export function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);

    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: email, senha: password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Falha no login');
      }
      
      localStorage.setItem('authToken', data.token);

      navigate('/');

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Fazer Login</h1>
      <p>Insira suas informações de login para acessar sua conta.</p>
      
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="Insira seu email"
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
            placeholder="Insira sua senha"
          />
        </div>

        {error && <p style={{ color: 'red' }}>{error}</p>}

        <button type="submit">Login</button>
      </form>
      
      <p>
        Não tem uma conta? <Link to="/registrar">Registre-se</Link>
      </p>
      <p>
        Esqueceu sua senha? <Link to="/recuperar-senha">Resetar Senha</Link>
      </p>
    </div>
  );
}