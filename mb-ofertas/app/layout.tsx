import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MB Ofertas - Painel",
  description: "Crie e gerencie ofertas para divulgar em redes e WhatsApp",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-stone-50 text-stone-800 antialiased">
        <header className="sticky top-0 z-20 border-b border-stone-200 bg-white/95 shadow-sm backdrop-blur">
          <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4 sm:px-6">
            <a
              href="/"
              className="flex items-center gap-2 text-xl font-bold tracking-tight text-stone-900 hover:text-amber-700 transition"
            >
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500 text-white text-sm font-bold">
                M
              </span>
              MB Ofertas
            </a>
            <nav className="flex items-center gap-1">
              <a
                href="/gerar-oferta"
                className="rounded-lg px-4 py-2.5 text-sm font-medium text-stone-600 transition hover:bg-amber-50 hover:text-amber-800"
              >
                Buscar por URL
              </a>
              <a
                href="/"
                className="rounded-lg px-4 py-2.5 text-sm font-medium text-stone-600 transition hover:bg-stone-100 hover:text-stone-900"
              >
                Produtos
              </a>
              <a
                href="/campanhas"
                className="rounded-lg px-4 py-2.5 text-sm font-medium text-stone-600 transition hover:bg-stone-100 hover:text-stone-900"
              >
                Campanhas
              </a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6">{children}</main>
      </body>
    </html>
  );
}
