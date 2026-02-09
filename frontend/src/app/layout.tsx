import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "上司案件・落とし所AIエージェント",
  description: "「今日中に」を今日中にしないAI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
