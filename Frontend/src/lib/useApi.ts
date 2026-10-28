"use client";

import { useEffect, useState } from "react";

type Estado<T> =
  | { estado: "cargando" }
  | { estado: "listo"; datos: T }
  | { estado: "error"; error: unknown };

export function useApi<T>(consulta: () => Promise<T>, clave = ""): Estado<T> {
  const [resultado, setResultado] = useState<Estado<T>>({ estado: "cargando" });

  useEffect(() => {
    let vigente = true;
    consulta()
      .then((datos) => vigente && setResultado({ estado: "listo", datos }))
      .catch((error) => vigente && setResultado({ estado: "error", error }));
    return () => {
      vigente = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [clave]);

  return resultado;
}
