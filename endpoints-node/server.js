import express from "express";
import pool from "./db.js";

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

//PUT
app.put("/api/user/:id", (req, res) => {
  const { id } = req.params;
  const { name, email } = req.body;
  res.json({
    message: `Este es el usuario con id ${id}`,
    data: { name, email },
  });
});

//delete

app.delete("/api/user/:id", (req, res) => {
  const { id } = req.params;
  res.json({ message: `Usuario con ID ${id} eliminado` });
});

//endpoint conexion a db
//GET

app.get("/api/inventario", async (req, res) => {
  try {
    // codigo a probar
    const [rows] = await pool.query("SELECT * FROM inventario");
    res.json(rows);
  } catch (error) {
    console.log(error);
    res.status(500).json({ error: "Error en la consulta" });
  }
});

//iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en el puerto ${PORT}`);
});
