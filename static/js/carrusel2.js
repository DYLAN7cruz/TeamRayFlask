let slideIndex2 = 1;
showSlidesss(slideIndex2)

function plusSlides2(n){
    showSlidesss(slideIndex2 += n)
}
function currentSlide2(n){
    showSlidesss(slideIndex2 = n)
}
function showSlidesss(n){
    let i;
    let slides2 = document.querySelectorAll(".carrusel2");
    let quadrates1 = document.querySelectorAll(".quadrate1"); 
    if(n > slides2.length) slideIndex2 = 1
    if(n < 1) slideIndex2 = slides2.length
    for(i = 0; i < slides2.length; i++){
        slides2[i].style.display = "none"
    }
    for(i = 0; i < quadrates1.length;i++){
        quadrates1[i].className = quadrates1[i].className.replace("active","")
    }
    slides2[slideIndex2-1].style.display = "block";
    // quadrates1[slideIndex2-1].className += " active";
}

