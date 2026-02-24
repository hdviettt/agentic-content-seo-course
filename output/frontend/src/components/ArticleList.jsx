import { useState, useEffect } from "react";
import { listArticles, deleteArticle } from "../api";
import "./ArticleList.css";

export default function ArticleList({ refreshKey, onSelect, selectedId }) {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    listArticles().then(setArticles).catch(() => {});
  }, [refreshKey]);

  // Poll every 10s for new articles
  useEffect(() => {
    const id = setInterval(() => {
      listArticles().then(setArticles).catch(() => {});
    }, 10000);
    return () => clearInterval(id);
  }, []);

  async function handleDelete(e, articleId) {
    e.stopPropagation();
    if (!confirm("Delete this article?")) return;
    await deleteArticle(articleId);
    setArticles((prev) => prev.filter((a) => a.id !== articleId));
  }

  if (articles.length === 0) {
    return <div className="article-list-empty">No articles yet</div>;
  }

  return (
    <div className="article-list">
      <div className="article-list-header">Articles ({articles.length})</div>
      {articles.map((a) => (
        <div
          key={a.id}
          className={`article-card ${selectedId === a.id ? "article-card--selected" : ""}`}
          onClick={() => onSelect(a)}
        >
          <div className="article-card-topic">{a.topic}</div>
          <div className="article-card-meta">
            {a.word_count ? `${a.word_count} words` : ""}
            {a.status && <span className={`badge badge--${a.status}`}>{a.status}</span>}
          </div>
          <button
            className="article-card-delete"
            onClick={(e) => handleDelete(e, a.id)}
            title="Delete"
          >
            &times;
          </button>
        </div>
      ))}
    </div>
  );
}
