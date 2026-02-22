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
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        <header className="border-b border-slate-200 bg-white">
          <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
            <h1 className="text-lg font-semibold">MB Ofertas</h1>
            <nav className="flex gap-6">
              <a href="/" className="text-slate-600 hover:text-slate-900">
                Produtos
              </a>
              <a href="/campanhas" className="text-slate-600 hover:text-slate-900">
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
