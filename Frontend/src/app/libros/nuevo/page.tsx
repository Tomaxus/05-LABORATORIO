"use client";

import { useRouter } from "next/navigation";

import FormularioLibro from "@/components/FormularioLibro";
import { crearLibro } from "@/lib/api";

export default function Crear() {
  const router = useRouter();

  return (
    <FormularioLibro
      tituloPagina="Nuevo libro"
      onGuardar={async (datos) => {
        await crearLibro(datos);
        router.push("/libros");
      }}
    />
  );
}
