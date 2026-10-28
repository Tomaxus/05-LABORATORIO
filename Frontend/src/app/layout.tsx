import type { Metadata } from "next";
import Link from "next/link";

import "./globals.css";

export const metadata: Metadata = {
  title: "Biblioteca Paulo Coelho",
  description: "Catálogo de libros de Paulo Coelho",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="es" className="antialiased">
      <body>
        <header className="flex items-center justify-between gap-4 border-b border-linea px-6 py-8 max-sm:flex-col sm:px-12">
          <h1 className="m-0 text-[1.4rem]">
            <Link href="/libros" className="text-tinta hover:underline">
              Biblioteca Paulo Coelho
            </Link>
          </h1>
          <nav className="flex gap-6 text-[0.95rem]">
            <Link href="/libros" className="text-tinta-suave hover:underline">Catálogo</Link>
            <Link href="/libros/editoriales" className="text-tinta-suave hover:underline">Editoriales</Link>
            <Link href="/libros/autor" className="text-tinta-suave hover:underline">Sobre el autor</Link>
          </nav>
        </header>

        <main className="mx-auto max-w-[900px] px-6 pt-4 pb-16 sm:px-12">
          {children}
        </main>

        <footer className="p-8 text-center text-[0.85rem] text-tinta-suave"></footer>
      </body>
    </html>
  );
}
