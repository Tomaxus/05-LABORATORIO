"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { Cargando, ErrorApi } from "@/components/Estado";
import Ficha from "@/components/Ficha";
import LibroCard from "@/components/LibroCard";
import { obtenerEditorial } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export default function DetalleEditorial() {
  const { id } = useParams<{ id: string }>();
  const resultado = useApi(() => obtenerEditorial(id), id);

  if (resultado.estado === "cargando") return <Cargando />;
  if (resultado.estado === "error") {
    return (
      <ErrorApi
        error={resultado.error}
        tituloNoEncontrado="Editorial no encontrada"
        mensajeNoEncontrado="No existe ninguna editorial con ese id"
      />
    );
  }

  const editorial = resultado.datos;

  return (
    <article className="mx-auto mt-8 text-center">
      <title>{`${editorial.nombre} | Biblioteca Paulo Coelho`}</title>
      <h2 className="mb-4 text-[2rem]">{editorial.nombre}</h2>

      <div className="mx-auto max-w-[480px]">
        <Ficha filas={[["País", editorial.pais]]} />
      </div>

      <h3 className="text-lg font-bold">Libros publicados</h3>
      <section className="flex flex-wrap gap-x-8 gap-y-10 pt-4 pb-8 text-left">
        {editorial.libros.length === 0 ? (
          <p>Esta editorial todavía no tiene libros registrados.</p>
        ) : (
          editorial.libros.map((libro) => (
            <LibroCard
              key={libro.id}
              href={`/libros/${libro.id}`}
              titulo={libro.titulo}
              imagen={libro.imagen}
              meta={String(libro.anio)}
            />
          ))
        )}
      </section>

      <Link href="/libros/editoriales" className="volver">&larr; Volver a editoriales</Link>
    </article>
  );
}
