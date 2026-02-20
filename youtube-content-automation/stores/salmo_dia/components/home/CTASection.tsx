import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";

export function CTASection() {
  return (
    <section className="py-16 md:py-20">
      <div className="container mx-auto px-4">
        <div className="rounded-2xl bg-gradient-to-br from-gold-500/15 to-gold-700/10 border border-gold-200 p-8 text-center md:p-12">
          <h2 className="font-serif text-2xl font-bold text-gold-800 md:text-3xl">
            Comece o dia com a Palavra
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-muted-foreground">
            Acesse o salmo de hoje e visite nossa loja para e-books e recursos.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Button asChild size="lg" variant="gold">
              <Link href={ROUTES.salmos}>Ver Salmo de Hoje</Link>
            </Button>
            <Button asChild size="lg" variant="outline">
              <Link href={ROUTES.loja}>Ir para a Loja</Link>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
