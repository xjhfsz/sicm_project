import React, { useState, useEffect } from 'react';
import StatusCard from './StatusCard';

export default function MeuComponente() {
  const [nome, setNome] = useState('');
  const [visitantes, setVisitantes] = useState([]);
  const [mensagem, setMensagem] = useState('');

  // Carrega autorizações do banco de dados
  const carregarVisitantes = () => {
    fetch('/api/visitantes/')
      .then((res) => res.json())
      .then((data) => setVisitantes(data))
      .catch((err) => console.error('Erro ao carregar autorizações:', err));
  };

  useEffect(() => {
    carregarVisitantes();
  }, []);

  // Cadastra no banco via POST
  const handleCadastrar = async (e) => {
    e.preventDefault();
    if (!nome.trim()) return;

    try {
      const response = await fetch('/api/visitantes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nome }),
      });

      if (response.ok) {
        setNome('');
        setMensagem('Autorização salva com sucesso no banco!');
        carregarVisitantes();
        setTimeout(() => setMensagem(''), 4000);
      } else {
        const errData = await response.json();
        alert(errData.erro || 'Erro ao cadastrar.');
      }
    } catch (error) {
      console.error('Erro de conexão:', error);
    }
  };

  // Revoga no banco via DELETE
  const handleRevogar = async (id) => {
    try {
      const response = await fetch(`/api/visitantes/${id}/revogar/`, {
        method: 'DELETE',
      });

      if (response.ok) {
        setVisitantes(visitantes.filter((item) => item.id !== id));
      }
    } catch (error) {
      console.error('Erro ao revogar:', error);
    }
  };

  return (
    <div className="text-start mt-4">
      <div className="row">
        <StatusCard titulo="Autorizados Hoje" valor={visitantes.length} cor="success" />
        <StatusCard titulo="Aguardando Validação" valor="0" cor="warning" />
        <StatusCard titulo="Total de Registros" valor={visitantes.length} cor="primary" />
      </div>

      <div className="card shadow-sm border-0 mb-4 bg-light">
        <div className="card-body p-4">
          <h5 className="card-title fw-bold text-dark mb-3">Nova Autorização Rápida</h5>
          <form onSubmit={handleCadastrar} className="row g-3">
            <div className="col-md-9">
              <input
                type="text"
                className="form-control"
                placeholder="Nome completo do visitante..."
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                required
              />
            </div>
            <div className="col-md-3">
              <button type="submit" className="btn btn-primary w-100 fw-bold">
                Autorizar Entrada
              </button>
            </div>
          </form>

          {mensagem && (
            <div className="alert alert-success mt-3 mb-0 py-2">{mensagem}</div>
          )}
        </div>
      </div>

      <div className="card shadow-sm border-0">
        <div className="card-header bg-white py-3">
          <h6 className="mb-0 fw-bold text-secondary">Autorizações Cadastradas no Banco</h6>
        </div>
        <div className="table-responsive">
          <table className="table table-hover align-middle mb-0">
            <thead className="table-light">
              <tr>
                <th>Nome do Visitante</th>
                <th>Data da Visita</th>
                <th>Unidade</th>
                <th className="text-end">Ação</th>
              </tr>
            </thead>
            <tbody>
              {visitantes.length === 0 ? (
                <tr>
                  <td colSpan="4" className="text-center text-muted py-3">
                    Nenhuma autorização encontrada no banco de dados.
                  </td>
                </tr>
              ) : (
                visitantes.map((v) => (
                  <tr key={v.id}>
                    <td className="fw-semibold">{v.nome}</td>
                    <td><span className="badge bg-light text-dark">{v.data_visita}</span></td>
                    <td className="text-muted">{v.unidade}</td>
                    <td className="text-end">
                      <button
                        onClick={() => handleRevogar(v.id)}
                        className="btn btn-sm btn-outline-danger"
                      >
                        Revogar
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}