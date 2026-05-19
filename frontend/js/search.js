window.onload = function () {
  const searchForm = document.querySelector("form");
  if (searchForm) {
    searchForm.addEventListener("submit", (event) => {
      const query = document.getElementById("searchQuery").value.trim();
      const category = document.getElementById("category").value;
      if (query === "" && category === "") {
        event.preventDefault();
        alert("Please fill any field before searching!");
      }
    });
  }
};
