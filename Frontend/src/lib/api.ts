export type Editorial = {
  id: string;
  nombre: string;
  pais: string;
};

export type Libro = {
  id: string;
  titulo: string;
  anio: number;
  paginas: number;
  imagen: string;
  editorial: Editorial;
};

export type EditorialDetalle = Editorial & {
  libros: Libro[];
};

export type DatosLibro = {
  titulo: string;
  anio: number;
  paginas: number;
  imagen: string;
  editorial_id: string;
};

export type ErroresCampos = Record<string, string[]>;

export class ApiError extends Error {
  constructor(
    public status: number,
    public datos: unknown,
  ) {
    super(`La API respondió con el código ${status}`);
  }

  get noEncontrado() {
    return this.status === 404;
  }
}

async function pedir<T>(ruta: string, opciones: RequestInit = {}): Promise<T> {
  const respuesta = await fetch(`/api${ruta}`, {
    ...opciones,
    headers: { "Content-Type": "application/json", Accept: "application/json" },
  });

  if (respuesta.status === 204) {
    return undefined as T;
  }

  const datos = await respuesta.json().catch(() => null);
  if (!respuesta.ok) {
    throw new ApiError(respuesta.status, datos);
  }
  return datos as T;
}

export const listarLibros = () => pedir<Libro[]>("/libros");

export const obtenerLibro = (id: string) => pedir<Libro>(`/libros/${id}`);

export const crearLibro = (datos: DatosLibro) =>
  pedir<Libro>("/libros", { method: "POST", body: JSON.stringify(datos) });

export const editarLibro = (id: string, datos: DatosLibro) =>
  pedir<Libro>(`/libros/${id}`, { method: "PUT", body: JSON.stringify(datos) });

export const eliminarLibro = (id: string) => pedir<void>(`/libros/${id}`, { method: "DELETE" });

export const listarEditoriales = () => pedir<Editorial[]>("/editoriales");

export const obtenerEditorial = (id: string) => pedir<EditorialDetalle>(`/editoriales/${id}`);

export function rutaImagen(imagen: string) {
  if (/^(https?:)?\/\//.test(imagen) || imagen.startsWith("/")) {
    return imagen;
  }
  return `/${imagen}`;
}
