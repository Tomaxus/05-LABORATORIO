import Link from "next/link";

import Portada from "@/components/Portada";

type Props = {
  href: string;
  titulo: string;
  meta: string;
  imagen?: string;
};

export default function LibroCard({ href, titulo, meta, imagen }: Props) {
  return (
    <article className="flex-[1_1_250px] border-t border-linea pt-5">
      <Link href={href} className="group block text-inherit">
        {imagen && (
          <Portada
            src={imagen}
            titulo={titulo}
            className="mb-[0.9rem] w-full transition-colors group-hover:bg-acento"
          />
        )}
        <h2 className="mb-[0.4rem] text-[1.15rem] text-tinta group-hover:text-acento">{titulo}</h2>
        <p className="text-[0.9rem] text-tinta-suave">{meta}</p>
      </Link>
    </article>
  );
}
