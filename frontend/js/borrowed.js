window.onload = async function () {
  await displayBorrowedBooks();
};

async function displayBorrowedBooks() {
  const tableBody = document.querySelector("table tbody");
  if (!tableBody) return;

  tableBody.innerHTML = "";

  let books = [];
  try {
    const data = await apiRequest("GET", "/borrowed/");
    books = data.books || [];
  } catch (e) {
    tableBody.innerHTML = `<tr><td colspan="5">${e.message || "Could not load borrowed books."}</td></tr>`;
    return;
  }

  if (books.length === 0) {
    tableBody.innerHTML = "<tr><td colspan='5'>No books borrowed yet.</td></tr>";
    return;
  }

  books.forEach((book) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td>${book.borrowDate || ""}</td>
      <td>${book.returnDeadline || ""}</td>
      <td><button type="button">Return Book</button></td>
    `;
    const btn = row.querySelector("button");
    btn.addEventListener("click", () => returnFromTable(book.id));
    tableBody.appendChild(row);
  });
}

async function returnFromTable(slug) {
  if (!confirm("Are you sure you want to return this book?")) return;
  try {
    await apiRequest("POST", `/books/${encodeURIComponent(slug)}/return/`);
    alert("Book Returned!");
    await displayBorrowedBooks();
  } catch (e) {
    alert(e.message || "Return failed");
  }
}
