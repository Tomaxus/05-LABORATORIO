"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";

import { Cargando, ErrorApi } from "@/components/Estado";
import { eliminarLibro, obtenerLibro } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export default function Eliminar() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const resultado = useApi(() => obtenerLibro(id), id);
  const [eliminando, setEliminando] = useState(false);
  const [fallo, setFallo] = useState(false);

  if (resultado.estado === "cargando") return <Cargando />;
  if (resultado.estado === "error") return <ErrorApi error={resultado.error} />;

  const libro = resultado.datos;

  async function confirmar() {
    setEliminando(true);
    setFallo(false);
    try {
      await eliminarLibro(id);
      router.push("/libros");
    } catch {
      setFallo(true);
      setEliminando(false);
    }
  }

  return (
    <div className="mx-auto mt-8 max-w-[480px] text-center">
      <title>{`Eliminar ${libro.titulo} | Biblioteca Paulo Coelho`}</title>
      <h2 className="mb-4 text-[2rem]">¿Eliminar &quot;{libro.titulo}&quot;?</h2>
      <p className="mb-6">Esta acción no se puede deshacer.</p>
      {fallo && <p className="mb-4 text-peligro">No se pudo eliminar el libro. Inténtalo de nuevo.</p>}

      <button type="button" onClick={confirmar} disabled={eliminando}
        className="boton boton-peligro mb-6 disabled:opacity-60">
        {eliminando ? "Eliminando…" : "Sí, eliminar"}
      </button>

      <div>
        <Link href={`/libros/${libro.id}`} className="volver">&larr; Cancelar</Link>
      </div>
    </div>
  );
}
