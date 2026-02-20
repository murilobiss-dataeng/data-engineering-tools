import Link from "next/link";
import { SITE_NAME, ROUTES, SOCIAL_LINKS } from "@/lib/constants";
import {
  Youtube,
  Instagram,
  Facebook,
  Twitter,
  Music2,
} from "lucide-react";

const socialConfig = [
  { key: "youtube", href: SOCIAL_LINKS.youtube, Icon: Youtube, label: "YouTube" },
  { key: "instagram", href: SOCIAL_LINKS.instagram, Icon: Instagram, label: "Instagram" },
  { key: "facebook", href: SOCIAL_LINKS.facebook, Icon: Facebook, label: "Facebook" },
  { key: "twitter", href: SOCIAL_LINKS.twitter, Icon: Twitter, label: "Twitter/X" },
  { key: "tiktok", href: SOCIAL_LINKS.tiktok, Icon: Music2, label: "TikTok" },
];

export function Footer() {
  return (
    <footer className="border-t bg-scripture-darker text-scripture-cream">
      <div className="container mx-auto px-4 py-10">
        <div className="grid gap-8 md:grid-cols-3">
          <div>
            <p className="font-serif text-lg font-semibold text-gold-400">{SITE_NAME}</p>
            <p className="mt-2 text-sm text-scripture-cream/80">
              Palavra, reflexão e conteúdo para o seu dia. Conecte-se conosco nas redes.
            </p>
          </div>
          <div>
            <p className="text-sm font-medium text-gold-400">Navegação</p>
            <ul className="mt-3 space-y-2 text-sm">
              <li>
                <Link href={ROUTES.home} className="hover:text-gold-300 transition-colors">
                  Início
                </Link>
              </li>
              <li>
                <Link href={ROUTES.salmos} className="hover:text-gold-300 transition-colors">
                  Salmos
                </Link>
              </li>
              <li>
                <Link href={ROUTES.loja} className="hover:text-gold-300 transition-colors">
                  Loja
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <p className="text-sm font-medium text-gold-400">Redes sociais</p>
            <div className="mt-3 flex flex-wrap gap-3">
              {socialConfig.map(({ key, href, Icon, label }) => (
                <a
                  key={key}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex h-10 w-10 items-center justify-center rounded-full border border-gold-600/50 bg-gold-950/30 text-gold-400 transition hover:bg-gold-800/40 hover:text-gold-300"
                  aria-label={label}
                >
                  <Icon className="h-5 w-5" />
                </a>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-8 border-t border-white/10 pt-6 text-center text-sm text-scripture-cream/70">
          © {new Date().getFullYear()} {SITE_NAME}. Todos os direitos reservados.
        </div>
      </div>
    </footer>
  );
}
