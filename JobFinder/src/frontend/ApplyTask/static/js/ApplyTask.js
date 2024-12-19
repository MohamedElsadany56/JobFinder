let Employer = document.querySelector(".main-body .form ul .Employer");
let candidate = document.querySelector(".main-body .form ul .Candidate");
let isEmployerClicked = false;
let isCandidateClicked = false;
let disabilityDescription = document.querySelector("#Jop");

Employer.addEventListener("click", () => {
  if (!isEmployerClicked) {
    // Mark Employer as active and Candidate as inactive
    Employer.classList.add("active");
    candidate.classList.remove("active");
    isEmployerClicked = true;
    isCandidateClicked = false;
    disabilityDescription.classList.add("show"); // Add animation class
    disabilityDescription.style.display = "block"; // Show textarea
  } else {
    // Toggle Employer off if clicked again
    Employer.classList.remove("active");
    isEmployerClicked = false;
    disabilityDescription.classList.remove("show"); // Remove animation class
    disabilityDescription.style.display = "none"; // Hide textarea
  }
});

candidate.addEventListener("click", () => {
  if (!isCandidateClicked) {
    candidate.classList.add("active");
    Employer.classList.remove("active");
    isCandidateClicked = true;
    isEmployerClicked = false;
    disabilityDescription.classList.remove("show"); // Remove animation class
    disabilityDescription.style.display = "none"; // Hide textarea
  } else {
    candidate.classList.remove("active");
    isCandidateClicked = false;
  }
});
