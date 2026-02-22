/** @type {import('next').NextConfig} */
const nextConfig = {
  // Não use output: "standalone" no Vercel – deixe o padrão para evitar 404
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:4000",
  },
};

module.exports = nextConfig;
