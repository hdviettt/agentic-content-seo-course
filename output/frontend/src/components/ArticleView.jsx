import { useState, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { getArticle } from "../api";
import "./ArticleView.css";

export default function ArticleView({ articleId, onBack }) {
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getArticle(articleId)
      .then(setArticle)
      .finally(() => setLoading(false));
  }, [articleId]);

  if (loading) {
    return <div className="article-view-loading">Loading...</div>;
  }

  if (!article || article.error) {
    return (
      <div className="article-view-error">
        <p>{article?.error || "Article not found"}</p>
        <button onClick={onBack}>Back to chat</button>
      </div>
    );
  }

  const keywords = article.target_keywords
    ? JSON.parse(article.target_keywords)
    : [];

  return (
    <div className="article-view">
      <div className="article-view-header">
        <button className="article-view-back" onClick={onBack}>
          &larr; Back to chat
        </button>
        <div className="article-view-meta">
          <h1>{article.topic}</h1>
          <div className="article-view-info">
            {article.word_count && <span>{article.word_count} words</span>}
            {article.status && (
              <span className={`badge badge--${article.status}`}>
                {article.status}
              </span>
            )}
            {article.created_at && (
              <span>
                {new Date(article.created_at).toLocaleDateString()}
              </span>
            )}
          </div>
          {keywords.length > 0 && (
            <div className="article-view-keywords">
              {keywords.map((kw) => (
                <span key={kw} className="keyword-tag">
                  {kw}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
      <div className="article-view-content">
        <ReactMarkdown>{article.article_markdown || ""}</ReactMarkdown>
      </div>
    </div>
  );
}
