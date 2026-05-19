const loginForm = document.getElementById("loginForm");
const loginMessage = document.getElementById("loginMessage");

loginForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const email = document.getElementById("loginEmail").value.trim();
  const password = document.getElementById("loginPassword").value.trim();

  loginMessage.textContent = "";
  loginMessage.style.color = "red";

  if (!email || !password) {
    loginMessage.textContent = "Please fill in all fields.";
    return;
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    loginMessage.textContent = "Invalid email format.";
    return;
  }

  try {
    const data = await apiRequest("POST", "/login/", { email, password });
    localStorage.setItem("currentUser", JSON.stringify(data.user));
    loginMessage.style.color = "green";
    loginMessage.textContent = "Login successful! Redirecting...";
    setTimeout(function () {
      if (data.user.role === "admin") {
        window.location.href = "admin-dashboard.html";
      } else {
        window.location.href = "user-dashboard.html";
      }
    }, 800);
  } catch (err) {
    loginMessage.textContent = err.message || "Login failed.";
  }
});
