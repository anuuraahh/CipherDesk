import { useState } from "react";
import "./Terminal.css";

const API_BASE = "http://127.0.0.1:8000";

const stages = [
  { key: "communicator", label: "communicator" },
  { key: "news", label: "news analyst" },
  { key: "price", label: "price analyst" },
  { key: "report", label: "report writer" },
];

function Terminal({ onReportReady }) {
  const [query, setQuery] = useState("");
  const [running, setRunning] = useState(false);
  const [currentStage, setCurrentStage] = useState(-1);
  const [log, setLog] = useState("");
  const [error, setError] = useState("");

  async function runPipeline() {
    if (!query.trim() || running) return;

    setRunning(true);
    setError("");
    setCurrentStage(0);
    onReportReady(null);

    try {
      setLog("parsing your request...");
      const parseRes = await fetch(`${API_BASE}/parse`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
      if (!parseRes.ok) throw new Error("communicator agent failed");
      const { coin, days } = await parseRes.json();

      setCurrentStage(1);
      setLog(`fetching news for ${coin}...`);
      const newsRes = await fetch(`${API_BASE}/news`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coin, days }),
      });
      if (!newsRes.ok) throw new Error("news analyst agent failed");
      const newsResult = await newsRes.json();

      setCurrentStage(2);
      setLog(`fetching price data for ${coin}...`);
      const priceRes = await fetch(`${API_BASE}/price`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ coin, days }),
      });
      if (!priceRes.ok) throw new Error("price analyst agent failed");
      const priceResult = await priceRes.json();

      setCurrentStage(3);
      setLog("writing final report...");
      const reportRes = await fetch(`${API_BASE}/report`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          coin,
          price_analysis: priceResult,
          news_analysis: newsResult,
        }),
      });
      if (!reportRes.ok) throw new Error("report writer agent failed");
      const { report } = await reportRes.json();

      setCurrentStage(4);
      setLog("done");
      onReportReady({
        coin,
        report,
        priceStats: priceResult.current,
        historical: priceResult.historical,
      });
    } catch (err) {
      setError(err.message);
      setLog("");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="terminal">
      <div className="terminal-prompt-row">
        <span className="prompt-arrow">&gt;</span>
        <input
          className="prompt-input"
          type="text"
          placeholder="how is bitcoin doing this month?"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && runPipeline()}
          disabled={running}
        />
        <button
          className="run-button"
          onClick={runPipeline}
          disabled={running || !query.trim()}
        >
          {running ? "running..." : "run"}
        </button>
      </div>

      <div className="pipeline-row">
        <div className="pipeline-track">
          <div
            className="pipeline-track-fill"
            style={{
              width: `${(Math.max(currentStage, 0) / (stages.length - 1)) * 100}%`,
            }}
          />
        </div>
        <div className="pipeline-nodes">
          {stages.map((stage, i) => (
            <div key={stage.key} className="pipeline-node-col">
              <div
                className={
                  "pipeline-node" +
                  (currentStage > i || currentStage === 4 ? " node-done" : "") +
                  (currentStage === i ? " node-active" : "")
                }
              />
              <span className="pipeline-label">{stage.label}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="terminal-log">
        {error ? <span className="log-error">error: {error}</span> : log}
      </div>
    </div>
  );
}

export default Terminal;