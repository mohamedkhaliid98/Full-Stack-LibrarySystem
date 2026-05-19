document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", async function (event) {
    const apiMode = form.dataset.api;
    if (!apiMode) {
      return;
    }
    event.preventDefault();

    const title = document.querySelector('input[name="title"]');
    const author = document.querySelector('input[name="author"]');
    const category = document.querySelector('select[name="category"]');
    const description = document.querySelector('textarea[name="description"]');

    let isValid = true;
    removeErrors();

    if (!title.value.trim()) {
      showError(title, "Book Name is required");
      isValid = false;
    } else if (title.value.trim().length < 2) {
      showError(title, "Book Name must be at least 2 characters");
      isValid = false;
    }

    if (!author.value.trim()) {
      showError(author, "Author is required");
      isValid = false;
    } else if (author.value.trim().length < 2) {
      showError(author, "Author name must be at least 2 characters");
      isValid = false;
    }

    if (!category.value) {
      showError(category, "Please select a category");
      isValid = false;
    }

    if (!description.value.trim()) {
      showError(description, "Description is required");
      isValid = false;
    } else if (description.value.trim().length < 10) {
      showError(description, "Description must be at least 10 characters");
      isValid = false;
    }

    if (!isValid) {
      return;
    }

    try {
      if (apiMode === "add-book") {
        await apiRequest("POST", "/admin/books/create/", {
          title: title.value.trim(),
          author: author.value.trim(),
          category: category.value,
          description: description.value.trim(),
        });
        showSuccessMessage("Book saved to the server.");
      } else if (apiMode === "edit-book") {
        const id = form.dataset.bookPk;
        await apiRequest("PUT", `/admin/books/${id}/`, {
          title: title.value.trim(),
          author: author.value.trim(),
          category: category.value,
          description: description.value.trim(),
        });
        showSuccessMessage("Book updated on the server.");
      }
    } catch (e) {
      alert(e.message || "Save failed");
    }
  });

  const resetBtn = document.querySelector('button[type="reset"]');
  if (resetBtn) {
    resetBtn.addEventListener("click", function () {
      removeErrors();
    });
  }
});

function showError(inputElement, message) {
  const errorDiv = document.createElement("div");
  errorDiv.className = "error-message";
  errorDiv.style.color = "#e74c3c";
  errorDiv.style.fontSize = "12px";
  errorDiv.style.marginTop = "5px";
  errorDiv.innerText = message;
  errorDiv.style.display = "block";
  inputElement.style.borderColor = "#e74c3c";
  inputElement.parentNode.insertBefore(errorDiv, inputElement.nextSibling);
}

function removeErrors() {
  document.querySelectorAll(".error-message").forEach(function (error) {
    error.remove();
  });
  document.querySelectorAll("input, select, textarea").forEach(function (input) {
    input.style.borderColor = "#ddd";
  });
}

function showSuccessMessage(text) {
  let successDiv = document.querySelector(".success-message");
  if (!successDiv) {
    successDiv = document.createElement("div");
    successDiv.className = "success-message";
    const form = document.querySelector("form");
    form.parentNode.insertBefore(successDiv, form);
  }
  successDiv.style.display = "block";
  successDiv.innerText = text || " Form submitted successfully!";
  setTimeout(function () {
    successDiv.style.display = "none";
  }, 3000);
}
