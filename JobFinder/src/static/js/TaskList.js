document.addEventListener("DOMContentLoaded", () => {
  const keywordInput = document.getElementById("keyword");
  const locationSelect = document.getElementById("location");
  const categorySelect = document.getElementById("category");
  const experienceSelect = document.getElementById("experience");
  const jobTypeSelect = document.getElementById("job-type");
  const qualificationSelect = document.getElementById("qualification");
  const genderSelect = document.getElementById("gender");
  const jobList = document.querySelector(".job-list ul");

  const filterJobs = () => {
    const keyword = keywordInput.value.toLowerCase();
    const location = locationSelect.value;
    const category = categorySelect.value;
    const experience = experienceSelect.value;
    const jobType = jobTypeSelect.value;
    const qualification = qualificationSelect.value;
    const gender = genderSelect.value;

    const jobs = jobList.querySelectorAll(".list-item");
    jobs.forEach((job) => {
      const jobTitle = job.querySelector("h2").textContent.toLowerCase();
      const jobLocation = job.querySelector(".location p").textContent;
      const jobCategory = job.dataset.category;
      const jobExperience = job.dataset.experience;
      const jobTypeData = job.dataset.jobType;
      const jobQualification = job.dataset.qualification;
      const jobGender = job.dataset.gender;

      const matchesKeyword = jobTitle.includes(keyword);
      const matchesLocation = !location || jobLocation.includes(location);
      const matchesCategory = !category || jobCategory === category;
      const matchesExperience = !experience || jobExperience === experience;
      const matchesJobType = !jobType || jobTypeData === jobType;
      const matchesQualification =
        !qualification || jobQualification === qualification;
      const matchesGender = !gender || jobGender === gender;

      if (
        matchesKeyword &&
        matchesLocation &&
        matchesCategory &&
        matchesExperience &&
        matchesJobType &&
        matchesQualification &&
        matchesGender
      ) {
        job.style.display = "";
      } else {
        job.style.display = "none";
      }
    });
  };

  keywordInput.addEventListener("input", filterJobs);
  locationSelect.addEventListener("change", filterJobs);
  categorySelect.addEventListener("change", filterJobs);
  experienceSelect.addEventListener("change", filterJobs);
  jobTypeSelect.addEventListener("change", filterJobs);
  qualificationSelect.addEventListener("change", filterJobs);
  genderSelect.addEventListener("change", filterJobs);
});
