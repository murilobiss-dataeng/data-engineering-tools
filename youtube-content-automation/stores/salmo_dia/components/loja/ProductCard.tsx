import Link from "next/link";
import Image from "next/image";
import type { Product } from "@/data/products";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { ROUTES } from "@/lib/constants";
import { ExternalLink, ShoppingCart } from "lucide-react";

function formatPrice(cents: number) {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(cents / 100);
}

export function ProductCard({ product }: { product: Product }) {
  const isAffiliate = product.type === "affiliate";

  return (
    <Card className="flex flex-col overflow-hidden transition hover:shadow-md">
      <Link href={`${ROUTES.loja}/${product.slug}`} className="block">
        <div className="relative aspect-[4/3] bg-muted">
          <Image
            src={product.image}
            alt={product.title}
            fill
            className="object-cover"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          />
        </div>
      </Link>
      <CardHeader>
        <Link href={`${ROUTES.loja}/${product.slug}`}>
          <h3 className="font-serif text-xl font-semibold hover:text-gold-700">
            {product.title}
          </h3>
        </Link>
        <p className="line-clamp-2 text-sm text-muted-foreground">
          {product.description}
        </p>
      </CardHeader>
      <CardFooter className="mt-auto flex items-center justify-between gap-2 border-t pt-4">
        {isAffiliate ? (
          <span className="text-sm text-muted-foreground">Afiliado Amazon</span>
        ) : product.price != null ? (
          <span className="font-medium text-gold-700">
            {formatPrice(product.price)}
          </span>
        ) : null}
        <Button asChild size="sm" variant={isAffiliate ? "outline" : "gold"}>
          <Link href={`${ROUTES.loja}/${product.slug}`}>
            {isAffiliate ? (
              <>
                Ver na Amazon
                <ExternalLink className="ml-1.5 h-3.5 w-3.5" />
              </>
            ) : (
              <>
                Comprar
                <ShoppingCart className="ml-1.5 h-3.5 w-3.5" />
              </>
            )}
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
}
