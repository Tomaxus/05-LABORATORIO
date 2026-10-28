type Props = {
  filas: [etiqueta: string, valor: string | number][];
};

export default function Ficha({ filas }: Props) {
  return (
    <dl className="my-10 text-left">
      {filas.map(([etiqueta, valor]) => (
        <div key={etiqueta} className="flex justify-between border-b border-linea py-[0.7rem]">
          <dt className="text-tinta-suave">{etiqueta}</dt>
          <dd>{valor}</dd>
        </div>
      ))}
    </dl>
  );
}
