import { ApiError } from "@/lib/api";
import NoEncontrado from "@/components/NoEncontrado";

export function Cargando() {
  return <p className="pt-16 text-center text-tinta-suave">Cargando…</p>;
}

type ErrorProps = {
  error: unknown;
  tituloNoEncontrado?: string;
  mensajeNoEncontrado?: string;
};

export function ErrorApi({ error, tituloNoEncontrado, mensajeNoEncontrado }: ErrorProps) {
  if (error instanceof ApiError && error.noEncontrado) {
    return <NoEncontrado titulo={tituloNoEncontrado} mensaje={mensajeNoEncontrado} />;
  }

  return (
    <article className="mx-auto mt-12 max-w-[440px] text-center">
      <h2 className="text-2xl">No se pudo cargar la información</h2>
      <p className="mt-2 text-tinta-suave">
        Revisa que la API del lab 03 esté corriendo en <code>http://127.0.0.1:8000</code>.
      </p>
    </article>
  );
}
