import ChatWidget from './components/ChatWidget';
import Example from './components/Example';
import './App.css'

function App() {
  return (
    <div>
      <Example/>
      <ChatWidget apiUrl="http://localhost:8000/api/chat" />
    </div>
  );
}

export default App;