function bookSlugFromBody() {
  return document.body.getAttribute("data-book-slug") || "";
}

window.onload = function () {
  refreshDetails();
};

async function refreshDetails() {
  const slug = bookSlugFromBody();
  if (!slug) return;

  let book;
  try {
    const data = await apiRequest("GET", `/books/${encodeURIComponent(slug)}/`);
    book = data.book;
  } catch {
    alert("Could not load book details.");
    return;
  }

  const statusTag = document.querySelector("p b");
  const form = document.querySelector("form");
  if (!statusTag || !form) return;

  const titleEl = document.getElementById("detailTitle");
  const authorEl = document.getElementById("detailAuthor");
  const categoryEl = document.getElementById("detailCategory");
  const descEl = document.getElementById("detailDescription");
  if (titleEl) titleEl.textContent = book.title;
  if (authorEl) authorEl.textContent = book.author;
  if (categoryEl) {
    const tags = book.category || [];
    categoryEl.textContent = book.shelfCategory || (tags.length ? tags.join(", ") : "");
  }
  if (descEl) descEl.textContent = book.description || "";

  const button = form.querySelector("button");
  statusTag.innerText = book.status;
  statusTag.style.color = book.status === "Available" ? "green" : "red";

  form.onsubmit = async function (e) {
    e.preventDefault();
    try {
      if (book.status === "Borrowed") {
        await apiRequest("POST", `/books/${encodeURIComponent(slug)}/return/`);
        alert("Book Returned!");
      } else {
        await apiRequest("POST", `/books/${encodeURIComponent(slug)}/borrow/`);
        alert("Book Borrowed!");
        window.location.href = "borrowed-books.html";
        return;
      }
      await refreshDetails();
    } catch (err) {
      alert(err.message || "Action failed");
    }
  };

  if (book.status === "Borrowed") {
    button.innerText = "Return Book";
    button.style.backgroundColor = "orange";
  } else {
    button.innerText = "Borrow This Book";
    button.style.backgroundColor = "";
  }
}
