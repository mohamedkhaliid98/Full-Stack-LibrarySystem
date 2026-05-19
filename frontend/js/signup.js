const signupForm = document.getElementById("signupForm");
const signupMessage = document.getElementById("signupMessage");

signupForm.addEventListener("submit", async function (event) {
  event.preventDefault();

  const fullName = document.getElementById("fullName").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();
  const confirmPassword = document.getElementById("confirmPassword").value.trim();
  const accountType = document.getElementById("accountType").value;

  signupMessage.textContent = "";
  signupMessage.style.color = "red";

  if (!fullName || !email || !password || !confirmPassword || !accountType) {
    signupMessage.textContent = "Please fill in all fields.";
    return;
  }

  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailPattern.test(email)) {
    signupMessage.textContent = "Please enter a valid email.";
    return;
  }

  if (password.length < 6) {
    signupMessage.textContent = "Password must be at least 6 characters.";
    return;
  }

  if (password !== confirmPassword) {
    signupMessage.textContent = "Passwords do not match.";
    return;
  }

  try {
    await apiRequest("POST", "/register/", {
      fullName,
      email,
      password,
      role: accountType,
    });
    signupMessage.style.color = "green";
    signupMessage.textContent = "Account created successfully! Redirecting...";
    signupForm.reset();
    setTimeout(() => {
      window.location.href = "login.html";
    }, 900);
  } catch (err) {
    signupMessage.textContent = err.message || "Could not create account.";
  }
});
