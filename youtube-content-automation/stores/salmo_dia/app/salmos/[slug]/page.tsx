import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import { getSalmoBySlug } from "@/data/salmos";
import { Button } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";
import { sanitizeText } from "@/lib/utils";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const salmo = getSalmoBySlug(slug);
  if (!salmo) return { title: "Salmo não encontrado" };
  return {
    title: `Salmo ${salmo.numero} - ${salmo.titulo}`,
    description: salmo.texto.slice(0, 160) + "...",
    openGraph: {
      title: `Salmo ${salmo.numero} | ${salmo.titulo}`,
      description: salmo.texto.slice(0, 160) + "...",
    },
  };
}

export default async function SalmoPage({ params }: PageProps) {
  const { slug } = await params;
  const salmo = getSalmoBySlug(slug);
  if (!salmo) notFound();

  const verses = salmo.texto.split("\n").filter((l) => l.trim());

  return (
    <div className="container mx-auto max-w-3xl px-4 py-10">
      <Button asChild variant="ghost" size="sm" className="mb-8">
        <Link href={ROUTES.salmos}>← Voltar aos Salmos</Link>
      </Button>

      <article>
        <header className="border-b border-gold-200/50 pb-6">
          <p className="text-sm font-medium uppercase tracking-wide text-gold-600">
            Salmo {salmo.numero}
          </p>
          <h1 className="mt-2 font-serif text-3xl font-bold text-foreground md:text-4xl">
            {salmo.titulo}
          </h1>
          <p className="mt-2 text-muted-foreground">Tema: {salmo.tema}</p>
        </header>

        <div className="prose-scripture mt-8 space-y-4 font-serif text-lg leading-relaxed text-foreground">
          {verses.map((line, i) => (
            <p key={i} className="text-balance">
              {sanitizeText(line)}
            </p>
          ))}
        </div>
      </article>

      <div className="mt-12 flex flex-wrap gap-4">
        <Button asChild variant="gold">
          <Link href={ROUTES.salmos}>Ver todos os Salmos</Link>
        </Button>
        <Button asChild variant="outline">
          <Link href={ROUTES.loja}>Visitar a Loja</Link>
        </Button>
      </div>
    </div>
  );
}
