import { Metadata } from "next";
import Link from "next/link";
import { redirect } from "next/navigation";
import { getProductBySlug } from "@/data/products";
import { Button } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Checkout",
  description: "Finalize sua compra - Salmo do Dia",
  robots: { index: false, follow: false },
};

interface PageProps {
  searchParams: Promise<{ product?: string }>;
}

export default async function CheckoutPage({ searchParams }: PageProps) {
  const { product: slug } = await searchParams;
  if (!slug) redirect(ROUTES.loja);

  const product = getProductBySlug(slug);
  if (!product || product.type !== "digital") redirect(ROUTES.loja);

  const price = product.price ?? 0;
  const formatPrice = (c: number) =>
    new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" }).format(c / 100);

  return (
    <div className="container mx-auto max-w-2xl px-4 py-12">
      <h1 className="font-serif text-2xl font-bold text-gold-800">Checkout (simulado)</h1>
      <p className="mt-2 text-muted-foreground">
        Esta página simula o checkout. Integração com Stripe em breve.
      </p>

      <div className="mt-10 rounded-lg border bg-card p-6">
        <h2 className="font-semibold">{product.title}</h2>
        <p className="mt-1 text-sm text-muted-foreground">{product.description}</p>
        <p className="mt-4 text-xl font-bold text-gold-700">{formatPrice(price)}</p>
        <p className="mt-6 text-sm text-muted-foreground">
          Após o pagamento (futuro Stripe), o download do e-book será disponibilizado por e-mail.
        </p>
        <div className="mt-8 flex gap-4">
          <Button asChild variant="gold">
            <Link href={ROUTES.loja}>Confirmar compra (simulado)</Link>
          </Button>
          <Button asChild variant="outline">
            <Link href={ROUTES.loja}>Voltar à loja</Link>
          </Button>
        </div>
      </div>
    </div>
  );
}
