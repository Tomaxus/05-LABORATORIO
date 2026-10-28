"use client";

import { useParams, useRouter } from "next/navigation";

import { Cargando, ErrorApi } from "@/components/Estado";
import FormularioLibro from "@/components/FormularioLibro";
import { editarLibro, obtenerLibro } from "@/lib/api";
import { useApi } from "@/lib/useApi";

export default function Editar() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const resultado = useApi(() => obtenerLibro(id), id);

  if (resultado.estado === "cargando") return <Cargando />;
  if (resultado.estado === "error") return <ErrorApi error={resultado.error} />;

  return (
    <FormularioLibro
      tituloPagina="Editar libro"
      inicial={resultado.datos}
      onGuardar={async (datos) => {
        await editarLibro(id, datos);
        router.push(`/libros/${id}`);
      }}
    />
  );
}
