"use client";

import CatalogoHeader from "@/components/CatalogoHeader";
import { Cargando, ErrorApi } from "@/components/Estado";
import LibroCard from "@/components/LibroCard";
import { listarEditoriales } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export default function ListadoEditoriales() {
  const editoriales = useApi(listarEditoriales);

  return (
    <>
      <title>Editoriales | Biblioteca Paulo Coelho</title>
      <CatalogoHeader titulo="Editoriales" />

      {editoriales.estado === "cargando" && <Cargando />}
      {editoriales.estado === "error" && <ErrorApi error={editoriales.error} />}
      {editoriales.estado === "listo" && (
        <section className="flex flex-wrap gap-x-8 gap-y-10 pt-4">
          {editoriales.datos.map((editorial) => (
            <LibroCard
              key={editorial.id}
              href={`/libros/editoriales/${editorial.id}`}
              titulo={editorial.nombre}
              meta={editorial.pais}
            />
          ))}
        </section>
      )}
    </>
  );
}
