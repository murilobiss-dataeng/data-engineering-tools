import Link from "next/link";
import Image from "next/image";
import { products } from "@/data/products";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { ROUTES } from "@/lib/constants";
import { ShoppingBag } from "lucide-react";

const featured = products.slice(0, 3);

function formatPrice(cents: number) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(cents / 100);
}

export function FeaturedProducts() {
  return (
    <section className="py-16 md:py-20">
      <div className="container mx-auto px-4">
        <h2 className="font-serif text-3xl font-bold text-gold-800 md:text-4xl">
          Destaques da Loja
        </h2>
        <p className="mt-2 text-muted-foreground">
          E-books e produtos selecionados para você.
        </p>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {featured.map((product) => (
            <Card key={product.id} className="overflow-hidden transition hover:shadow-md">
              <div className="relative aspect-[4/3] bg-muted">
                <Image
                  src={product.image}
                  alt={product.title}
                  fill
                  className="object-cover"
                  sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                />
              </div>
              <CardHeader>
                <h3 className="font-serif text-xl font-semibold">{product.title}</h3>
                <p className="line-clamp-2 text-sm text-muted-foreground">
                  {product.description}
                </p>
              </CardHeader>
              <CardFooter className="flex items-center justify-between gap-2">
                {product.type === "digital" && product.price != null ? (
                  <span className="font-medium text-gold-700">{formatPrice(product.price)}</span>
                ) : (
                  <span className="text-sm text-muted-foreground">Ver na Amazon</span>
                )}
                <Button asChild size="sm" variant="gold">
                  <Link href={`${ROUTES.loja}/${product.slug}`}>Ver</Link>
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
        <div className="mt-10 text-center">
          <Button asChild variant="outline" size="lg">
            <Link href={ROUTES.loja}>
              <ShoppingBag className="mr-2 h-4 w-4" />
              Ver toda a Loja
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
