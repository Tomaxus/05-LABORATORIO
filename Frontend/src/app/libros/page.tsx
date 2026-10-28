"use client";

import Link from "next/link";

import CatalogoHeader from "@/components/CatalogoHeader";
import { Cargando, ErrorApi } from "@/components/Estado";
import LibroCard from "@/components/LibroCard";
import { listarLibros } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export default function Listado() {
  const libros = useApi(listarLibros);

  return (
    <>
      <title>Catálogo | Biblioteca Paulo Coelho</title>
      <CatalogoHeader
        titulo="Catálogo"
        accion={<Link href="/libros/nuevo" className="boton">+ Nuevo libro</Link>}
      />

      {libros.estado === "cargando" && <Cargando />}
      {libros.estado === "error" && <ErrorApi error={libros.error} />}
      {libros.estado === "listo" && (
        <section className="flex flex-wrap gap-x-8 gap-y-10 pt-4">
          {libros.datos.map((libro) => (
            <LibroCard
              key={libro.id}
              href={`/libros/${libro.id}`}
              titulo={libro.titulo}
              imagen={libro.imagen}
              meta={`${libro.anio} · ${libro.editorial.nombre}`}
            />
          ))}
        </section>
      )}
    </>
  );
}
