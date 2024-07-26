
    //CREAMOS UNA FUNCION CON EL EVENTO SCROLL
    window.addEventListener("scroll", function () {
      var header = document.querySelector("header");
      header.classList.toggle('down', window.scrollY > 0);



    });

    //RESPONSIVE DEL MENU
    var menu = document.querySelector('.menu');
    var menuBtn = document.querySelector('.menu-btn');
    var closeBtn = document.querySelector('.close-btn');

    menuBtn.addEventListener("click", () => {
      menu.classList.add('active');
    });

    closeBtn.addEventListener("click", () => {
      menu.classList.remove('active');
    });
