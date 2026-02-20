"use client";

import { useState } from "react";
import { Share2, Youtube, Instagram, Facebook, Twitter, Music2 } from "lucide-react";
import { SOCIAL_LINKS } from "@/lib/constants";

const items = [
  { key: "youtube", href: SOCIAL_LINKS.youtube, Icon: Youtube, label: "YouTube" },
  { key: "instagram", href: SOCIAL_LINKS.instagram, Icon: Instagram, label: "Instagram" },
  { key: "facebook", href: SOCIAL_LINKS.facebook, Icon: Facebook, label: "Facebook" },
  { key: "twitter", href: SOCIAL_LINKS.twitter, Icon: Twitter, label: "X" },
  { key: "tiktok", href: SOCIAL_LINKS.tiktok, Icon: Music2, label: "TikTok" },
];

export function SocialFloatButton() {
  const [open, setOpen] = useState(false);

  return (
    <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end gap-2">
      {open && (
        <div className="flex flex-col gap-2 rounded-lg border bg-card p-2 shadow-lg">
          {items.map(({ key, href, Icon, label }) => (
            <a
              key={key}
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 rounded-md px-3 py-2 text-sm hover:bg-accent"
              aria-label={label}
            >
              <Icon className="h-4 w-4 text-gold-600" />
              {label}
            </a>
          ))}
        </div>
      )}
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="flex h-12 w-12 items-center justify-center rounded-full bg-gold-500 text-gold-950 shadow-lg transition hover:bg-gold-400"
        aria-expanded={open}
        aria-label={open ? "Fechar redes sociais" : "Abrir redes sociais"}
      >
        <Share2 className="h-5 w-5" />
      </button>
    </div>
  );
}
