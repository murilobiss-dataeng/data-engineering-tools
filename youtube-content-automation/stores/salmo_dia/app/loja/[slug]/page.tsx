import { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import Image from "next/image";
import { getProductBySlug } from "@/data/products";
import { Button } from "@/components/ui/button";
import { ROUTES } from "@/lib/constants";
import { AmazonButton } from "@/components/loja/AmazonButton";

interface PageProps {
  params: Promise<{ slug: string }>;
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params;
  const product = getProductBySlug(slug);
  if (!product) return { title: "Produto não encontrado" };
  return {
    title: product.title,
    description: product.description,
    openGraph: { title: product.title, description: product.description },
  };
}

export default async function ProductPage({ params }: PageProps) {
  const { slug } = await params;
  const product = getProductBySlug(slug);
  if (!product) notFound();

  const isAffiliate = product.type === "affiliate";

  function formatPrice(cents: number) {
    return new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(cents / 100);
  }

  return (
    <div className="container mx-auto px-4 py-10">
      <div className="grid gap-10 lg:grid-cols-2">
        <div className="relative aspect-square overflow-hidden rounded-lg bg-muted">
          <Image
            src={product.image}
            alt={product.title}
            fill
            className="object-cover"
            priority
            sizes="(max-width: 1024px) 100vw, 50vw"
          />
        </div>
        <div>
          <p className="text-sm font-medium uppercase tracking-wide text-gold-600">
            {product.category}
          </p>
          <h1 className="mt-2 font-serif text-3xl font-bold text-foreground md:text-4xl">
            {product.title}
          </h1>
          <p className="mt-4 text-muted-foreground">{product.description}</p>
          <div className="mt-8 flex flex-wrap items-center gap-4">
            {isAffiliate ? (
              <AmazonButton
                url={product.affiliateUrl!}
                productId={product.id}
                productTitle={product.title}
              />
            ) : product.price != null ? (
              <>
                <span className="text-2xl font-bold text-gold-700">
                  {formatPrice(product.price)}
                </span>
                <Button asChild variant="gold" size="lg">
                  <Link href={`${ROUTES.checkout}?product=${product.slug}`}>
                    Comprar (checkout simulado)
                  </Link>
                </Button>
              </>
            ) : null}
          </div>
          <p className="mt-6 text-sm text-muted-foreground">
            {isAffiliate
              ? "Ao clicar você será redirecionado à Amazon. Podemos receber comissão de afiliado."
              : "Checkout simulado. Integração com Stripe em breve."}
          </p>
        </div>
      </div>
    </div>
  );
}
