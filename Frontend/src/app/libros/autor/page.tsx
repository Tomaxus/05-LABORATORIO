import type { Metadata } from "next";
import Image from "next/image";

export const metadata: Metadata = {
  title: "Sobre el autor | Biblioteca Paulo Coelho",
};

export default function Autor() {
  return (
    <article className="flex items-start gap-10 pt-8 max-sm:flex-col max-sm:items-center max-sm:text-center">
      <Image
        src="/img/paulo.jpg"
        width={440}
        height={587}
        alt="Retrato de Paulo Coelho"
        preload
        className="aspect-3/4 w-[220px] shrink-0 rounded bg-acento-suave object-cover"
      />

      <div>
        <h2 className="mb-[0.3rem] text-[2rem]">Paulo Coelho</h2>
        <p className="mb-5 text-[0.9rem] text-acento">Río de Janeiro, Brasil &middot; 24 de agosto de 1947</p>

        <p className="mb-4">
          Paulo Coelho es un escritor brasileño, uno de los autores más leídos del mundo.
          Antes de dedicarse por completo a la literatura trabajó como letrista de canciones
          y periodista, y recorrió gran parte del mundo en busca de las experiencias que
          más tarde darían forma a sus historias.
        </p>
        <p className="mb-4">
          Su obra más conocida, <em>El Alquimista</em> (1988), se ha traducido a más de
          ochenta idiomas y es una de las novelas más vendidas de la historia. A lo largo
          de su carrera ha explorado temas como la búsqueda personal, la espiritualidad y
          el destino, con un estilo sencillo y cercano al lector.
        </p>
        <p className="mb-4">
          En 2002 fue elegido miembro de la Academia Brasileña de Letras, reconocimiento
          a una trayectoria que combina la narrativa con reflexiones sobre el camino que
          cada persona recorre para encontrar su propia leyenda personal.
        </p>
      </div>
    </article>
  );
}
