import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-scripture-darker to-scripture-dark py-20 text-scripture-cream md:py-28">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(201,162,39,0.08)_0%,transparent_70%)]" />
      <div className="container relative mx-auto px-4 text-center">
        <p className="font-serif text-gold-400 text-sm uppercase tracking-widest md:text-base">
          Palavra para o seu dia
        </p>
        <h1 className="mt-4 font-serif text-4xl font-bold tracking-tight md:text-5xl lg:text-6xl">
          Salmo do Dia
        </h1>
        <p className="mx-auto mt-6 max-w-2xl text-lg text-scripture-cream/85">
          Reflexões, salmos e conteúdo para fortalecer sua fé. E-books e recursos na nossa loja.
        </p>
        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Button asChild size="lg" variant="gold" className="font-medium">
            <Link href={ROUTES.salmos}>Ver Salmo de Hoje</Link>
          </Button>
          <Button asChild size="lg" variant="outline" className="border-gold-500/50 text-gold-300 hover:bg-gold-500/10">
            <Link href={ROUTES.loja}>Loja</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
