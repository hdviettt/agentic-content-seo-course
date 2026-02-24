const BASE = "";

export async function listArticles() {
  const res = await fetch(`${BASE}/api/articles`);
  return res.json();
}

export async function getArticle(id) {
  const res = await fetch(`${BASE}/api/articles/${id}`);
  return res.json();
}

export async function deleteArticle(id) {
  const res = await fetch(`${BASE}/api/articles/${id}`, { method: "DELETE" });
  return res.json();
}

/**
 * Send a message to the team via our custom /api/chat endpoint.
 * Calls onContent(text) with the response, then onDone().
 */
export async function runTeam(prompt, { onContent, onDone, onError }) {
  try {
    const res = await fetch(`${BASE}/api/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: prompt }),
    });

    if (!res.ok) {
      const err = await res.text();
      onError?.(err);
      return;
    }

    const data = await res.json();
    if (data.content) {
      onContent?.(data.content);
    }
    onDone?.();
  } catch (err) {
    onError?.(err.message);
  }
}
