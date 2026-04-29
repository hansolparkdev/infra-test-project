import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'standalone',  // Docker 배포에 최적화
  reactStrictMode: true,
};

export default nextConfig;
