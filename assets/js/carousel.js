document.addEventListener("DOMContentLoaded", function() {
  const slides = document.querySelectorAll(".testimonial-slide");
  let currentSlide = 0;
  let timer;
  
  function showSlide(index) {
    slides.forEach((slide) => {
      slide.style.display = "none";
    });
    slides[index].style.display = "block";
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
  
  showSlide(currentSlide);
  resetTimer();
  
  const prevBtns = document.querySelectorAll(".carousel-btn-prev");
  const nextBtns = document.querySelectorAll(".carousel-btn-next");
  const testimonialSlider = document.querySelector(".testimonial-slider");
  
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
