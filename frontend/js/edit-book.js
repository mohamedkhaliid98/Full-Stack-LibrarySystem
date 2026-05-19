const params = new URLSearchParams(window.location.search);
const bookPk = params.get("id");
const form = document.querySelector("form");

if (form && bookPk) {
  form.dataset.api = "edit-book";
  form.dataset.bookPk = bookPk;
}

(async function loadBook() {
  if (!form || !bookPk) {
    alert("Missing book id. Open this page from the admin book list.");
    return;
  }
  try {
    const data = await apiRequest("GET", `/admin/books/${bookPk}/detail/`);
    const b = data.book;
    const title = document.querySelector('input[name="title"]');
    const author = document.querySelector('input[name="author"]');
    const category = document.querySelector('select[name="category"]');
    const description = document.querySelector('textarea[name="description"]');
    if (title) title.value = b.title || "";
    if (author) author.value = b.author || "";
    if (category) category.value = b.category || "";
    if (description) description.value = b.description || "";
  } catch (e) {
    alert(e.message || "Could not load book");
  }
})();
