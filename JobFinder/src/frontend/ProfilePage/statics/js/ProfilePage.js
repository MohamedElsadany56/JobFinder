document.addEventListener("DOMContentLoaded", () => {
  const dropDownMenus = document.querySelectorAll(".drop-down select");

  dropDownMenus.forEach((dropDown) => {
    dropDown.addEventListener("change", (e) => {
      const jobContainer = e.target.closest(".job");
      const statusElement = jobContainer.querySelector(".status");

      const selectedValue = e.target.value;

      statusElement.textContent = selectedValue;

      statusElement.classList.remove("pending", "working-on", "done");

      statusElement.classList.add(selectedValue);
    });
  });
});
