import type { NextConfig } from "next";

const API_URL = process.env.API_URL ?? "https://localhost:8443";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:ruta*",
        destination: `${API_URL}/api/:ruta*/`,
      },
    ];
  },
};

export default nextConfig;
