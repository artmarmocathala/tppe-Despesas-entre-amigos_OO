import React, { useEffect, useState } from 'react';
import StatCard from '../components/StatCard';

export function Home() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      setError(null);
      const token = localStorage.getItem('authToken');
      try {
        const resp = await fetch('http://127.0.0.1:5000/stats', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!resp.ok) throw new Error('Erro ao buscar estatísticas.');
        const data = await resp.json();
        setStats(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  if (loading) return <p>Carregando estatísticas...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;
  if (!stats) return <p>Não foi possível carregar as estatísticas.</p>;

  // Determina se a visão é de admin com base nos dados recebidos
  const isAdminView = stats.total_usuarios !== undefined;

  return (
    // Container principal da página
    <div className="container mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">Dashboard</h1>
      <p className="text-gray-600 mb-8">
        {isAdminView ? 'Visão geral do sistema.' : 'Este é o resumo das suas atividades.'}
      </p>

      {/* Grelha responsiva para os cards */}
      {/* Por padrão tem 1 coluna, em ecrãs médios (md) 2, e em ecrãs grandes (lg) 4. */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Renderização condicional dos cards */}
        {isAdminView ? (
          <>
            <StatCard title="Total de Usuários" value={stats.total_usuarios} />
            <StatCard title="Total de Grupos" value={stats.total_grupos} />
            <StatCard title="Total de Pessoas" value={stats.total_pessoas} />
            <StatCard title="Total de Despesas" value={stats.total_despesas} />
          </>
        ) : (
          <>
            <StatCard title="Meus Grupos" value={stats.meus_grupos} />
            <StatCard title="Pessoas nos meus Grupos" value={stats.minhas_pessoas} />
            <StatCard title="Despesas nos meus Grupos" value={stats.minhas_despesas} />
          </>
        )}
      </div>
    </div>
  );
}