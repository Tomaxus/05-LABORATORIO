"use client";

import Link from "next/link";
import { useState, type FormEvent, type ReactNode } from "react";

import CatalogoHeader from "@/components/CatalogoHeader";
import { Cargando, ErrorApi } from "@/components/Estado";
import { ApiError, listarEditoriales, type DatosLibro, type ErroresCampos, type Libro } from "@/lib/api";
import { useApi } from "@/lib/useApi";

type Props = {
  tituloPagina: string;
  inicial?: Libro;
  onGuardar: (datos: DatosLibro) => Promise<void>;
};

type Campo = keyof DatosLibro;

const estiloCampo =
  "w-full rounded border border-linea bg-white p-[0.55rem] font-sans text-base text-tinta focus:border-acento focus:outline-none";

export default function FormularioLibro({ tituloPagina, inicial, onGuardar }: Props) {
  const editoriales = useApi(listarEditoriales);
  const [datos, setDatos] = useState<Record<Campo, string>>({
    titulo: inicial?.titulo ?? "",
    anio: inicial ? String(inicial.anio) : "",
    paginas: inicial ? String(inicial.paginas) : "",
    imagen: inicial?.imagen ?? "",
    editorial_id: inicial?.editorial.id ?? "",
  });
  const [errores, setErrores] = useState<ErroresCampos>({});
  const [enviando, setEnviando] = useState(false);

  function cambiar(campo: Campo, valor: string) {
    setDatos((actuales) => ({ ...actuales, [campo]: valor }));
  }

  async function enviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setEnviando(true);
    setErrores({});
    try {
      await onGuardar({ ...datos, anio: Number(datos.anio), paginas: Number(datos.paginas) });
    } catch (error) {
      if (error instanceof ApiError && error.status === 400 && error.datos) {
        setErrores(error.datos as ErroresCampos);
      } else if (error instanceof ApiError && error.status === 401) {
        setErrores({ general: ["Debes iniciar sesión para guardar."] });
      } else if (error instanceof ApiError && error.status === 403) {
        setErrores({ general: ["Solo un administrador puede guardar libros."] });
      } else {
        setErrores({ general: ["No se pudo guardar. Revisa que la API esté corriendo."] });
      }
      setEnviando(false);
    }
  }

  if (editoriales.estado === "cargando") return <Cargando />;
  if (editoriales.estado === "error") return <ErrorApi error={editoriales.error} />;

  const campo = (id: Campo, etiqueta: string, control: ReactNode) => (
    <p>
      <label htmlFor={id} className="mb-[0.3rem] block text-[0.9rem] text-tinta-suave">{etiqueta}</label>
      {control}
      {errores[id]?.map((mensaje) => (
        <span key={mensaje} className="mt-1 block text-[0.85rem] text-peligro">{mensaje}</span>
      ))}
    </p>
  );

  return (
    <>
      <title>{`${tituloPagina} | Biblioteca Paulo Coelho`}</title>
      <CatalogoHeader titulo={tituloPagina} />

      <form onSubmit={enviar} className="mx-auto my-8 max-w-[480px] space-y-[1.1rem]">
        {errores.general && <p className="text-peligro">{errores.general[0]}</p>}

        {campo("titulo", "Título:",
          <input id="titulo" required maxLength={200} value={datos.titulo}
            onChange={(e) => cambiar("titulo", e.target.value)} className={estiloCampo} />)}
        {campo("anio", "Año:",
          <input id="anio" type="number" required min={0} value={datos.anio}
            onChange={(e) => cambiar("anio", e.target.value)} className={estiloCampo} />)}
        {campo("paginas", "Páginas:",
          <input id="paginas" type="number" required min={0} value={datos.paginas}
            onChange={(e) => cambiar("paginas", e.target.value)} className={estiloCampo} />)}
        {campo("imagen", "Imagen:",
          <input id="imagen" required maxLength={200} placeholder="img/1.jpg" value={datos.imagen}
            onChange={(e) => cambiar("imagen", e.target.value)} className={estiloCampo} />)}
        {campo("editorial_id", "Editorial:",
          <select id="editorial_id" required value={datos.editorial_id}
            onChange={(e) => cambiar("editorial_id", e.target.value)} className={estiloCampo}>
            <option value="">---------</option>
            {editoriales.datos.map((editorial) => (
              <option key={editorial.id} value={editorial.id}>
                {editorial.nombre} ({editorial.pais})
              </option>
            ))}
          </select>)}

        <button type="submit" disabled={enviando} className="boton mt-2 disabled:opacity-60">
          {enviando ? "Guardando…" : "Guardar"}
        </button>
      </form>

      <Link href="/libros" className="volver">&larr; Volver al catálogo</Link>
    </>
  );
}
