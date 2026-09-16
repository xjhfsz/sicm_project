import React from 'react';
import ReactDOM from 'react-dom/client';
import MeuComponente from './components/MeuComponente';

const rootElement = document.getElementById('react-root');

if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(
    <React.StrictMode>
      <MeuComponente />
    </React.StrictMode>
  );
}