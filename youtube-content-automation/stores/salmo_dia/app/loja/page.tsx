import { Metadata } from "next";
import { products } from "@/data/products";
import { ProductCard } from "@/components/loja/ProductCard";
import { SITE_NAME } from "@/lib/constants";

export const metadata: Metadata = {
  title: "Loja",
  description: "E-books, recursos digitais e produtos selecionados. Salmo do Dia.",
};

export default function LojaPage() {
  const digital = products.filter((p) => p.type === "digital");
  const affiliate = products.filter((p) => p.type === "affiliate");

  return (
    <div className="container mx-auto px-4 py-10">
      <h1 className="font-serif text-3xl font-bold text-gold-800 md:text-4xl">
        Loja
      </h1>
      <p className="mt-2 text-muted-foreground">
        Produtos próprios e indicações da Amazon.
      </p>

      <section className="mt-12">
        <h2 className="font-serif text-xl font-semibold text-foreground">
          Produtos digitais
        </h2>
        <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {digital.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

      <section className="mt-14">
        <h2 className="font-serif text-xl font-semibold text-foreground">
          Afiliados Amazon
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Ao comprar pelos links abaixo, você apoia o Salmo do Dia (comissão de afiliado).
        </p>
        <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {affiliate.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>
    </div>
  );
}
