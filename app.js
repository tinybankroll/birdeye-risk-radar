(function () {
  "use strict";

  const data = window.RADAR_DEMO_DATA || { summary: {}, assessments: [] };
  const summary = data.summary || {};
  const assessments = Array.isArray(data.assessments) ? data.assessments : [];
  const state = {
    classification: "all",
    source: "all",
    warning: "all",
    search: "",
    sort: "volume",
    selectedAddress: null,
  };

  const els = {
    runLine: document.getElementById("runLine"),
    modeLabel: document.getElementById("modeLabel"),
    summaryCards: document.getElementById("summaryCards"),
    classificationFilters: document.getElementById("classificationFilters"),
    sourceFilters: document.getElementById("sourceFilters"),
    warningFilter: document.getElementById("warningFilter"),
    searchInput: document.getElementById("searchInput"),
    sortSelect: document.getElementById("sortSelect"),
    resultCount: document.getElementById("resultCount"),
    boardNote: document.getElementById("boardNote"),
    tokenGrid: document.getElementById("tokenGrid"),
    detailPanel: document.getElementById("detailPanel"),
    endpointStrip: document.getElementById("endpointStrip"),
  };

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function numberValue(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : 0;
  }

  function formatUsd(value) {
    const numeric = Number(value);
    if (!Number.isFinite(numeric)) return "unknown";
    if (numeric >= 1_000_000) return `$${(numeric / 1_000_000).toFixed(2)}m`;
    if (numeric >= 1_000) return `$${(numeric / 1_000).toFixed(1)}k`;
    return `$${numeric.toFixed(2)}`;
  }

  function shortAddress(address) {
    const value = String(address || "");
    if (value.length <= 16) return value;
    return `${value.slice(0, 6)}...${value.slice(-6)}`;
  }

  function titleCase(value) {
    return String(value || "")
      .replace(/[_-]/g, " ")
      .replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function birdeyeUrl(token) {
    return `https://birdeye.so/token/${encodeURIComponent(token.address)}?chain=${encodeURIComponent(summary.chain || "solana")}`;
  }

  function warningMatches(token) {
    if (state.warning === "all") return true;
    const warnings = token.warnings || [];
    if (state.warning === "liquidity-below") {
      return warnings.some((warning) => String(warning).startsWith("liquidity-below"));
    }
    return warnings.includes(state.warning);
  }

  function tokenSearchMatches(token) {
    if (!state.search) return true;
    const haystack = [
      token.symbol,
      token.name,
      token.address,
      token.source,
      token.classification,
      ...(token.warnings || []),
      ...(token.risk_flags || []),
    ].join(" ").toLowerCase();
    return haystack.includes(state.search);
  }

  function filteredTokens() {
    return assessments
      .filter((token) => state.classification === "all" || token.classification === state.classification)
      .filter((token) => state.source === "all" || token.source === state.source)
      .filter(warningMatches)
      .filter(tokenSearchMatches)
      .sort((a, b) => {
        if (state.sort === "liquidity") return numberValue(b.liquidity_usd) - numberValue(a.liquidity_usd);
        if (state.sort === "symbol") return String(a.symbol).localeCompare(String(b.symbol));
        if (state.sort === "warnings") return (b.warnings || []).length - (a.warnings || []).length;
        return numberValue(b.volume_24h_usd) - numberValue(a.volume_24h_usd);
      });
  }

  function countsBy(key) {
    return assessments.reduce((acc, token) => {
      const value = token[key] || "unknown";
      acc[value] = (acc[value] || 0) + 1;
      return acc;
    }, {});
  }

  function strongestTokens() {
    return [...assessments]
      .sort((a, b) => numberValue(b.volume_24h_usd) - numberValue(a.volume_24h_usd))
      .slice(0, 3)
      .map((token) => token.symbol)
      .join(", ");
  }

  function renderSummary() {
    const classifications = countsBy("classification");
    const missingSecurity = assessments.filter((token) => (token.warnings || []).includes("missing-security-data")).length;
    const cards = [
      {
        label: "Successful calls",
        value: summary.call_count ?? 0,
        caption: summary.qualification_complete ? "Sprint gate complete" : "Sprint gate incomplete",
      },
      {
        label: "Assessed tokens",
        value: assessments.length,
        caption: `${classifications.research || 0} research / ${classifications.watch || 0} watch / ${classifications.reject || 0} reject`,
      },
      {
        label: "Security gaps",
        value: missingSecurity,
        caption: "Token-security package access blocked",
      },
      {
        label: "Top volume sample",
        value: strongestTokens() || "none",
        caption: "Demo evidence, not a trade signal",
      },
    ];

    els.summaryCards.innerHTML = cards.map((card) => `
      <article class="summary-card">
        <p class="eyebrow">${escapeHtml(card.label)}</p>
        <span class="summary-value">${escapeHtml(card.value)}</span>
        <p class="summary-caption">${escapeHtml(card.caption)}</p>
      </article>
    `).join("");

    const mode = summary.mode || "demo";
    els.modeLabel.textContent = `${titleCase(mode)} evidence`;
    els.runLine.textContent = `${summary.timestamp_utc || "unknown time"} on ${summary.chain || "solana"}: ${summary.call_count || 0} successful Birdeye calls, ${assessments.length} token assessments, read-only output.`;
  }

  function renderSegmentedControl(container, labels, stateKey) {
    container.innerHTML = labels.map((item) => `
      <button
        class="segment-button"
        type="button"
        role="tab"
        aria-selected="${state[stateKey] === item.value ? "true" : "false"}"
        data-state-key="${escapeHtml(stateKey)}"
        data-value="${escapeHtml(item.value)}"
      >${escapeHtml(item.label)}</button>
    `).join("");
  }

  function renderControls() {
    const classificationCounts = countsBy("classification");
    renderSegmentedControl(els.classificationFilters, [
      { label: `All (${assessments.length})`, value: "all" },
      { label: `Research (${classificationCounts.research || 0})`, value: "research" },
      { label: `Watch (${classificationCounts.watch || 0})`, value: "watch" },
      { label: `Reject (${classificationCounts.reject || 0})`, value: "reject" },
    ], "classification");

    const sourceCounts = countsBy("source");
    renderSegmentedControl(els.sourceFilters, [
      { label: `All (${assessments.length})`, value: "all" },
      { label: `New listings (${sourceCounts.new_listing || 0})`, value: "new_listing" },
      { label: `Trending (${sourceCounts.token_trending || 0})`, value: "token_trending" },
    ], "source");
  }

  function tokenReasons(token) {
    const flags = token.risk_flags || [];
    const warnings = token.warnings || [];
    if (flags.length) return flags.map((flag) => `Reject: ${titleCase(flag)}.`);
    if (warnings.length) return warnings.map((warning) => `Research: ${titleCase(warning)}.`);
    return ["Watch: no critical flags were present in this sample."];
  }

  function renderTokenCard(token) {
    const warnings = token.warnings || [];
    const flags = token.risk_flags || [];
    const selected = token.address === state.selectedAddress;
    const liquidity = numberValue(token.liquidity_usd);
    const volume = numberValue(token.volume_24h_usd);
    const bar = Math.min(100, Math.max(4, Math.log10(Math.max(liquidity + volume, 1)) * 12));
    const chips = [
      ...flags.map((flag) => `<span class="mini-chip flag">${escapeHtml(titleCase(flag))}</span>`),
      ...warnings.slice(0, 3).map((warning) => `<span class="mini-chip warning">${escapeHtml(titleCase(warning))}</span>`),
    ].join("");

    return `
      <article class="token-card ${selected ? "selected" : ""}" data-address="${escapeHtml(token.address)}">
        <div class="token-head">
          <div class="token-title">
            <span class="symbol">${escapeHtml(token.symbol)}</span>
            <span class="token-name">${escapeHtml(token.name)}</span>
          </div>
          <span class="status-chip status-${escapeHtml(token.classification)}">${escapeHtml(token.classification)}</span>
        </div>
        <p class="token-source">${escapeHtml(titleCase(token.source))}</p>
        <div class="metric-row">
          <div class="metric-box">
            <span class="metric-label">Liquidity</span>
            <span class="metric-value">${escapeHtml(formatUsd(token.liquidity_usd))}</span>
          </div>
          <div class="metric-box">
            <span class="metric-label">24h volume</span>
            <span class="metric-value">${escapeHtml(formatUsd(token.volume_24h_usd))}</span>
          </div>
        </div>
        <div class="bar-track" aria-hidden="true"><span class="bar-fill" style="--bar: ${bar.toFixed(1)}%"></span></div>
        <div class="chip-row">${chips || '<span class="mini-chip">No listed warnings</span>'}</div>
        <div class="card-actions">
          <button class="detail-button" type="button" data-address="${escapeHtml(token.address)}">Inspect</button>
          <a href="${escapeHtml(birdeyeUrl(token))}" target="_blank" rel="noopener noreferrer">Birdeye</a>
        </div>
        <p class="address-line">${escapeHtml(shortAddress(token.address))}</p>
      </article>
    `;
  }

  function renderTokens() {
    const tokens = filteredTokens();
    els.resultCount.textContent = `${tokens.length} token${tokens.length === 1 ? "" : "s"}`;
    els.boardNote.textContent = tokens.length ? "Research-only output." : "No matching candidates.";
    if (!tokens.length) {
      els.tokenGrid.innerHTML = '<div class="empty-state">No token matches the active filter.</div>';
      renderDetail(null);
      return;
    }

    if (!tokens.some((token) => token.address === state.selectedAddress)) {
      state.selectedAddress = tokens[0].address;
    }

    els.tokenGrid.innerHTML = tokens.map(renderTokenCard).join("");
    renderDetail(assessments.find((token) => token.address === state.selectedAddress) || tokens[0]);
  }

  function renderDetail(token) {
    if (!token) {
      els.detailPanel.innerHTML = '<div class="empty-state">No selected token.</div>';
      return;
    }

    const reasons = tokenReasons(token).map((reason) => `<li>${escapeHtml(reason)}</li>`).join("");
    const flags = (token.risk_flags || []).length ? token.risk_flags.map(titleCase).join(", ") : "none";
    const warnings = (token.warnings || []).length ? token.warnings.map(titleCase).join(", ") : "none";

    els.detailPanel.innerHTML = `
      <div>
        <p class="eyebrow">Selected token</p>
        <h2>${escapeHtml(token.symbol)}</h2>
        <p class="run-line">${escapeHtml(token.name)}</p>
      </div>
      <span class="status-chip status-${escapeHtml(token.classification)}">${escapeHtml(token.classification)}</span>
      <dl class="detail-kv">
        <dt>Source</dt><dd>${escapeHtml(titleCase(token.source))}</dd>
        <dt>Liquidity</dt><dd>${escapeHtml(formatUsd(token.liquidity_usd))}</dd>
        <dt>Volume</dt><dd>${escapeHtml(formatUsd(token.volume_24h_usd))}</dd>
        <dt>Address</dt><dd>${escapeHtml(token.address)}</dd>
      </dl>
      <div class="detail-section">
        <h3>Verdict basis</h3>
        <ul class="reason-list">${reasons}</ul>
      </div>
      <div class="detail-section">
        <h3>Markers</h3>
        <dl class="detail-kv">
          <dt>Flags</dt><dd>${escapeHtml(flags)}</dd>
          <dt>Warnings</dt><dd>${escapeHtml(warnings)}</dd>
        </dl>
      </div>
      <div class="detail-section">
        <a href="${escapeHtml(birdeyeUrl(token))}" target="_blank" rel="noopener noreferrer">Open token on Birdeye</a>
      </div>
    `;
  }

  function renderEndpoints() {
    const counts = summary.endpoint_counts || {};
    const errors = Array.isArray(summary.endpoint_errors) ? summary.endpoint_errors : [];
    const endpoints = Array.isArray(summary.endpoints) ? summary.endpoints : Object.keys(counts);
    els.endpointStrip.innerHTML = endpoints.map((endpoint) => {
      const error = errors.find((item) => item.endpoint === endpoint);
      return `
        <article class="endpoint-card">
          <span class="endpoint-name">${escapeHtml(endpoint)}</span>
          <span class="endpoint-count">${escapeHtml(counts[endpoint] || 0)}</span>
          <p class="endpoint-meta">${error ? escapeHtml(`Blocked: HTTP ${error.status_code}`) : "Successful call count"}</p>
        </article>
      `;
    }).join("");
  }

  function render() {
    renderControls();
    renderSummary();
    renderTokens();
    renderEndpoints();
  }

  document.addEventListener("click", (event) => {
    const segment = event.target.closest(".segment-button");
    if (segment) {
      state[segment.dataset.stateKey] = segment.dataset.value;
      render();
      return;
    }

    const detailButton = event.target.closest("[data-address]");
    if (detailButton) {
      state.selectedAddress = detailButton.dataset.address;
      renderTokens();
    }
  });

  els.searchInput.addEventListener("input", (event) => {
    state.search = event.target.value.trim().toLowerCase();
    renderTokens();
  });

  els.warningFilter.addEventListener("change", (event) => {
    state.warning = event.target.value;
    renderTokens();
  });

  els.sortSelect.addEventListener("change", (event) => {
    state.sort = event.target.value;
    renderTokens();
  });

  render();
})();
