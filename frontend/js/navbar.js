function renderNavbar() {
  const navbar = document.getElementById("navbar");
  if (!navbar) return;

  const currentUserRaw = localStorage.getItem("currentUser");
  let currentUser = null;
  try {
    currentUser = currentUserRaw ? JSON.parse(currentUserRaw) : null;
  } catch {
    currentUser = null;
  }

  let links = '<a href="index.html">Home</a>';

  if (!currentUser) {
    links += `
       <a href="login.html">Login</a>
       <a href="signup.html">Sign Up</a>
    `;
  } else if (currentUser.role === "admin") {
    links += `
       <a href="admin-dashboard.html">Dashboard</a>
       <a href="view-books-admin.html">View Books</a>
       <a href="add_book.html">Add Book</a>
       <a href="#" id="logoutBtn">Logout</a>
    `;
  } else {
    links += `
       <a href="user-dashboard.html">View Books</a>
       <a href="search.html">Search</a>
       <a href="borrowed-books.html">Borrowed Books</a>
       <a href="#" id="logoutBtn">Logout</a>
    `;
  }

  navbar.innerHTML = links;

  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", async function (e) {
      e.preventDefault();
      try {
        await apiRequest("POST", "/logout/");
      } catch {
        /* ignore */
      }
      localStorage.removeItem("currentUser");
      window.location.href = "index.html";
    });
  }
}

(async function bootstrapNavbar() {
  try {
    const data = await apiRequest("GET", "/me/");
    if (data && data.user) {
      localStorage.setItem("currentUser", JSON.stringify(data.user));
    } else {
      localStorage.removeItem("currentUser");
    }
  } catch {
    localStorage.removeItem("currentUser");
  }
  renderNavbar();
})();
