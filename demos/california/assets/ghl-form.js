/* SkyBlue Pool Care quote form -> GoHighLevel.
 *
 * Paste your GHL Inbound Webhook URL below (Automation > Workflows >
 * trigger "Inbound Webhook"). A single form can override it with a
 * data-ghl-webhook="..." attribute. See GHL-SETUP.md.
 *
 * With no URL set, the form validates and goes to thank-you.html so the
 * site can be tested end to end before GHL is wired.
 */
(function () {
  var GHL_WEBHOOK_URL = window.GHL_WEBHOOK_URL || "";
  var THANK_YOU = "thank-you.html";

  var params = new URLSearchParams(location.search);

  function digits(s) { return (s || "").replace(/\D/g, ""); }

  function setStatus(form, msg, bad) {
    var el = form.querySelector(".f-status");
    if (!el) return;
    el.textContent = msg;
    el.classList.toggle("bad", !!bad);
  }

  function validate(form) {
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (f) {
      var v = f.value.trim();
      var bad = !v ||
        (f.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) ||
        (f.type === "tel" && digits(v).length < 10);
      f.closest(".f-field").classList.toggle("invalid", bad);
      f.setAttribute("aria-invalid", bad ? "true" : "false");
      if (bad && ok) { f.focus(); ok = false; }
    });
    return ok;
  }

  document.querySelectorAll("form[data-ghl-form]").forEach(function (form) {
    form.page_url && (form.page_url.value = location.href);
    ["utm_source", "utm_medium", "utm_campaign", "utm_term", "gclid"].forEach(function (k) {
      if (form[k]) form[k].value = params.get(k) || "";
    });

    form.addEventListener("input", function (ev) {
      var field = ev.target.closest(".f-field");
      if (field) field.classList.remove("invalid");
    });

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (form.website && form.website.value) return; // honeypot
      if (!validate(form)) {
        setStatus(form, "Please fill in the highlighted fields.", true);
        return;
      }

      var data = {};
      new FormData(form).forEach(function (v, k) { if (k !== "website") data[k] = String(v).trim(); });
      data.phone = "+1" + digits(data.phone).slice(-10);
      data.sms_consent = data.sms_consent === "yes";
      data.tags = ["website lead", (data.service_needed || "").toLowerCase(), data.page_city ? "area: " + data.page_city.toLowerCase() : ""].filter(Boolean);
      data.submitted_at = new Date().toISOString();

      var url = form.getAttribute("data-ghl-webhook") || GHL_WEBHOOK_URL;
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      setStatus(form, "Sending...");

      if (!url) {
        console.info("No GHL webhook set yet. Payload:", data);
        location.href = THANK_YOU;
        return;
      }

      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error(r.status);
        location.href = THANK_YOU;
      }).catch(function () {
        btn.disabled = false;
        setStatus(form, "That didn't go through. Please call (310) 421-8863 or try again.", true);
      });
    });
  });
})();
