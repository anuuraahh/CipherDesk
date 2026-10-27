import { useState } from "react";
import "./App.css";
import TickerTape from "./components/TickerTape";
import BootSequence from "./components/BootSequence";
import Terminal from "./components/Terminal";
import PaperLedger from "./components/PaperLedger";

function App() {
  const [booted, setBooted] = useState(false);
  const [reportData, setReportData] = useState(null);

  return (
    <div className="app">
      {!booted && <BootSequence onComplete={() => setBooted(true)} />}
      <TickerTape />
      <Terminal onReportReady={setReportData} />
      <PaperLedger data={reportData} />
    </div>
  );
}

export default App;