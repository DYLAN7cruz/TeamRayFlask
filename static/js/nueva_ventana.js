const comentariosForm = document.querySelector("#comentarios");

let users = [];
let editing = false;
let userId = null;

window.addEventListener("DOMContentLoaded", async () => {
    const response = await fetch("/api/comentarios");
    const data = await response.json();
    users = data;
    renderUser(users);
});

comentariosForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nombre = comentariosForm["nombre"].value;
    const apellido = comentariosForm["apellido"].value;
    const descripcion = comentariosForm["descripcion"].value;

    if (!editing) {

        const response = await fetch("/api/comentarios", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                nombre,
                apellido,
                descripcion,
            }),
        });

        const data = await response.json();
        users.push(data);
        renderUser(users);
    } else {
        const response = await fetch(`/api/comentarios/${userId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                nombre,
                apellido,
                descripcion,
            }),
        });
        const updatedUser = await response.json();

        users = users.map((user) =>
            user.id === updatedUser.id ? updatedUser : user
        );
        console.log(users)
        renderUser(users);

        editing = false;
        userId = null;
    }
    comentariosForm.reset();
});

function renderUser(users) {
    const userList = document.querySelector("#userList");
    userList.innerHTML = "";
    users.forEach((user) => {
        const userItem = document.createElement("table");

        userItem.innerHTML = `

        <tr class="fila">
        
        <th class="fila1">NOMBRE</th>
        <th class="fila1">APELLIDO</th>
        <th class="fila1">COMENTARIO</th>
        
        <th class="fila1">ELIMINAR</th>
        <th class="fila1">ACTUALIZAR</th>
    
    </tr>
       
        <tr class="columna">
    
    <td class="columna1"> ${user.nombre}</td>     
    <td class="columna1"> ${user.apellido}</td>
    <td class="columna1">${user.descripcion}</td>
    
    <td class="columna1"><button data-id="${user.id}" class="boton2 btn-delete btn btn-danger btn-sm ">ELIMINAR</button></td>
    <td class="columna1"><button data-id="${user.id}" class="boton2 btn-edit btn btn-secondary btn-sm ">ACTUALIZAR</button></td>
      
    </tr>
  
`;

        // ELIMINAR
        const btnDelete = userItem.querySelector(".btn-delete");

        btnDelete.addEventListener("click", async (e) => {
            const response = await fetch(`/api/comentarios/${user.id}`, {
                method: "DELETE",
            });

            const data = await response.json();

            users = users.filter((user) => user.id !== data.id);
            renderUser(users);
        });

        userList.appendChild(userItem);


        const btnEdit = userItem.querySelector(".btn-edit");

        btnEdit.addEventListener("click", async (e) => {
            const response = await fetch(`/api/comentarios/${user.id}`);
            const data = await response.json();

            comentariosForm["nombre"].value = data.nombre;
            comentariosForm["apellido"].value = data.apellido;
            comentariosForm["descripcion"].value = data.descripcion;

            editing = true;
            userId = user.id;
        });
    });
}