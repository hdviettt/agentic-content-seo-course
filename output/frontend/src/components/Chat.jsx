import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { streamTeamRun } from "../api";
import "./Chat.css";

function AIOResultCard({ json }) {
  let data;
  try {
    data = JSON.parse(json);
  } catch {
    return <pre>{json}</pre>;
  }

  if (!data.has_aio) {
    return (
      <div className="aio-card">
        <div className="aio-card-header">
          <span className="aio-card-label">AI Overview</span>
          <span className="aio-card-keyword">{data.keyword}</span>
        </div>
        <p className="aio-card-empty">No AI Overview exists for this keyword.</p>
      </div>
    );
  }

  return (
    <div className="aio-card">
      <div className="aio-card-header">
        <span className="aio-card-label">AI Overview</span>
        <span className="aio-card-keyword">{data.keyword}</span>
      </div>
      <div className="aio-card-content">{data.content}</div>
      {data.references?.length > 0 && (
        <div className="aio-card-refs">
          <span className="aio-card-refs-label">Sources</span>
          {data.references.map((ref, i) => (
            <a
              key={i}
              className="aio-card-ref"
              href={ref.url}
              target="_blank"
              rel="noopener noreferrer"
            >
              <span className="aio-card-ref-source">{ref.source}</span>
              <span className="aio-card-ref-title">{ref.title}</span>
            </a>
          ))}
        </div>
      )}
    </div>
  );
}

const markdownComponents = {
  pre({ children }) {
    // Check if the child is a code element with aio-result language
    const child = children?.props || {};
    const className = child.className || "";
    if (className.includes("language-aio-result")) {
      const text = String(child.children || "").trim();
      return <AIOResultCard json={text} />;
    }
    return <pre>{children}</pre>;
  },
};

export default function Chat({ onRunComplete, onSelectArticle }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [articleCardsMap, setArticleCardsMap] = useState({});
  const bottomRef = useRef(null);
  const streamingRef = useRef(false);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send() {
    const prompt = input.trim();
    if (!prompt || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: prompt }]);
    setLoading(true);
    streamingRef.current = false;

    await streamTeamRun(prompt, {
      onChunk(text) {
        if (!streamingRef.current) {
          streamingRef.current = true;
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: text },
          ]);
        } else {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            updated[updated.length - 1] = {
              ...last,
              content: last.content + text,
            };
            return updated;
          });
        }
      },
      async onDone(fullText) {
        if (streamingRef.current) {
          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = {
              ...updated[updated.length - 1],
              content: fullText,
            };
            return updated;
          });
        } else {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: fullText || "(No response)" },
          ]);
        }

        setLoading(false);

        if (onRunComplete) {
          const created = await onRunComplete();
          if (created && created.length > 0) {
            setMessages((prev) => {
              const msgIndex = prev.length - 1;
              setArticleCardsMap((map) => ({ ...map, [msgIndex]: created }));
              return prev;
            });
          }
        }
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
        <div className="chat-messages-inner">
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
                  <ReactMarkdown components={markdownComponents}>
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>
              {msg.role === "assistant" &&
                articleCardsMap[i]?.length > 0 && (
                  <div className="chat-article-cards">
                    {articleCardsMap[i].map((a) => (
                      <button
                        key={a.id}
                        className="chat-article-card"
                        onClick={() => onSelectArticle?.(a)}
                      >
                        <span className="chat-article-card-topic">
                          {a.topic}
                        </span>
                        <span className="chat-article-card-meta">
                          {a.word_count ? `${a.word_count} words` : "View"}
                        </span>
                      </button>
                    ))}
                  </div>
                )}
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
      </div>
      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <textarea
            className="chat-input"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything..."
            rows={1}
            disabled={loading}
          />
          <button
            className="chat-send"
            onClick={send}
            disabled={!input.trim() || loading}
          >
            &#8593;
          </button>
        </div>
      </div>
    </div>
  );
}
