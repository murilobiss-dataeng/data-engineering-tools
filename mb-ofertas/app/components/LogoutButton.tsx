"use client";

import { usePathname } from "next/navigation";

export function LogoutButton() {
  const pathname = usePathname();
  if (pathname === "/login") return null;

  async function handleLogout() {
    await fetch("/api/auth/logout", { method: "POST" });
    window.location.href = "/login";
  }

  return (
    <button
      type="button"
      onClick={handleLogout}
      className="rounded-lg px-4 py-2.5 text-sm font-medium text-stone-500 transition hover:bg-stone-100 hover:text-stone-700"
    >
      Sair
    </button>
  );
}
