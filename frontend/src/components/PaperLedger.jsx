import { useEffect, useState } from "react";
import CountUp from "./CountUp";
import "./PaperLedger.css";

function PaperLedger({ data }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (data) {
      const timer = setTimeout(() => setVisible(true), 50);
      return () => clearTimeout(timer);
    } else {
      setVisible(false);
    }
  }, [data]);

  if (!data) return null;

  const { priceStats, historical } = data;
  const changeUp = priceStats?.usd_24h_change >= 0;

  const formattedReport = data.report
    .split("\n")
    .map((line, i) => {
      if (line.startsWith("# ")) {
        return <h1 key={i} className="ledger-h1">{line.slice(2)}</h1>;
      }
      if (line.startsWith("## ")) {
        return <h2 key={i} className="ledger-h2">{line.slice(3)}</h2>;
      }
      if (line.trim() === "") {
        return null;
      }
      return <p key={i} className="ledger-p">{line}</p>;
    })
    .filter(Boolean);

  return (
    <div className={"ledger-wrap" + (visible ? " ledger-visible" : "")}>
      <div className="ledger-stamp">verified by signal terminal</div>
      <div className="ledger-content">
        {priceStats && (
          <div className="stat-strip">
            <div className="stat-cell">
              <span className="stat-label">price</span>
              <span className="stat-value">
                <CountUp value={priceStats.usd} prefix="$" decimals={2} />
              </span>
            </div>
            <div className="stat-cell">
              <span className="stat-label">24h change</span>
              <span className={"stat-value " + (changeUp ? "stat-up" : "stat-down")}>
                {changeUp ? "+" : ""}
                <CountUp value={priceStats.usd_24h_change} decimals={2} />%
              </span>
            </div>
            {historical && (
              <>
                <div className="stat-cell">
                  <span className="stat-label">period high</span>
                  <span className="stat-value">
                    <CountUp value={historical.period_high} prefix="$" decimals={2} />
                  </span>
                </div>
                <div className="stat-cell">
                  <span className="stat-label">period low</span>
                  <span className="stat-value">
                    <CountUp value={historical.period_low} prefix="$" decimals={2} />
                  </span>
                </div>
              </>
            )}
          </div>
        )}
        {formattedReport}
      </div>
    </div>
  );
}

export default PaperLedger;