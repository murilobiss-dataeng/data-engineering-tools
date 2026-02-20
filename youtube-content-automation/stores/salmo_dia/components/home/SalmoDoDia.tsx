import Link from "next/link";
import { getSalmoDoDia } from "@/data/salmos";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ROUTES } from "@/lib/constants";

export function SalmoDoDia() {
  const salmo = getSalmoDoDia();
  const preview = salmo.texto.split("\n").slice(0, 4).join(" ");

  return (
    <section className="bg-scripture-cream py-16 md:py-20">
      <div className="container mx-auto px-4">
        <h2 className="font-serif text-3xl font-bold text-gold-800 md:text-4xl">
          Salmo do Dia
        </h2>
        <p className="mt-2 text-muted-foreground">
          Uma palavra para meditar hoje.
        </p>
        <Card className="mt-10 border-gold-200 bg-white shadow-sm">
          <CardHeader>
            <p className="text-sm font-medium uppercase tracking-wide text-gold-600">
              Salmo {salmo.numero}
            </p>
            <h3 className="font-serif text-2xl font-semibold text-scripture-dark">
              {salmo.titulo}
            </h3>
            <p className="text-sm text-muted-foreground">Tema: {salmo.tema}</p>
          </CardHeader>
          <CardContent>
            <p className="prose-scripture text-foreground/90 line-clamp-4 whitespace-pre-line">
              {preview}…
            </p>
            <Button asChild variant="gold" className="mt-6">
              <Link href={`${ROUTES.salmos}/${salmo.slug}`}>
                Ler salmo completo
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </section>
  );
}
