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
 * Stream a team run via SSE. Uses our custom /api/chat/stream endpoint
 * which wraps team.arun() in SSE events (TeamMode.tasks doesn't support
 * native AgentOS streaming).
 *
 * Callbacks:
 *   onChunk(text)  — called with each content delta (append to message)
 *   onDone(text)   — called with full final text when run completes
 *   onError(msg)   — called on error
 */
export async function streamTeamRun(prompt, { onChunk, onDone, onError }) {
  try {
    const res = await fetch(`${BASE}/api/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: prompt }),
    });

    if (!res.ok) {
      const err = await res.text();
      onError?.(err);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let fullText = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      // Parse SSE frames: split on double newline
      const frames = buffer.split("\n\n");
      // Last element may be incomplete — keep it in buffer
      buffer = frames.pop() || "";

      for (const frame of frames) {
        if (!frame.trim()) continue;

        const lines = frame.split("\n");
        let eventName = "";
        let dataStr = "";

        for (const line of lines) {
          if (line.startsWith("event: ")) {
            eventName = line.slice(7).trim();
          } else if (line.startsWith("data: ")) {
            dataStr = line.slice(6);
          }
        }

        if (!eventName || !dataStr) continue;

        try {
          const data = JSON.parse(dataStr);

          if (eventName === "TeamRunContent" && data.content) {
            fullText += data.content;
            onChunk?.(data.content);
          } else if (eventName === "TeamRunCompleted") {
            // Final event — use its content as the authoritative full text
            if (data.content) {
              fullText = data.content;
            }
            onDone?.(fullText);
            return;
          } else if (eventName === "TeamRunError") {
            onError?.(data.content || "Unknown error");
            return;
          }
        } catch {
          // Skip malformed JSON
        }
      }
    }

    // Stream ended without TeamRunCompleted — still call onDone
    onDone?.(fullText);
  } catch (err) {
    onError?.(err.message);
  }
}
