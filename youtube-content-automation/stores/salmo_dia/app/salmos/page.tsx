import { Metadata } from "next";
import Link from "next/link";
import { salmos } from "@/data/salmos";
import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { ROUTES } from "@/lib/constants";
import { BookOpen } from "lucide-react";

export const metadata: Metadata = {
  title: "Salmos",
  description: "Leia os salmos e medite na Palavra. Salmo do Dia.",
};

export default function SalmosPage() {
  return (
    <div className="container mx-auto px-4 py-10">
      <h1 className="font-serif text-3xl font-bold text-gold-800 md:text-4xl">
        Salmos
      </h1>
      <p className="mt-2 text-muted-foreground">
        Conteúdo para leitura e reflexão.
      </p>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {salmos.map((salmo) => (
          <Link key={salmo.id} href={`${ROUTES.salmos}/${salmo.slug}`}>
            <Card className="h-full transition hover:shadow-md hover:border-gold-200">
              <CardHeader className="pb-2">
                <div className="flex items-center gap-2 text-gold-600">
                  <BookOpen className="h-4 w-4" />
                  <span className="text-sm font-medium">Salmo {salmo.numero}</span>
                </div>
                <h2 className="font-serif text-xl font-semibold text-foreground">
                  {salmo.titulo}
                </h2>
                <p className="text-sm text-muted-foreground">Tema: {salmo.tema}</p>
              </CardHeader>
              <CardContent>
                <p className="line-clamp-3 text-sm text-muted-foreground whitespace-pre-line">
                  {salmo.texto}
                </p>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
