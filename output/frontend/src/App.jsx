import { useState } from "react";
import Chat from "./components/Chat";
import ArticleList from "./components/ArticleList";
import ArticleView from "./components/ArticleView";
import "./App.css";

export default function App() {
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="app">
      <aside className="sidebar">
        <h1 className="logo">SEO Workspace</h1>
        <ArticleList
          refreshKey={refreshKey}
          onSelect={setSelectedArticle}
          selectedId={selectedArticle?.id}
        />
      </aside>
      <main className="main">
        {selectedArticle ? (
          <ArticleView
            articleId={selectedArticle.id}
            onBack={() => setSelectedArticle(null)}
          />
        ) : (
          <Chat onArticleCreated={() => setRefreshKey((k) => k + 1)} />
        )}
      </main>
    </div>
  );
}
