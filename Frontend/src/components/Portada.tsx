import Image from "next/image";

import { rutaImagen } from "@/lib/api";

type Props = {
  src: string;
  titulo: string;
  className?: string;
};

export default function Portada({ src, titulo, className = "" }: Props) {
  return (
    <Image
      src={rutaImagen(src)}
      alt={`Portada de ${titulo}`}
      width={400}
      height={600}
      unoptimized
      className={`aspect-2/3 rounded bg-acento-suave object-cover ${className}`}
    />
  );
}
