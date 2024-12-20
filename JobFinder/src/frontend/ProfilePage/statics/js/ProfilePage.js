document.addEventListener("DOMContentLoaded", () => {
  // Existing status dropdown code
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

  // Add show/hide applicants functionality
  const showApplicantsButtons = document.querySelectorAll(
    ".show-applicants button"
  );
  showApplicantsButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      const applicantsList = e.target.closest(".job").nextElementSibling;
      const isVisible = applicantsList.classList.contains("visible");

      applicantsList.classList.toggle("visible");

      button.textContent = isVisible ? "Show Applicants" : "Hide Applicants";
    });
  });
});
