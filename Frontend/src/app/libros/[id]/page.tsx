"use client";

import Link from "next/link";
import { useParams } from "next/navigation";

import { Cargando, ErrorApi } from "@/components/Estado";
import Ficha from "@/components/Ficha";
import Portada from "@/components/Portada";
import Resenas from "@/components/Resenas";
import { obtenerLibro } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export default function Detalle() {
  const { id } = useParams<{ id: string }>();
  const resultado = useApi(() => obtenerLibro(id), id);

  if (resultado.estado === "cargando") return <Cargando />;
  if (resultado.estado === "error") return <ErrorApi error={resultado.error} />;

  const libro = resultado.datos;
  const rapida = libro.paginas < 250;

  return (
    <article className="mx-auto mt-8 max-w-[480px] text-center">
      <title>{`${libro.titulo} | Biblioteca Paulo Coelho`}</title>
      <Portada src={libro.imagen} titulo={libro.titulo} className="mx-auto mb-6 w-[220px]" />
      <h2 className="mb-4 text-[2rem]">{libro.titulo}</h2>

      <p className="inline-block rounded-[3px] bg-acento-suave px-[0.8rem] py-1 text-[0.85rem] text-acento">
        {rapida ? "Lectura rápida" : "Lectura extensa"}
      </p>

      <Ficha
        filas={[
          ["Año", libro.anio],
          ["Páginas", libro.paginas],
          ["Editorial", libro.editorial.nombre],
          ["País", libro.editorial.pais],
        ]}
      />

      <div className="mb-6 flex justify-center gap-3">
        <Link href={`/libros/${libro.id}/editar`} className="boton">Editar</Link>
        <Link href={`/libros/${libro.id}/eliminar`} className="boton boton-peligro">Eliminar</Link>
      </div>

      <Resenas libroId={libro.id} />

      <Link href="/libros" className="volver">&larr; Volver al catálogo</Link>
    </article>
  );
}
