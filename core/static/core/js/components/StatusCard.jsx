import React from 'react';

export default function StatusCard({ titulo, valor, cor }) {
  return (
    <div className="col-md-4 mb-3">
      <div className={`card border-start border-4 border-${cor} shadow-sm h-100`}>
        <div className="card-body">
          <h6 className="text-uppercase text-muted fw-bold small mb-1">{titulo}</h6>
          <h3 className="mb-0 fw-bold">{valor}</h3>
        </div>
      </div>
    </div>
  );
}