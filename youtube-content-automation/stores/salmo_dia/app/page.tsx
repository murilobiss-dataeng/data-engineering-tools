import { Hero } from "@/components/home/Hero";
import { SalmoDoDia } from "@/components/home/SalmoDoDia";
import { FeaturedProducts } from "@/components/home/FeaturedProducts";
import { CTASection } from "@/components/home/CTASection";

export default function HomePage() {
  return (
    <>
      <Hero />
      <SalmoDoDia />
      <FeaturedProducts />
      <CTASection />
    </>
  );
}
