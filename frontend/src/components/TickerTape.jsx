import "./TickerTape.css";

const tickerData = [
  { symbol: "BTC", price: "64,270", change: "+2.69%", up: true },
  { symbol: "ETH", price: "1,792.58", change: "+2.99%", up: true },
  { symbol: "SOL", price: "142.30", change: "-1.24%", up: false },
  { symbol: "DOGE", price: "0.1120", change: "+5.02%", up: true },
  { symbol: "XRP", price: "0.5890", change: "-0.87%", up: false },
  { symbol: "ADA", price: "0.3910", change: "+1.15%", up: true },
];

function TickerTape() {
  const doubled = [...tickerData, ...tickerData];

  return (
    <div className="ticker-wrap">
      <div className="ticker-track">
        {doubled.map((item, i) => (
          <span key={i} className="ticker-item">
            <span className="ticker-symbol">{item.symbol}</span>
            <span className="ticker-price">${item.price}</span>
            <span className={item.up ? "ticker-up" : "ticker-down"}>
              {item.change}
            </span>
          </span>
        ))}
      </div>
    </div>
  );
}

export default TickerTape;