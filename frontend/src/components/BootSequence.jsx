import { useState, useEffect } from "react";
import "./BootSequence.css";

const bootLines = [
  "SIGNAL TERMINAL v1.0 — INITIALIZING",
  "CONNECTING TO NEWS FEED... OK",
  "CONNECTING TO PRICE FEED... OK",
  "CONNECTING TO LLM CORE... OK",
  "SYSTEM READY",
];

function BootSequence({ onComplete }) {
  const [lineIndex, setLineIndex] = useState(0);
  const [charIndex, setCharIndex] = useState(0);
  const [displayedLines, setDisplayedLines] = useState([]);

  useEffect(() => {
    if (lineIndex >= bootLines.length) {
      const timer = setTimeout(onComplete, 500);
      return () => clearTimeout(timer);
    }

    const currentLine = bootLines[lineIndex];

    if (charIndex < currentLine.length) {
      const timer = setTimeout(() => setCharIndex(charIndex + 1), 20);
      return () => clearTimeout(timer);
    } else {
      const timer = setTimeout(() => {
        setDisplayedLines((prev) => [...prev, currentLine]);
        setLineIndex(lineIndex + 1);
        setCharIndex(0);
      }, 200);
      return () => clearTimeout(timer);
    }
  }, [lineIndex, charIndex, onComplete]);

  const currentTypingLine =
    lineIndex < bootLines.length
      ? bootLines[lineIndex].slice(0, charIndex)
      : "";

  return (
    <div className="boot-screen">
      <div className="scanlines"></div>
      <div className="boot-text">
        {displayedLines.map((line, i) => (
          <div key={i} className="boot-line">{line}</div>
        ))}
        {lineIndex < bootLines.length && (
          <div className="boot-line">
            {currentTypingLine}
            <span className="boot-cursor">_</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default BootSequence;