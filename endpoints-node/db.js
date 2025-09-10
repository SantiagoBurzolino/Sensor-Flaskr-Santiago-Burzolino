import mysql from "mysql2/promise";
import Dotenv from "dotenv";

Dotenv.config(); // carga las variables del entorno

//configuracion de la conexión
const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER, // De esta forma lo encriptamos
  password: process.env.DB_PASSWORD, // los datos sensibles(contraseña, datos personales y demas)
  database: process.env.DB_NAME,
  waitForConnections: true, // La propiedad que espera a que haya una conexion disponible.
  connectionLimit: 10, // La maxima cantidad de personas la cual se pueden conectar.
  queueLimit: 0, // La cantidad maxima de personas que pueden esperar para conectarse.
});

export default pool;
