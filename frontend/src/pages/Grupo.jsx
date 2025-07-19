import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { PessoaForm } from '../components/PessoaForm';
import { DespesaForm } from '../components/DespesaForm';

export function Grupo() {
  const { id } = useParams();
  const [grupo, setGrupo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const [isPessoaModalOpen, setIsPessoaModalOpen] = useState(false);
  const [isDespesaModalOpen, setIsDespesaModalOpen] = useState(false);
  const [editingPessoa, setEditingPessoa] = useState(null);
  const [editingDespesa, setEditingDespesa] = useState(null);

  const fetchDetalhesGrupo = async () => {
    const token = localStorage.getItem('authToken');
    if (!token) {
      navigate('/login');
      return;
    }
    try {
      if (!loading) setLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/grupos/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) {
        throw new Error('Falha ao buscar detalhes do grupo');
      }
      const data = await response.json();
      setGrupo(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetalhesGrupo();
  }, [id]);

  const handlePessoaCreated = () => { setIsPessoaModalOpen(false); fetchDetalhesGrupo(); };
  const handlePessoaUpdated = () => { setEditingPessoa(null); fetchDetalhesGrupo(); };
  const handleDeletePessoa = async (pessoaId) => {
    if (!window.confirm("Tem certeza que deseja excluir esta pessoa?")) return;
    const token = localStorage.getItem('authToken');
    try {
      const response = await fetch(`http://127.0.0.1:5000/pessoas/${pessoaId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Falha ao deletar pessoa.");
      fetchDetalhesGrupo();
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDespesaCreated = () => { setIsDespesaModalOpen(false); fetchDetalhesGrupo(); };
  const handleDespesaUpdated = () => { setEditingDespesa(null); fetchDetalhesGrupo(); };
  const handleDeleteDespesa = async (despesa) => {
    if (!window.confirm("Tem certeza que deseja excluir esta despesa?")) return;
    const token = localStorage.getItem('authToken');
    const endpoint = `http://127.0.0.1:5000/despesas/${despesa.tipo}s/${despesa.id}`;
    try {
      const response = await fetch(endpoint, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Falha ao deletar despesa.");
      fetchDetalhesGrupo();
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) return <p>Carregando detalhes do grupo...</p>;
  if (error) return <p style={{ color: 'red' }}>Erro: {error}</p>;
  if (!grupo) return <p>Grupo não encontrado.</p>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>{grupo.nome}</h1>
        <div>
          <button onClick={() => setIsPessoaModalOpen(true)}>Adicionar nova Pessoa</button>
          <button onClick={() => setIsDespesaModalOpen(true)} style={{ marginLeft: '10px' }}>Adicionar nova Despesa</button>
        </div>
      </div>

      <hr />

      <h2>Pessoas no Grupo ({grupo.pessoas.length})</h2>
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>CPF</th>
            <th style={{ textAlign: 'right' }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {grupo.pessoas.map(pessoa => (
            <tr key={pessoa.id}>
              <td>{pessoa.nome}</td>
              <td>{pessoa.cpf}</td>
              <td style={{ textAlign: 'right' }}>
                <button onClick={() => setEditingPessoa(pessoa)}>Editar</button>
                <button onClick={() => handleDeletePessoa(pessoa.id)} style={{ marginLeft: '5px' }}>Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <hr />

      <h2>Despesas ({grupo.despesas.length})</h2>
      <table>
        <thead>
          <tr>
            <th>Tipo</th>
            <th>Valor</th>
            <th>Data</th>
            <th style={{ textAlign: 'right' }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {grupo.despesas.map(despesa => (
            <tr key={despesa.id}>
              <td>{despesa.tipo.charAt(0).toUpperCase() + despesa.tipo.slice(1)}</td>
              <td>R$ {despesa.valor.toFixed(2)}</td>
              <td>{new Date(despesa.data).toLocaleDateString()}</td>
              <td style={{ textAlign: 'right' }}>
                <button onClick={() => setEditingDespesa(despesa)}>Editar</button>
                <button onClick={() => handleDeleteDespesa(despesa)} style={{ marginLeft: '5px' }}>Excluir</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <hr />
      
      <h2>Divisão de Despesas</h2>
      {grupo.divisao.error ? (
        <p style={{ color: 'orange' }}>{grupo.divisao.error}</p>
      ) : (
        <div>
          <p><strong>Total das Despesas:</strong> R$ {grupo.divisao.total_despesas?.toFixed(2)}</p>
          <p><strong>Valor por Pessoa:</strong> R$ {grupo.divisao.valor_por_pessoa?.toFixed(2)}</p>
        </div>
      )}

      {/* --- Modais --- */}
      {isPessoaModalOpen && (
        <div className="modal-overlay"><div className="modal-content">
            <button onClick={() => setIsPessoaModalOpen(false)} className="close-button">X</button>
            <PessoaForm grupoId={id} onPessoaCreated={handlePessoaCreated} />
        </div></div>
      )}
      {editingPessoa && (
        <div className="modal-overlay"><div className="modal-content">
            <button onClick={() => setEditingPessoa(null)} className="close-button">X</button>
            <PessoaForm pessoaToEdit={editingPessoa} onPessoaUpdated={handlePessoaUpdated} />
        </div></div>
      )}
      {isDespesaModalOpen && (
        <div className="modal-overlay"><div className="modal-content">
            <button onClick={() => setIsDespesaModalOpen(false)} className="close-button">X</button>
            <DespesaForm grupoId={id} pessoas={grupo.pessoas} onDespesaCreated={handleDespesaCreated} />
        </div></div>
      )}
      {editingDespesa && (
        <div className="modal-overlay"><div className="modal-content">
            <button onClick={() => setEditingDespesa(null)} className="close-button">X</button>
            <DespesaForm pessoas={grupo.pessoas} despesaToEdit={editingDespesa} onDespesaUpdated={handleDespesaUpdated} />
        </div></div>
      )}
    </div>
  );
}