import { MetadataRoute } from "next";

const BASE_URL = process.env.NEXT_PUBLIC_SITE_URL ?? "https://salmododia.com.br";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: "*", allow: "/", disallow: ["/checkout", "/api/"] },
    ],
    sitemap: `${BASE_URL}/sitemap.xml`,
  };
}
