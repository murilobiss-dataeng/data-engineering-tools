import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MB Ofertas - Painel",
  description: "Envio automatizado de ofertas via WhatsApp",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className="min-h-screen bg-gradient-to-b from-slate-50 to-white text-slate-900 antialiased">
        <header className="sticky top-0 z-20 border-b border-slate-200/80 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80">
          <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
            <a href="/" className="text-lg font-bold tracking-tight text-emerald-700 hover:text-emerald-800">
              MB Ofertas
            </a>
            <nav className="flex gap-1">
              <a
                href="/gerar-oferta"
                className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-emerald-50 hover:text-emerald-700"
              >
                Gerar oferta
              </a>
              <a
                href="/"
                className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
              >
                Produtos
              </a>
              <a
                href="/campanhas"
                className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
              >
                Campanhas
              </a>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>
      </body>
    </html>
  );
}
