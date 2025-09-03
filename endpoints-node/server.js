import express from "express";

const app = express();
const PORT = 5000;

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Este es un endpoint hecho con express");
});

//endpoint con parametro

app.get("/api/user/:id", (req, res) => {
  //destructuracion
  const { id } = req.params;
  res.send({ message: `El usuario con id ${id} es pepito` });
});

app.get("/api/search", (req, res) => {
  const { name, lastname } = req.query;
  res.json({
    firstName: name,
    lastname,
  });
  // http://localhost:PUERTO/api/search?name=Santiago&lastname=Burzolino
});

//endpoint POST
app.post("/api/user", (req, res) => {
  const { name, email } = req.body;
  res.json({ message: "Usuario Creado", data: { name, email } });
});

//iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en el puerto ${PORT}`);
});
