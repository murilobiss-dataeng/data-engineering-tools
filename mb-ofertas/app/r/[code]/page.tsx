import { redirect, notFound } from "next/navigation";
import { getPublicApiBaseUrl } from "@/lib/api";

export default async function ShortLinkRedirect({
  params,
}: {
  params: Promise<{ code: string }>;
}) {
  const { code } = await params;
  if (!code?.trim() || code.length > 20) notFound();
  try {
    const base = getPublicApiBaseUrl();
    const res = await fetch(`${base}/api/short-links/${encodeURIComponent(code)}`, {
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
