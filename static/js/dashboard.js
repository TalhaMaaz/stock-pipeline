let priceChart = null;
let pctChart = null;
let activeTicker = null;

// --- Boot ---
async function init() {
  await loadCards();
  const tickers = await fetchTickers();
  renderButtons(tickers);
  loadTicker(tickers[0]);
}

// --- Fetch helpers ---
async function fetchTickers() {
  const res = await fetch("/api/tickers");
  return res.json();
}

async function fetchStock(ticker) {
  const res = await fetch(`/api/stock/${ticker}`);
  return res.json();
}

async function fetchLatest() {
  const res = await fetch("/api/latest");
  return res.json();
}

// --- Ticker cards ---
async function loadCards() {
  const latest = await fetchLatest();
  const container = document.getElementById("ticker-cards");
  container.innerHTML = latest.map(d => {
    const change = d.pct_change != null ? d.pct_change.toFixed(2) : "N/A";
    const cls = d.pct_change >= 0 ? "positive" : "negative";
    const arrow = d.pct_change >= 0 ? "▲" : "▼";
    return `
      <div class="card">
        <div class="ticker-name">${d.ticker}</div>
        <div class="price">$${d.close.toFixed(2)}</div>
        <div class="change ${cls}">${arrow} ${change}%</div>
      </div>`;
  }).join("");
}

// --- Ticker buttons ---
function renderButtons(tickers) {
  const container = document.getElementById("ticker-buttons");
  container.innerHTML = tickers.map(t =>
    `<button onclick="loadTicker('${t}')" id="btn-${t}">${t}</button>`
  ).join("");
}

// --- Load ticker charts ---
async function loadTicker(ticker) {
  activeTicker = ticker;

  // Update active button
  document.querySelectorAll("#ticker-buttons button").forEach(b => b.classList.remove("active"));
  const btn = document.getElementById(`btn-${ticker}`);
  if (btn) btn.classList.add("active");

  const data = await fetchStock(ticker);
  const labels = data.map(d => d.date);
  const close  = data.map(d => d.close);
  const sma20  = data.map(d => d.sma_20);
  const sma50  = data.map(d => d.sma_50);
  const pct    = data.map(d => d.pct_change);

  document.getElementById("price-title").textContent = `${ticker} — Price & Moving Averages`;
  document.getElementById("pct-title").textContent   = `${ticker} — Daily % Change`;

  renderPriceChart(labels, close, sma20, sma50);
  renderPctChart(labels, pct);
}

// --- Price chart ---
function renderPriceChart(labels, close, sma20, sma50) {
  if (priceChart) priceChart.destroy();
  const ctx = document.getElementById("priceChart").getContext("2d");
  priceChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Close",  data: close, borderColor: "#ffffff", borderWidth: 1.5, pointRadius: 0, tension: 0.3 },
        { label: "SMA 20", data: sma20, borderColor: "#00d4aa", borderWidth: 1.5, pointRadius: 0, tension: 0.3 },
        { label: "SMA 50", data: sma50, borderColor: "#ff9f40", borderWidth: 1.5, pointRadius: 0, tension: 0.3 },
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: "#aaa" } } },
      scales: {
        x: { ticks: { color: "#666", maxTicksLimit: 10 }, grid: { color: "#1e2130" } },
        y: { ticks: { color: "#666" }, grid: { color: "#1e2130" } }
      }
    }
  });
}

// --- % Change chart ---
function renderPctChart(labels, pct) {
  if (pctChart) pctChart.destroy();
  const ctx = document.getElementById("pctChart").getContext("2d");
  pctChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "% Change",
        data: pct,
        backgroundColor: pct.map(v => v >= 0 ? "rgba(0,212,170,0.6)" : "rgba(255,77,77,0.6)"),
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { labels: { color: "#aaa" } } },
      scales: {
        x: { ticks: { color: "#666", maxTicksLimit: 10 }, grid: { color: "#1e2130" } },
        y: { ticks: { color: "#666" }, grid: { color: "#1e2130" } }
      }
    }
  });
}

init();
