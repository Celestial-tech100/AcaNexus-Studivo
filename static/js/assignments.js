document.addEventListener("DOMContentLoaded", () => {

  console.log("AcaNexus loaded");

  const cards = document.querySelectorAll(".assignment-card");
  const filters = document.querySelectorAll(".filter");

  // animation
  cards.forEach((card, i) => {
    card.style.opacity = 0;
    card.style.transform = "translateY(15px)";

    setTimeout(() => {
      card.style.transition = "0.4s ease";
      card.style.opacity = 1;
      card.style.transform = "translateY(0)";
    }, i * 60);
  });

  // filter
  filters.forEach(filter => {
    filter.addEventListener("click", () => {

      filters.forEach(f => f.classList.remove("active"));
      filter.classList.add("active");

      const type = filter.textContent.toLowerCase();

      document.querySelectorAll(".assignment-card").forEach(card => {
        const status = card.dataset.status;

        if (type === "all") card.style.display = "flex";
        else if (type === "done") card.style.display = status === "completed" ? "flex" : "none";
        else if (type === "pending") card.style.display = status === "pending" ? "flex" : "none";
      });

    });
  });

});
