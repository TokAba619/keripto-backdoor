// Change this later deployed backend URL (Render/Cloud Run)
const API_BASE = "http://127.0.0.1:8000";

async function postFile(endpoint, file, vaultPassword, filePassword = null) {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("vault_password", vaultPassword);
  if (filePassword) fd.append("file_password", filePassword);

  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    body: fd
  });

  if (!res.ok) {
    let msg = "Request failed";
    try {
      const data = await res.json();
      msg = data.detail || msg;
    } catch {}
    throw new Error(msg);
  }

  return await res.blob();
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}


function setActiveNav() {
  const path = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("nav a").forEach(a => {
    const href = a.getAttribute("href");
    if (href === path) a.classList.add("active");
  });
}


function showStatus(el, type, msg) {
  el.classList.remove("ok", "err");
  el.classList.add(type === "ok" ? "ok" : "err");
  el.textContent = msg;
  el.style.display = "block";
}

function isStrongPassword(password) {
  const regex =
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$/;
  return regex.test(password);
}

function initEncryptPage() {
  const file = document.getElementById("file");
  const pass = document.getElementById("password");
  const btn = document.getElementById("encryptBtn");
  const bar = document.getElementById("progress");
  const status = document.getElementById("status");

  btn.addEventListener("click", async () => {
    status.style.display = "none";

    if (!file.files?.length) return showStatus(status, "err", "Please choose a file first.");
    if (!isStrongPassword(pass.value)) {
  return showStatus(
    status,
    "err",
    "Password must be at least 8 characters and include uppercase, lowercase, number, and symbol."
  );
}


    btn.disabled = true;

    if (bar) bar.style.display = "block";

    try {
      const originalName = file.files[0].name;

 
      // Ask user for optional file-level password
let filePass = prompt("Enter file password (optional, for PDF only):");
filePass = filePass && filePass.trim() !== "" ? filePass : null;

const blob = await postFile("/encrypt", file.files[0], pass.value, filePass);



      downloadBlob(blob, `${originalName}.enc`);

      showStatus(status, "ok", `Encrypted successfully: ${originalName}.enc`);
    } catch (e) {
      showStatus(status, "err", e.message);
    } finally {
      btn.disabled = false;
      if (bar) bar.style.display = "none";
    }
  });
  pass.addEventListener("input", () => {
  pass.style.borderColor = isStrongPassword(pass.value) ? "green" : "red";
});

}


function initDecryptPage() {
  const file = document.getElementById("file");
  const pass = document.getElementById("password");
  const btn = document.getElementById("decryptBtn");
  const bar = document.getElementById("progress");
  const status = document.getElementById("status");

  btn.addEventListener("click", async () => {
    status.style.display = "none";

    if (!file.files?.length) return showStatus(status, "err", "Please choose an encrypted file (.enc) first.");
    if (!pass.value) return showStatus(status, "err", "Please enter a password.");

    btn.disabled = true;
    if (bar) bar.style.display = "block";

    try {
      const encName = file.files[0].name;


      const blob = await postFile("/decrypt", file.files[0], pass.value);

      const outName = encName.toLowerCase().endsWith(".enc")
        ? encName.slice(0, -4)
        : "decrypted_file";

      downloadBlob(blob, outName);

      showStatus(status, "ok", `Decrypted successfully: ${outName}`);
    } catch (e) {
      showStatus(status, "err", e.message);
    } finally {
      btn.disabled = false;
      if (bar) bar.style.display = "none";
    }
  });
}

function initPasswordToggle() {
  const pass = document.getElementById("password");
  const toggle = document.getElementById("togglePassword");

  if (!pass || !toggle) return;

  toggle.addEventListener("click", () => {
    const isHidden = pass.type === "password";
    pass.type = isHidden ? "text" : "password";
    toggle.textContent = isHidden ? "🙈" : "👁️";
  });
}


document.addEventListener("DOMContentLoaded", () => {
  setActiveNav();
  initPasswordToggle();
  if (document.body.dataset.page === "encrypt") initEncryptPage();
  if (document.body.dataset.page === "decrypt") initDecryptPage();
});
