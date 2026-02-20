import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";

export default function NotFound() {
  return (
    <div className="container mx-auto flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
      <h1 className="font-serif text-4xl font-bold text-gold-800">404</h1>
      <p className="mt-4 text-muted-foreground">Página não encontrada.</p>
      <Button asChild variant="gold" className="mt-8">
        <Link href={ROUTES.home}>Voltar ao início</Link>
      </Button>
    </div>
  );
}
