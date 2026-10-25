// Renders publications.json (refreshed weekly from ORCID by a GitHub Action).
// The static list in index.html stays as a fallback if this fails.
(function () {
  const list = document.getElementById("pubs");
  const meta = document.getElementById("pubs-meta");
  if (!list) return;

  const esc = (s) => String(s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // Shorten long author lists but always keep Colin visible, in bold.
  function authors(raw) {
    if (!raw) return "";
    const names = raw.split(", ");
    const me = names.findIndex((n) => /Warnes/.test(n));
    let shown = names;
    if (names.length > 6) {
      shown = names.slice(0, 3);
      if (me >= 3) shown.push("…", names[me]);
      shown.push("et al.");
    }
    return shown.map((n) => /Warnes/.test(n) ? `<strong>${esc(n)}</strong>` : esc(n)).join(", ");
  }

  fetch("publications.json", { cache: "no-cache" })
    .then((r) => r.ok ? r.json() : Promise.reject(r.status))
    .then((data) => {
      if (!data.publications || !data.publications.length) return;
      list.innerHTML = data.publications.map((p) => {
        const a = authors(p.authors);
        const title = p.url ? `<a href="${esc(p.url)}">${esc(p.title)}</a>` : esc(p.title);
        const venue = [p.venue && `<em>${esc(p.venue)}</em>`, p.year].filter(Boolean).join(", ") +
          (p.preprint ? ` <span class="tag">preprint</span>` : "");
        const lead = a ? a.replace(/\.$/, "") + ". " : "";
        return `<li>${lead}${title}. ${venue}.</li>`;
      }).join("");
      if (meta) {
        meta.innerHTML = `From <a href="${esc(data.profile)}">ORCID</a> · updated ${esc(data.updated)}`;
      }
    })
    .catch(() => {});
})();
