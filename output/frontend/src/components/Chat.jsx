import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { runTeam } from "../api";
import "./Chat.css";

export default function Chat({ onArticleCreated }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send() {
    const prompt = input.trim();
    if (!prompt || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: prompt }]);
    setLoading(true);

    await runTeam(prompt, {
      onContent(text) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: text },
        ]);
      },
      onDone() {
        setLoading(false);
        onArticleCreated?.();
      },
      onError(err) {
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: `Error: ${err}` },
        ]);
        setLoading(false);
      },
    });
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <div className="chat">
      <div className="chat-messages">
        {messages.length === 0 && !loading && (
          <div className="chat-empty">
            <h2>SEO Workspace</h2>
            <p>Ask me to write articles, find images, or analyze AI Overviews.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div key={i} className={`chat-msg chat-msg--${msg.role}`}>
            <div className="chat-msg-label">
              {msg.role === "user" ? "You" : "Team"}
            </div>
            <div className="chat-msg-content">
              {msg.role === "assistant" ? (
                <ReactMarkdown>{msg.content}</ReactMarkdown>
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-thinking">
            <div className="chat-thinking-dots">
              <span />
              <span />
              <span />
            </div>
            Team is working...
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="chat-input-area">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Write an article about on-page SEO..."
          rows={2}
          disabled={loading}
        />
        <button
          className="chat-send"
          onClick={send}
          disabled={!input.trim() || loading}
        >
          {loading ? "Working..." : "Send"}
        </button>
      </div>
    </div>
  );
}
