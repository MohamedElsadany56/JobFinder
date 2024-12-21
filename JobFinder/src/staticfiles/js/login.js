let Employer = document.querySelector(".main-body .form ul .Employer");
let candidate = document.querySelector(".main-body .form ul .Candidate");
let isEmployerClicked = false;
let isCandidateClicked = false;

Employer.addEventListener("click", () => {
  if (!isEmployerClicked) {
    // Mark Employer as active and Candidate as inactive
    Employer.classList.add("active");
    candidate.classList.remove("active");
    isEmployerClicked = true;
    isCandidateClicked = false;
  } else {
    // Toggle Employer off if clicked again
    Employer.classList.remove("active");
    isEmployerClicked = false;
  }
});

candidate.addEventListener("click", () => {
  if (!isCandidateClicked) {
    candidate.classList.add("active");
    Employer.classList.remove("active");
    isCandidateClicked = true;
    isEmployerClicked = false;
  } else {
    candidate.classList.remove("active");
    isCandidateClicked = false;
  }
});
