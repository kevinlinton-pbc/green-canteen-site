/**
 * Green Canteen contact form -> email.
 * Deploy: Extensions > Apps Script (or script.google.com) > paste this file >
 * Deploy > New deployment > type "Web app" > Execute as: Me > Who has access: Anyone.
 * Copy the "/exec" URL into FORM_ENDPOINT in contact.html.
 */
const TO = "greencanteen@plantbasedcampus.org";
const COPY_TO = "kevin.linton@plantbasedcampus.org"; // direct copy, because Gmail hides group mail sent by this account from its own inbox
const FROM = "no-reply@plantbasedcampus.org"; // must be a Send-as alias in the deploying account
const MAX_PER_HOUR = 20; // global cap, a cheap brake against spam floods

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return json_({ ok: true }); // honeypot: bots fill it, people don't

  const name = clean_(p.name, 120).replace(/\s+/g, " "), email = clean_(p.email, 200);
  const interest = p.interest === "Partner" ? "Partner" : "Volunteer";
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json_({ ok: false, error: "invalid" });

  const lock = LockService.getScriptLock();
  lock.waitLock(5000);
  try {
    const cache = CacheService.getScriptCache();
    const n = +(cache.get("count") || 0);
    if (n >= MAX_PER_HOUR) return json_({ ok: false, error: "busy" });
    cache.put("count", String(n + 1), 3600);
  } finally {
    lock.releaseLock();
  }

  const lines = [
    "Interest: " + interest,
    interest === "Partner" ? "Partnership type: " + clean_(p.partnership_type, 80) : null,
    interest === "Partner" ? "Organisation: " + clean_(p.organisation, 200) : null,
    "Name: " + name,
    "Email: " + email,
    "",
    clean_(p.message, 5000)
  ].filter(l => l !== null);

  // Sent as a verified "Send mail as" alias of the deploying account, so the group delivers
  // it to every member (including the account owner) instead of treating it as their own post.
  GmailApp.sendEmail(TO, "Green Canteen enquiry: " + interest + " (" + name + ")", lines.join("\n"), {
    from: FROM,
    cc: COPY_TO,
    replyTo: email,
    name: name + " (via Green Canteen website)"
  });
  return json_({ ok: true });
}

function clean_(v, max) {
  return String(v || "").trim().slice(0, max);
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
