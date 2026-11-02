import { useEffect, useRef, useState } from "react";
import Markdown from "react-markdown";

const API_URL = import.meta.env.VITE_API_URL;

const EXAMPLES = [
  "What are you working on right now?",
  "Tell me about your deepfake detection work",
  "What's your tech stack?",
  "How can I contact you?",
];

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send(text) {
    const message = text.trim();
    if (!message || loading) return;
    const history = messages;
    setMessages([...history, { role: "user", content: message }]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, history }),
      });
      const data = await res.json();
      const reply = res.ok ? data.reply : data.error || "Something went wrong.";
      setMessages((m) => [...m, { role: "assistant", content: reply }]);
    } catch {
      setMessages((m) => [...m, { role: "assistant", content: "Couldn't reach the server. Try again." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app">
      <header>
        <h1>Hey, I'm Miracle 👋</h1>
        <p>
          <strong>ML Engineer / AI Engineer</strong> — I build deepfake detectors, production ML
          systems, and agentic AI. Ask me anything about my experience, skills, or projects.
        </p>
      </header>

      <section className="chat">
        {messages.length === 0 && (
          <div className="examples">
            {EXAMPLES.map((e) => (
              <button key={e} onClick={() => send(e)}>{e}</button>
            ))}
          </div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            {m.role === "assistant" ? (
              <Markdown components={{ a: (p) => <a {...p} target="_blank" rel="noreferrer" /> }}>{m.content}</Markdown>
            ) : m.content}
          </div>
        ))}
        {loading && <div className="msg assistant typing">Thinking…</div>}
        <div ref={bottomRef} />
      </section>

      <form onSubmit={(e) => { e.preventDefault(); send(input); }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything..."
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>Send</button>
        {messages.length > 0 && (
          <button type="button" className="secondary" onClick={() => setMessages([])}>Clear</button>
        )}
      </form>
    </main>
  );
}
