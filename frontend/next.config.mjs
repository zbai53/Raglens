/** @type {import('next').NextConfig} */
const nextConfig = {
  // Emit a self-contained server bundle at .next/standalone.
  // Required by frontend/Dockerfile (which copies from that directory).
  output: 'standalone',
  reactStrictMode: true,
};

export default nextConfig;
