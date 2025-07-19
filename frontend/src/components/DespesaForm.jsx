import { useState, useEffect } from 'react';

export function DespesaForm({ grupoId, pessoas, onDespesaCreated, despesaToEdit, onDespesaUpdated }) {
  const [tipo, setTipo] = useState('compra');
  const [valor, setValor] = useState('');
  const [data, setData] = useState('');
  const [pagadorId, setPagadorId] = useState('');
  
  const [nomeMercado, setNomeMercado] = useState('');
  const [endereco, setEndereco] = useState('');
  const [itens, setItens] = useState(['']);

  const [error, setError] = useState(null);

  useEffect(() => {
    if (despesaToEdit) {
      setTipo(despesaToEdit.tipo);
      setValor(despesaToEdit.valor);
      setData(new Date(despesaToEdit.data).toISOString().split('T')[0]);
      setPagadorId(despesaToEdit.pagador_id);
      
      if (despesaToEdit.tipo === 'compra') {
        setNomeMercado(despesaToEdit.nome_mercado || '');
        setItens(despesaToEdit.itens && despesaToEdit.itens.length > 0 ? despesaToEdit.itens : ['']);
      } else if (despesaToEdit.tipo === 'imovel') {
        setEndereco(despesaToEdit.endereco || '');
      }
    }
  }, [despesaToEdit]);

  const handleItemChange = (index, value) => {
    const novosItens = [...itens];
    novosItens[index] = value;
    setItens(novosItens);
  };

  const handleAddItem = () => {
    setItens([...itens, '']);
  };

  const handleRemoveItem = (index) => {
    const novosItens = itens.filter((_, i) => i !== index);
    setItens(novosItens);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    const token = localStorage.getItem('authToken');
    const isEditing = !!despesaToEdit;

    const despesaData = {
      valor: parseFloat(valor),
      data,
      pagador_id: parseInt(pagadorId, 10),
    };

    let endpoint = '';
    if (tipo === 'compra') {
      despesaData.nome_mercado = nomeMercado;
      despesaData.itens = itens.filter(item => item.trim() !== ''); // Filtra itens vazios
      endpoint = isEditing
        ? `http://127.0.0.1:5000/despesas/compras/${despesaToEdit.id}`
        : `http://127.0.0.1:5000/grupos/${grupoId}/despesas/compras`;
    } else { // imovel
      despesaData.endereco = endereco;
      endpoint = isEditing
        ? `http://127.0.0.1:5000/despesas/imoveis/${despesaToEdit.id}`
        : `http://127.0.0.1:5000/grupos/${grupoId}/despesas/imoveis`;
    }

    try {
      const response = await fetch(endpoint, {
        method: isEditing ? 'PUT' : 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(despesaData),
      });

      if (!response.ok) {
        throw new Error(`Falha ao ${isEditing ? 'atualizar' : 'salvar'} despesa`);
      }

      if (isEditing) {
        if (onDespesaUpdated) onDespesaUpdated();
      } else {
        if (onDespesaCreated) onDespesaCreated();
      }

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>{despesaToEdit ? 'Editar Despesa' : 'Adicionar Nova Despesa'}</h3>
      
      <div>
        <label htmlFor="tipo">Tipo:</label>
        <select id="tipo" value={tipo} onChange={(e) => setTipo(e.target.value)} disabled={!!despesaToEdit}>
          <option value="compra">Compra</option>
          <option value="imovel">Imóvel</option>
        </select>
      </div>

      <div>
        <label htmlFor="valor">Valor (R$):</label>
        <input id="valor" type="number" step="0.01" value={valor} onChange={(e) => setValor(e.target.value)} required />
      </div>
      
      <div>
        <label htmlFor="data">Data:</label>
        <input id="data" type="date" value={data} onChange={(e) => setData(e.target.value)} required />
      </div>

      <div>
        <label htmlFor="pagador">Pagador:</label>
        <select id="pagador" value={pagadorId} onChange={(e) => setPagadorId(e.target.value)} required>
          <option value="">Selecione quem pagou</option>
          {pessoas.map(p => (
            <option key={p.id} value={p.id}>{p.nome}</option>
          ))}
        </select>
      </div>

      {tipo === 'compra' && (
        <>
          <div>
            <label htmlFor="nome_mercado">Nome do Mercado (opcional):</label>
            <input id="nome_mercado" type="text" value={nomeMercado} onChange={(e) => setNomeMercado(e.target.value)} />
          </div>
          <div>
            <label>Itens da Compra:</label>
            {itens.map((item, index) => (
              <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '5px' }}>
                <input
                  type="text"
                  placeholder={`Item ${index + 1}`}
                  value={item}
                  onChange={(e) => handleItemChange(index, e.target.value)}
                />
                <button type="button" onClick={() => handleRemoveItem(index)} style={{ marginLeft: '10px' }}>
                  Remover
                </button>
              </div>
            ))}
            <button type="button" onClick={handleAddItem}>
              Adicionar Item
            </button>
          </div>
        </>
      )}

      {tipo === 'imovel' && (
        <div>
          <label htmlFor="endereco">Endereço (opcional):</label>
          <input id="endereco" type="text" value={endereco} onChange={(e) => setEndereco(e.target.value)} />
        </div>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}
      <button type="submit">Salvar Despesa</button>
    </form>
  );
}