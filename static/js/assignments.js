document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".assignment-card");

  // ===============================
  // 1. ENTRY ANIMATION (smooth load)
  // ===============================
  cards.forEach((card, i) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";

    setTimeout(() => {
      card.style.transition = "all 0.5s ease";
      card.style.opacity = "1";
      card.style.transform = "translateY(0)";
    }, i * 80);
  });

  // ===============================
  // 2. BUTTON CLICK FEEDBACK
  // ===============================
  document.querySelectorAll(".assignment-actions button").forEach(btn => {
    btn.addEventListener("click", (e) => {
      btn.style.transform = "scale(0.95)";
      setTimeout(() => {
        btn.style.transform = "scale(1)";
      }, 150);
    });
  });

  // ===============================
  // 3. OVERDUE HIGHLIGHT PULSE
  // ===============================
  document.querySelectorAll(".status-pill.overdue").forEach(el => {
    setInterval(() => {
      el.style.boxShadow = "0 0 10px rgba(255, 107, 107, 0.4)";
      setTimeout(() => {
        el.style.boxShadow = "none";
      }, 600);
    }, 1500);
  });

  // ===============================
  // 4. FILTER SYSTEM (VISUAL ONLY)
  // ===============================
  const filters = document.querySelectorAll(".filter");
  const assignmentCards = document.querySelectorAll(".assignment-card");

  filters.forEach(filter => {
    filter.addEventListener("click", () => {

      filters.forEach(f => f.classList.remove("active"));
      filter.classList.add("active");

      const type = filter.textContent.toLowerCase();

      assignmentCards.forEach(card => {
        const status = card.querySelector(".status-pill")?.textContent.toLowerCase();

        if (type === "all") {
          card.style.display = "flex";
        }
        else if (type === "done" && status.includes("completed")) {
          card.style.display = "flex";
        }
        else if (type === "pending" && status.includes("pending")) {
          card.style.display = "flex";
        }
        else {
          card.style.display = "none";
        }
      });
    });
  });

});