import type { ReactNode } from "react";

type Props = {
  titulo: string;
  accion?: ReactNode;
};

export default function CatalogoHeader({ titulo, accion }: Props) {
  return (
    <div className="relative pt-10 pb-4 text-center">
      <h2 className="mb-[0.4rem] text-[1.8rem]">{titulo}</h2>
      {accion && <div className="mt-3 sm:absolute sm:top-10 sm:right-0 sm:mt-0">{accion}</div>}
    </div>
  );
}
