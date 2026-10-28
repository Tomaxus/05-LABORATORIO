import Link from "next/link";

type Props = {
  titulo?: string;
  mensaje?: string;
};

export default function NoEncontrado({
  titulo = "Libro no encontrado",
  mensaje = "No existe ningún libro con ese id",
}: Props) {
  return (
    <article className="mx-auto mt-12 max-w-[400px] text-center">
      <title>{`${titulo} | Biblioteca Paulo Coelho`}</title>
      <h2 className="text-2xl">{titulo}</h2>
      <p className="mt-2 mb-6 text-tinta-suave">{mensaje}</p>
      <Link href="/libros" className="text-acento hover:underline">
        &larr; Volver al catálogo
      </Link>
    </article>
  );
}
