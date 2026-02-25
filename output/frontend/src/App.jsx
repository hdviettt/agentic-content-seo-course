import { useState, useEffect, useCallback, useRef } from "react";
import { listArticles } from "./api";
import Chat from "./components/Chat";
import ArticleList from "./components/ArticleList";
import ArticleView from "./components/ArticleView";
import Toast from "./components/Toast";
import "./App.css";

export default function App() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [newArticleIds, setNewArticleIds] = useState(new Set());
  const [toast, setToast] = useState(null);
  const [latestNewArticles, setLatestNewArticles] = useState([]);
  const knownIdsRef = useRef(new Set());

  // Populate known article IDs on mount
  useEffect(() => {
    listArticles()
      .then((articles) => {
        knownIdsRef.current = new Set(articles.map((a) => a.id));
      })
      .catch(() => {});
  }, []);

  // Called when a team run completes — diff articles to find new ones
  const handleRunComplete = useCallback(async () => {
    try {
      const articles = await listArticles();
      const currentIds = new Set(articles.map((a) => a.id));
      const created = articles.filter((a) => !knownIdsRef.current.has(a.id));

      if (created.length > 0) {
        setNewArticleIds((prev) => {
          const next = new Set(prev);
          created.forEach((a) => next.add(a.id));
          return next;
        });
        setLatestNewArticles(created);
        const noun = created.length === 1 ? "article" : "articles";
        setToast(`${created.length} ${noun} created`);
      }

      knownIdsRef.current = currentIds;
      setRefreshKey((k) => k + 1);
    } catch {
      setRefreshKey((k) => k + 1);
    }
  }, []);

  const handleSelect = useCallback((article) => {
    setSelectedArticle(article);
  }, []);

  return (
    <div className="app">
      <aside className="sidebar">
        <h1 className="logo">SEO Workspace</h1>
        <ArticleList
          refreshKey={refreshKey}
          onSelect={handleSelect}
          selectedId={selectedArticle?.id}
          newArticleIds={newArticleIds}
        />
      </aside>
      <main className="main">
        <Chat
          onRunComplete={handleRunComplete}
          newArticles={latestNewArticles}
          onSelectArticle={handleSelect}
        />
      </main>
      {selectedArticle && (
        <aside className="article-panel">
          <ArticleView
            articleId={selectedArticle.id}
            onBack={() => setSelectedArticle(null)}
          />
        </aside>
      )}
      <Toast message={toast} onClose={() => setToast(null)} />
    </div>
  );
}
