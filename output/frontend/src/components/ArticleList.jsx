import { useState, useEffect } from "react";
import { listArticles, deleteArticle } from "../api";
import "./ArticleList.css";

export default function ArticleList({
  refreshKey,
  onSelect,
  selectedId,
  newArticleIds,
}) {
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

  // Sort by created_at descending (newest first)
  const sorted = [...articles].sort((a, b) => {
    if (!a.created_at || !b.created_at) return 0;
    return b.created_at.localeCompare(a.created_at);
  });

  if (sorted.length === 0) {
    return <div className="article-list-empty">No articles yet</div>;
  }

  return (
    <div className="article-list">
      <div className="article-list-header">Articles ({sorted.length})</div>
      {sorted.map((a) => {
        const isNew = newArticleIds?.has(a.id);
        return (
          <div
            key={a.id}
            className={`article-card${selectedId === a.id ? " article-card--selected" : ""}${isNew ? " article-card--new" : ""}`}
            onClick={() => onSelect(a)}
          >
            <div className="article-card-topic">
              {a.topic}
              {isNew && <span className="badge badge--new">NEW</span>}
            </div>
            <div className="article-card-meta">
              {a.word_count ? `${a.word_count} words` : ""}
              {a.status && (
                <span className={`badge badge--${a.status}`}>{a.status}</span>
              )}
            </div>
            <button
              className="article-card-delete"
              onClick={(e) => handleDelete(e, a.id)}
              title="Delete"
            >
              &times;
            </button>
          </div>
        );
      })}
    </div>
  );
}
