document.addEventListener("DOMContentLoaded", function() {
  const slides = Array.from(document.querySelectorAll(".testimonial-slide")); // Convert NodeList to an array
  let currentSlide = 0;
  let timer;

  function showSlide(index) {
    slides.forEach((slide) => {
      slide.style.display = "none";
    });
    slides[index].style.display = "block";
  }

  function shuffleSlides() {
    for (let i = slides.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [slides[i], slides[j]] = [slides[j], slides[i]]; // Swap elements to shuffle
    }
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
    resetTimer();
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
    resetTimer();
  }

  function resetTimer() {
    clearInterval(timer);
    timer = setInterval(nextSlide, 10000);
  }

  shuffleSlides(); // Randomize the order of slides initially
  showSlide(currentSlide);
  resetTimer();

  const prevBtns = document.querySelectorAll(".carousel-btn-prev");
  const nextBtns = document.querySelectorAll(".carousel-btn-next");

  prevBtns.forEach((btn) => {
    btn.addEventListener("click", function(e) {
      e.preventDefault();
      prevSlide();
    });
  });

  nextBtns.forEach((btn) => {
    btn.addEventListener("click", function(e) {
      e.preventDefault();
      nextSlide();
    });
  });
});
