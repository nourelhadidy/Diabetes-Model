// Tab switching
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach((p) => p.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
  });
});

function formToJSON(form) {
  const data = {};
  new FormData(form).forEach((value, key) => {
    // numeric fields: convert to number
    data[key] = isNaN(value) || value === "" ? value : Number(value);
  });
  return data;
}

function renderResult(el, res, error) {
  el.classList.remove("high", "low", "error");
  el.classList.add("show");

  if (error) {
    el.classList.add("error");
    el.innerHTML = `⚠️ ${error}`;
    return;
  }

  const pct = (res.probability * 100).toFixed(2);
  const isHigh = res.prediction === 1;
  el.classList.add(isHigh ? "high" : "low");
  el.innerHTML = `
    <strong>Risk Probability:</strong> ${pct}%<br/>
    ${isHigh ? "⚠️ High Risk of Diabetes Detected" : "✅ Low Risk of Diabetes"}
  `;
}

async function handleSubmit(formId, endpoint, resultId) {
  const form = document.getElementById(formId);
  const resultEl = document.getElementById(resultId);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const payload = formToJSON(form);

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        renderResult(resultEl, null, err.detail || `Request failed (${res.status})`);
        return;
      }

      const data = await res.json();
      renderResult(resultEl, data, null);
    } catch (err) {
      renderResult(resultEl, null, "Network error — is the API running?");
    }
  });
}

handleSubmit("form-v1", "/api/predict/v1", "result-v1");
handleSubmit("form-v2", "/api/predict/v2", "result-v2");
