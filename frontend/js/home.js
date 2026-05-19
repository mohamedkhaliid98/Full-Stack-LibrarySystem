const currentUser = JSON.parse(localStorage.getItem("currentUser") || "null");

if (currentUser) {
  alert("Welcome back, " + currentUser.fullName);
}

const buttons = document.getElementById("homeButtons");

if (currentUser && buttons) {
  buttons.style.display = "none";
}
