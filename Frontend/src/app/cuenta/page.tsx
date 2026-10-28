"use client";

import { type FormEvent, useEffect, useState } from "react";

import CatalogoHeader from "@/components/CatalogoHeader";
import {
  ApiError,
  cerrarSesion,
  iniciarSesion,
  obtenerSesion,
  registrarse,
  type Sesion,
} from "@/lib/api";

const estiloCampo =
  "w-full rounded border border-linea bg-white p-[0.55rem] font-sans text-base text-tinta focus:border-acento focus:outline-none";

function mensajeDeError(error: unknown) {
  if (error instanceof ApiError) {
    const datos = error.datos as { error?: string } | null;
    if (datos?.error) return datos.error;
  }
  return "No se pudo conectar con la API.";
}

export default function Cuenta() {
  const [sesion, setSesion] = useState<Sesion | null>(null);
  const [email, setEmail] = useState("");
  const [clave, setClave] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [enviando, setEnviando] = useState(false);

  useEffect(() => {
    obtenerSesion().then(setSesion).catch(() => setSesion(null));
  }, []);

  async function enviar(accion: "login" | "registro") {
    setEnviando(true);
    setMensaje("");
    try {
      if (accion === "registro") {
        await registrarse(email, clave);
        setMensaje("Cuenta creada. Ahora inicia sesión.");
      } else {
        await iniciarSesion(email, clave);
        setSesion(await obtenerSesion());
        setClave("");
      }
    } catch (error) {
      setMensaje(mensajeDeError(error));
    }
    setEnviando(false);
  }

  async function salir() {
    await cerrarSesion();
    setSesion(null);
  }

  if (sesion) {
    return (
      <>
        <CatalogoHeader titulo="Mi cuenta" />
        <div className="mx-auto my-8 max-w-[480px] space-y-4 text-center">
          <p>Sesión iniciada con rol <strong>{sesion.rol}</strong>.</p>
          <button type="button" onClick={salir} className="boton">Cerrar sesión</button>
        </div>
      </>
    );
  }

  return (
    <>
      <CatalogoHeader titulo="Cuenta" />
      <form onSubmit={(e: FormEvent<HTMLFormElement>) => { e.preventDefault(); enviar("login"); }} className="mx-auto my-8 max-w-[480px] space-y-[1.1rem]">
        {mensaje && <p className="text-peligro">{mensaje}</p>}
        <div>
          <label htmlFor="email" className="mb-[0.3rem] block text-[0.9rem] text-tinta-suave">Correo</label>
          <input id="email" type="email" required value={email}
            onChange={(e) => setEmail(e.target.value)} className={estiloCampo} />
        </div>
        <div>
          <label htmlFor="clave" className="mb-[0.3rem] block text-[0.9rem] text-tinta-suave">
            Contraseña (mínimo 10 caracteres)
          </label>
          <input id="clave" type="password" required value={clave}
            onChange={(e) => setClave(e.target.value)} className={estiloCampo} />
        </div>
        <div className="flex gap-3">
          <button type="submit" disabled={enviando} className="boton disabled:opacity-60">
            Iniciar sesión
          </button>
          <button type="button" disabled={enviando} className="boton disabled:opacity-60"
            onClick={() => enviar("registro")}>
            Registrarse
          </button>
        </div>
      </form>
    </>
  );
}
