let slideIndex = 1;
showSlides(slideIndex)

function plusSlides(n){
    showSlides(slideIndex += n)
}
function currentSlide(n){
    showSlides(slideIndex = n)
}
function showSlides(n){
    let i;
    let slides = document.querySelectorAll(".carrusel");
    let quadrates1 = document.querySelectorAll(".quadrate1"); 
    if(n > slides.length) slideIndex = 1
    if(n < 1) slideIndex = slides.length
    for(i = 0; i < slides.length; i++){
        slides[i].style.display = "none"
    }
    for(i = 0; i < quadrates1.length;i++){
        quadrates1[i].className = quadrates1[i].className.replace("active","")
    }
    slides[slideIndex-1].style.display = "block";
    quadrates1[slideIndex-1].className += " active";
}