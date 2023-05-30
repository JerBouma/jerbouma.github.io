document.addEventListener("DOMContentLoaded", function() {
    const slides = document.querySelectorAll(".testimonial-slide");
    let currentSlide = 0;
    
    function showSlide(index) {
      slides.forEach((slide) => {
        slide.style.display = "none";
      });
      slides[index].style.display = "block";
    }
    
    function nextSlide() {
      currentSlide = (currentSlide + 1) % slides.length;
      showSlide(currentSlide);
    }
    
    function prevSlide() {
      currentSlide = (currentSlide - 1 + slides.length) % slides.length;
      showSlide(currentSlide);
    }
    
    showSlide(currentSlide);
    setInterval(nextSlide, 10000);
    
    const prevBtns = document.querySelectorAll(".carousel-btn-prev");
    const nextBtns = document.querySelectorAll(".carousel-btn-next");
    
    prevBtns.forEach((btn) => {
      btn.addEventListener("click", function(e) {
        e.preventDefault();
        prevSlide();
        resetTimer();
      });
    });
    
    nextBtns.forEach((btn) => {
      btn.addEventListener("click", function(e) {
        e.preventDefault();
        nextSlide();
        resetTimer();
      });
    });
  });
  