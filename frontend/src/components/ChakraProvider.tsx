"use client";

import { ChakraProvider as BaseChakraProvider } from "@chakra-ui/react";

/**
 * Chakra UIのProviderコンポーネント。
 *
 * Next.js App Routerのサーバーコンポーネントから使用するため、
 * クライアントコンポーネントとして実装。
 */
export default function ChakraProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  return <BaseChakraProvider>{children}</BaseChakraProvider>;
}
