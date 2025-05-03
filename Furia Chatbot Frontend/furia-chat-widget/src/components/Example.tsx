import React from 'react';

const Example: React.FC = () => {
  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Bem-vindo ao FURIA Chatbot</h1>
        <p style={styles.subtitle}>Tire suas dúvidas sobre o time de CS da FURIA</p>
      </header>

      <main style={styles.main}>
        <img
          src="https://upload.wikimedia.org/wikipedia/pt/f/f9/Furia_Esports_logo.png"
          alt="FURIA Logo"
          style={styles.logo}
        />

        <div style={styles.chatContainer}>
        </div>
      </main>

      <footer style={styles.footer}>
        <p>© {new Date().getFullYear()} FURIA Chatbot - Projeto de exemplo</p>
      </footer>
    </div>
  );
};

const styles: { [key: string]: React.CSSProperties } = {
  container: {
    fontFamily: 'Arial, sans-serif',
    textAlign: 'center',
    backgroundColor: '#0f0f0f',
    color: '#ffffff',
    minHeight: '100vh',
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    padding: '2rem 1rem',
    backgroundColor: '#111',
  },
  title: {
    fontSize: '2.5rem',
    margin: 0,
  },
  subtitle: {
    fontSize: '1.2rem',
    color: '#bbb',
  },
  main: {
    flex: 1,
    padding: '2rem',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  logo: {
    width: '200px',
    marginBottom: '2rem',
  },
  chatContainer: {
    width: '100%',
    maxWidth: '400px',
    border: '1px solid #333',
    borderRadius: '10px',
    padding: '1rem',
    backgroundColor: '#1a1a1a',
  },
  footer: {
    padding: '1rem',
    backgroundColor: '#111',
    fontSize: '0.9rem',
    color: '#777',
  },
};

export default Example;
