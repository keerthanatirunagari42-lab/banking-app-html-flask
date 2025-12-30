const BASE_URL = "http://127.0.0.1:5000";

/* =========================
   LOGIN (index.html)
========================= */
function login() {
  const accNo = document.getElementById("acc_no").value;
  const pin = document.getElementById("pin").value;

  if (!accNo || !pin) {
    alert("Please enter account number and pin");
    return;
  }

  fetch(`${BASE_URL}/account/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      acc_no: accNo,
      pin: pin
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.message === "Login successful") {
        localStorage.setItem("accNo", accNo);
        localStorage.setItem("pin", pin);
        alert("Login successful");
        window.location.href = "dashboard.html";
      } else {
        alert("Invalid credentials");
      }
    })
    .catch(err => console.error(err));
}

function register() {
  const accNoInput = document.getElementById("acc_no");
  const nameInput = document.getElementById("name");
  const pinInput = document.getElementById("pin");

  if (!accNoInput || !nameInput || !pinInput) {
    alert("HTML input IDs are wrong");
    return;
  }

  const accNo = accNoInput.value;
  const name = nameInput.value;
  const pin = pinInput.value;

  if (!accNo || !name || !pin) {
    alert("Please fill all fields");
    return;
  }

  fetch(`${BASE_URL}/account/create`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      acc_no: accNo,
      name: name,
      pin: pin
    })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      window.location.href = "index.html";
    })
    .catch(err => {
      console.error(err);
      alert("Server error");
    });
}


/* =========================
   DASHBOARD PROTECTION
========================= */
const accNo = localStorage.getItem("accNo");
const pin = localStorage.getItem("pin");

// run only on dashboard page
if (window.location.pathname.includes("dashboard.html")) {
  if (!accNo || !pin) {
    alert("Please login first");
    window.location.href = "index.html";
  }
}

/* =========================
   CHECK BALANCE
========================= */
function checkBalance() {
  fetch(`${BASE_URL}/account/balance`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      acc_no: accNo,
      pin: pin
    })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerText =
        "Current Balance: " + data.balance;
    })
    .catch(err => console.error(err));
}

/* =========================
   DEPOSIT
========================= */
function deposit() {
  const amount = Number(document.getElementById("amount").value);

  if (!amount || amount <= 0) {
    alert("Enter valid amount");
    return;
  }

  fetch(`${BASE_URL}/account/deposit`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      acc_no: accNo,
      pin: pin,
      amount: amount
    })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerText =
        data.message + " | Balance: " + data.balance;
    })
    .catch(err => console.error(err));
}

/* =========================
   WITHDRAW
========================= */
function withdraw() {
  const amount = Number(document.getElementById("amount").value);

  if (!amount || amount <= 0) {
    alert("Enter valid amount");
    return;
  }

  fetch(`${BASE_URL}/account/withdraw`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      acc_no: accNo,
      pin: pin,
      amount: amount
    })
  })
    .then(res => res.json())
    .then(data => {
      document.getElementById("result").innerText =
        data.message + " | Balance: " + data.balance;
    })
    .catch(err => console.error(err));
}

/* =========================
   LOGOUT (OPTIONAL)
========================= */
function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}
