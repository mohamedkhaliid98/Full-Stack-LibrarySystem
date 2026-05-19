(async function () {
  let currentUser = null;
  try {
    currentUser = JSON.parse(localStorage.getItem("currentUser") || "null");
  } catch {
    currentUser = null;
  }

  if (!currentUser || currentUser.role !== "admin") {
    alert("Access denied! Admins only.");
    window.location.href = "login.html";
    return;
  }

  async function displayBooks() {
    const tableBody = document.querySelector("#booksTable tbody");
    if (!tableBody) return;

    try {
      const data = await apiRequest("GET", "/admin/books/");
      tableBody.innerHTML = "";
      data.books.forEach((book) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${book.title}</td>
          <td>${book.author}</td>
          <td>${book.category}</td>
          <td>${book.available ? "Available" : "Borrowed"}</td>
         <td>
            <a href="edit-book.html?id=${book.id}" class="action-btn edit-btn">Edit</a>
            <button type="button" class="action-btn delete-btn" data-id="${book.id}">Delete</button>
         </td>

        `;
        tableBody.appendChild(row);
      });

      tableBody.querySelectorAll("button[data-id]").forEach((btn) => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-id");
          if (!confirm("Delete this book?")) return;
          try {
            await apiRequest("DELETE", `/admin/books/${id}/delete/`);
            await displayBooks();
          } catch (e) {
            alert(e.message || "Delete failed");
          }
        });
      });
    } catch (e) {
      tableBody.innerHTML = `<tr><td colspan="5">${e.message || "Could not load books."}</td></tr>`;
    }
  }

  await displayBooks();
})();
