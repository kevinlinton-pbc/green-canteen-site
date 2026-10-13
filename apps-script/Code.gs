/**
 * Green Canteen contact and feedback forms -> email.
 * Deploy: Extensions > Apps Script (or script.google.com) > paste this file >
 * Deploy > New deployment > type "Web app" > Execute as: Me > Who has access: Anyone.
 * Copy the "/exec" URL into FORM_ENDPOINT in contact.html and feedback.html.
 * After editing, update the existing deployment (Manage deployments > Edit > Version: New version)
 * so the /exec URL stays the same. If Google asks to authorise new permissions, accept them.
 */
const TO = "greencanteen@plantbasedcampus.org";
const COPY_TO = "kevin.linton@plantbasedcampus.org"; // direct copy, because Gmail hides group mail sent by this account from its own inbox
const FROM = "no-reply@plantbasedcampus.org"; // must be a Send-as alias in the deploying account
const MAX_PER_HOUR = 20; // global cap, a cheap brake against spam floods
const FEEDBACK_SHEET_ID = "1cyYilpv_rnynD2uOvQDSkF2jA0sJUE2a1ucJj4PKMao"; // "Green Canteen Feedback" in Drive > Restaurant (Green Canteen)
const FEEDBACK_SCALES = [["taste", "Taste"], ["portion", "Portion"], ["value", "Value for money"], ["again", "Would buy again"]]; // must match QUESTIONS in feedback.html

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return json_({ ok: true }); // honeypot: bots fill it, people don't
  if (p.form === "feedback") return feedback_(p);

  const name = clean_(p.name, 120).replace(/\s+/g, " "), email = clean_(p.email, 200);
  const interest = p.interest === "Partner" ? "Partner" : "Volunteer";
  if (!name || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json_({ ok: false, error: "invalid" });
  if (!underLimit_()) return json_({ ok: false, error: "busy" });

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

function feedback_(p) {
  const meal = clean_(p.meal, 80), email = clean_(p.email, 200);
  const scores = FEEDBACK_SCALES.map(([k, label]) => [label, Math.round(+p[k])]);
  if (!meal || scores.some(([, n]) => !(n >= 1 && n <= 5))) return json_({ ok: false, error: "invalid" });
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return json_({ ok: false, error: "invalid" });
  if (!underLimit_()) return json_({ ok: false, error: "busy" });

  const comments = clean_(p.comments, 5000);
  // Columns: Timestamp, Meal, Taste, Portion, Value for money, Would buy again, Comments, Email
  SpreadsheetApp.openById(FEEDBACK_SHEET_ID).getSheets()[0]
    .appendRow([new Date(), cell_(meal), ...scores.map(([, n]) => n), cell_(comments), cell_(email)]);

  const lines = [
    "Meal: " + meal,
    "",
    ...scores.map(([label, n]) => label + ": " + n + "/5"),
    "",
    "Email: " + (email || "(not given)"),
    "",
    comments || "(no comments)"
  ];
  const opts = { from: FROM, cc: COPY_TO, name: "Green Canteen feedback" };
  if (email) opts.replyTo = email;
  GmailApp.sendEmail(TO, "Green Canteen feedback: " + meal, lines.join("\n"), opts);
  return json_({ ok: true });
}

function underLimit_() {
  const lock = LockService.getScriptLock();
  lock.waitLock(5000);
  try {
    const cache = CacheService.getScriptCache();
    const n = +(cache.get("count") || 0);
    if (n >= MAX_PER_HOUR) return false;
    cache.put("count", String(n + 1), 3600);
    return true;
  } finally {
    lock.releaseLock();
  }
}

function clean_(v, max) {
  return String(v || "").trim().slice(0, max);
}

// Stops visitor text starting with = + - @ being run as a spreadsheet formula.
function cell_(v) {
  return /^[=+\-@]/.test(v) ? "'" + v : v;
}

function json_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
