"use client";

import Link from "next/link";
import { type FormEvent, useEffect, useState } from "react";

import { ApiError, crearResena, listarResenas, type Resena } from "@/lib/api";

type Props = {
  libroId: string;
};

export default function Resenas({ libroId }: Props) {
  const [resenas, setResenas] = useState<Resena[] | null>(null);
  const [sinSesion, setSinSesion] = useState(false);
  const [texto, setTexto] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    listarResenas(libroId)
      .then(setResenas)
      .catch((e) => setSinSesion(e instanceof ApiError && e.status === 401));
  }, [libroId]);

  async function enviar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setError("");
    try {
      const nueva = await crearResena(libroId, texto);
      setResenas((actuales) => [nueva, ...(actuales ?? [])]);
      setTexto("");
    } catch {
      setError("No se pudo publicar la reseña.");
    }
  }

  if (sinSesion) {
    return (
      <p className="my-8 text-tinta-suave">
        <Link href="/cuenta" className="underline">Inicia sesión</Link> para escribir reseñas.
      </p>
    );
  }

  return (
    <section className="my-10 text-left">
      <h3 className="mb-4 text-[1.3rem]">Mis reseñas</h3>
      <form onSubmit={enviar} className="mb-6 space-y-3">
        {error && <p className="text-peligro">{error}</p>}
        <textarea id="resena" required maxLength={500} value={texto} rows={3}
          onChange={(e) => setTexto(e.target.value)}
          className="w-full rounded border border-linea bg-white p-[0.55rem] font-sans text-base text-tinta focus:border-acento focus:outline-none" />
        <button type="submit" className="boton">Publicar reseña</button>
      </form>
      {resenas?.map((r) => (
        <article key={r.id} className="border-b border-linea py-3">
          {/* el texto del usuario se muestra como texto: React lo escapa */}
          <p>{r.texto}</p>
          <p className="mt-1 text-[0.8rem] text-tinta-suave">{r.usuario}</p>
        </article>
      ))}
    </section>
  );
}
