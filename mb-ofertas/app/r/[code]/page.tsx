import { redirect, notFound } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000";

export default async function ShortLinkRedirect({
  params,
}: {
  params: Promise<{ code: string }>;
}) {
  const { code } = await params;
  if (!code?.trim() || code.length > 20) notFound();
  try {
    const res = await fetch(`${API_URL}/api/short-links/${encodeURIComponent(code)}`, {
      cache: "no-store",
    });
    if (!res.ok) notFound();
    const data = (await res.json()) as { url?: string };
    if (!data?.url) notFound();
    redirect(data.url);
  } catch {
    notFound();
  }
}
