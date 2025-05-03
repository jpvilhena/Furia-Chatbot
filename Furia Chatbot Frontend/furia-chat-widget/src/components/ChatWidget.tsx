import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './ChatWidget.css';

interface ChatWidgetProps {
  apiUrl?: string;
}

interface Message {
  from: 'user' | 'bot';
  text: string;
}

export default function ChatWidget({
  apiUrl = 'http://localhost:8000/api/chat',
}: ChatWidgetProps) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { from: 'bot', text: 'Olá! Pergunte algo sobre a FURIA.' },
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg: Message = { from: 'user', text: input };
    setMessages((m) => [...m, userMsg]);
    setInput('');

    try {
      const resp = await axios.post<{ reply: string }>(apiUrl, {
        session_id: 'widget',
        message: input,
      });
      setMessages((m) => [...m, { from: 'bot', text: resp.data.reply }]);
    } catch (err) {
      console.error(err);
      setMessages((m) => [
        ...m,
        { from: 'bot', text: 'Erro ao conectar ao servidor.' },
      ]);
    }
  };

  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className={`chat-widget ${open ? 'open' : ''}`}>
      <div className="chat-header" onClick={() => setOpen((o) => !o)}>
        {open ? 'Fechar Chat' : 'FURIA Chat'}
      </div>
      {open && (
        <div className="chat-body">
          <div className="messages">
            {messages.map((m, i) => (
              <div key={i} className={`message ${m.from}`}>
                {m.text}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="chat-input">
            <input
              type="text"
              placeholder="Digite sua mensagem..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKeyDown}
            />
            <button onClick={sendMessage}>Enviar</button>
          </div>
        </div>
      )}
    </div>
  );
}
