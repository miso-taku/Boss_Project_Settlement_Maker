import {
  Container,
  Heading,
  Text,
  Box,
  VStack,
  Badge,
  HStack,
} from "@chakra-ui/react";
import ReplyForm from "../components/ReplyForm";

export default function Home() {
  return (
    <Box
      minH="100vh"
      bgGradient="linear(to-br, gray.50, gray.100)"
      py={12}
      px={4}
    >
      <Container maxW="900px" centerContent>
        <VStack spacing={6} align="stretch" className="fade-in">
          <Box textAlign="center" mb={4}>
            <Heading
              as="h1"
              size="2xl"
              mb={3}
              color="gray.800"
              fontWeight="bold"
            >
              上司案件・落とし所AIエージェント
            </Heading>
            <HStack spacing={3} justify="center" mb={2}>
              <Badge
                colorScheme="gray"
                fontSize="md"
                px={3}
                py={1}
                borderRadius="full"
                variant="subtle"
              >
                「今日中に」を今日中にしないAI
              </Badge>
            </HStack>
            <Text fontSize="lg" color="gray.600" mt={2}>
              依頼文と状況を入力するだけで、角の立たない返信案を自動生成
            </Text>
          </Box>
          <ReplyForm />
        </VStack>
      </Container>
    </Box>
  );
}
