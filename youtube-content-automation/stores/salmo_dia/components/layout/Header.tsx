"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { SITE_NAME, ROUTES, SOCIAL_LINKS } from "@/lib/constants";
import { Button } from "@/components/ui/button";
import { BookOpen, ShoppingBag, Menu } from "lucide-react";
import { useState } from "react";

const navLinks = [
  { href: ROUTES.home, label: "Início" },
  { href: ROUTES.salmos, label: "Salmos" },
  { href: ROUTES.loja, label: "Loja" },
];

export function Header() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link href="/" className="flex items-center gap-2 font-serif text-xl font-semibold text-gold-700">
          <BookOpen className="h-6 w-6" aria-hidden />
          {SITE_NAME}
        </Link>

        <nav className="hidden md:flex md:items-center md:gap-6" aria-label="Principal">
          {navLinks.map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`text-sm font-medium transition-colors hover:text-gold-600 ${
                pathname === href ? "text-gold-600" : "text-muted-foreground"
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <Button asChild size="sm" variant="gold" className="hidden sm:inline-flex">
            <Link href={ROUTES.loja}>
              <ShoppingBag className="mr-1.5 h-4 w-4" />
              Loja
            </Link>
          </Button>
          <Button
            variant="ghost"
            size="icon"
            className="md:hidden"
            onClick={() => setMobileOpen((o) => !o)}
            aria-expanded={mobileOpen}
            aria-label="Abrir menu"
          >
            <Menu className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {mobileOpen && (
        <div className="border-t md:hidden">
          <nav className="container mx-auto flex flex-col gap-1 px-4 py-3" aria-label="Menu móvel">
            {navLinks.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className="rounded-md px-3 py-2 text-sm font-medium hover:bg-accent"
                onClick={() => setMobileOpen(false)}
              >
                {label}
              </Link>
            ))}
            <Button asChild variant="gold" className="mt-2">
              <Link href={ROUTES.loja} onClick={() => setMobileOpen(false)}>
                Ir para a Loja
              </Link>
            </Button>
          </nav>
        </div>
      )}
    </header>
  );
}
