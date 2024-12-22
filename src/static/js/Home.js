// script.js

// Add interactivity to "Find a Job" button
document.querySelector('.cta-buttons button').addEventListener('click', () => {
  alert('Feature coming soon!');
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    document.querySelector(this.getAttribute('href')).scrollIntoView({
      behavior: 'smooth',
    });
  });
});
