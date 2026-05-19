function updateRowStatus(row, status) {
  const statusCell = row.cells[2].querySelector("b");
  if (!statusCell) return;
  statusCell.innerText = status;
  statusCell.style.color = status === "Available" ? "green" : "red";
}

window.onload = async function () {
  const tbody = document.querySelector("table tbody");
  if (!tbody) return;

  let books = [];
  try {
    const data = await apiRequest("GET", "/books/");
    books = data.books || [];
  } catch {
    tbody.innerHTML = `<tr><td colspan="4">Could not load books. Please log in again.</td></tr>`;
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const q = params.get("searchQuery") ? params.get("searchQuery").toLowerCase() : "";
  const cat = params.get("category") ? params.get("category").toLowerCase() : "";

  tbody.innerHTML = "";
  books.forEach((book) => {
    const title = (book.title || "").toLowerCase();
    const author = (book.author || "").toLowerCase();
    const tags = (book.category || []).map((t) => String(t).toLowerCase());

    const isSearchEmpty = q === "" && cat === "";
    const matchesQuery = title.includes(q) || author.includes(q);
    const matchesCat = cat === "" || tags.includes(cat);

    if (!(isSearchEmpty || (matchesQuery && matchesCat))) {
      return;
    }

    const detailHref =
      book.slug === "cpp"
        ? "details-cpp.html"
        : book.slug === "clean"
          ? "details-clean.html"
          : book.slug === "alg"
            ? "details-algorithms.html"
            : `details-generic.html?slug=${encodeURIComponent(book.slug)}`;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${book.title}</td>
      <td>${book.author}</td>
      <td><b style="color:${book.status === "Available" ? "green" : "red"}">${book.status}</b></td>
      <td><a href="${detailHref}">View Details</a></td>
    `;
    tbody.appendChild(tr);
  });

  if (!tbody.children.length) {
    tbody.innerHTML = `<tr><td colspan="4">No books match your filters.</td></tr>`;
  }
};
