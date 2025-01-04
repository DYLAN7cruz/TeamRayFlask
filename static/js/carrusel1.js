let slideIndex1 = 1;
showSlidess(slideIndex1)

function plusSlides1(n){
    showSlidess(slideIndex1 += n)
}
function currentSlide1(n){
    showSlidess(slideIndex1 = n)
}
function showSlidess(n){
    let i;
    let slides1 = document.querySelectorAll(".carrusel1");
    let quadrates1 = document.querySelectorAll(".quadrate1"); 
    if(n > slides1.length) slideIndex1 = 1
    if(n < 1) slideIndex1 = slides1.length
    for(i = 0; i < slides1.length; i++){
        slides1[i].style.display = "none"
    }
    for(i = 0; i < quadrates1.length;i++){
        quadrates1[i].className = quadrates1[i].className.replace("active","")
    }
    slides1[slideIndex1-1].style.display = "block";
    // quadrates1[slideIndex1-1].className += " active";
}