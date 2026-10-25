// Highlights the sidebar link for the section currently in view.
(function () {
  const links = [...document.querySelectorAll(".sidebar a")];
  const sections = links.map((a) => document.querySelector(a.getAttribute("href"))).filter(Boolean);
  if (!sections.length) return;

  function update() {
    // The active section is the last one whose top has passed a line just below the top bar.
    const line = 140;
    let current = sections[0];
    for (const s of sections) {
      if (s.getBoundingClientRect().top <= line) current = s;
    }
    // At the very bottom, the last section is active even if it is short.
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      current = sections[sections.length - 1];
    }
    for (const a of links) {
      const on = a.getAttribute("href") === "#" + current.id;
      a.classList.toggle("active", on);
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    }
  }

  window.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
})();
