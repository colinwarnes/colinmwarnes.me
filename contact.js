// Contact form: enforces the 50-word limit and submits to Web3Forms without leaving the page.
(function () {
  const form = document.getElementById("contact-form");
  if (!form) return;
  const message = form.querySelector("#c-message");
  const count = form.querySelector("#c-count");
  const status = form.querySelector("#c-status");
  const button = form.querySelector("button");
  const MAX_WORDS = 50;

  const words = (s) => (s.trim().match(/\S+/g) || []).length;

  function updateCount() {
    const n = words(message.value);
    count.textContent = `${n} / ${MAX_WORDS} words`;
    count.classList.toggle("over", n > MAX_WORDS);
    message.setCustomValidity(n > MAX_WORDS ? `Please keep your message to ${MAX_WORDS} words.` : "");
  }
  message.addEventListener("input", updateCount);
  updateCount();

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    if (form.access_key.value.startsWith("YOUR_")) {
      status.textContent = "The contact form isn't set up yet. Please try again soon.";
      status.className = "status error";
      return;
    }
    button.disabled = true;
    status.textContent = "Sending…";
    status.className = "status";
    try {
      const res = await fetch(form.action, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form),
      });
      const data = await res.json();
      if (!res.ok || !data.success) throw new Error(data.message || res.status);
      form.reset();
      updateCount();
      status.textContent = "Thanks! Your message has been sent.";
      status.className = "status ok";
    } catch (err) {
      status.textContent = "Sorry, something went wrong. Please try again later.";
      status.className = "status error";
    } finally {
      button.disabled = false;
    }
  });
})();
