import type { Metadata } from "next";
import "./globals.css";
import ChakraProvider from "../components/ChakraProvider";

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
      <body>
        <ChakraProvider>{children}</ChakraProvider>
      </body>
    </html>
  );
}
