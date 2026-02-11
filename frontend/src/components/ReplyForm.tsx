"use client";

import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  FormControl,
  FormLabel,
  Input,
  Radio,
  RadioGroup,
  Stack,
  Textarea,
  Alert,
  AlertIcon,
  AlertTitle,
  AlertDescription,
  Spinner,
  useToast,
  Heading,
  Text,
  Icon,
  Divider,
  HStack,
  Badge,
  VStack,
  useColorModeValue,
} from "@chakra-ui/react";
import {
  EditIcon,
  TimeIcon,
  StarIcon,
  InfoIcon,
  CopyIcon,
  CheckIcon,
} from "@chakra-ui/icons";
import type { ApiError, Priority, ReplyDraftItem } from "../api/types";
import { ApiErrorException, generateReplyDrafts } from "../api/replyDrafts";

/**
 * 返信案生成フォームコンポーネント。
 *
 * 依頼文・残り時間・優先度・制約を入力し、返信案を生成・表示・コピーする。
 * Chakra UI v2を使用してモダンで洗練されたUIを実装。
 */
export default function ReplyForm() {
  const [requestText, setRequestText] = useState("");
  const [remainingHours, setRemainingHours] = useState<number | null>(null);
  const [priority, setPriority] = useState<Priority | null>(null);
  const [constraints, setConstraints] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [replyDraft, setReplyDraft] = useState<ReplyDraftItem | null>(null);
  const toast = useToast();

  const cardBg = useColorModeValue("white", "gray.800");
  const inputBg = useColorModeValue("white", "gray.700");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setReplyDraft(null);

    try {
      const response = await generateReplyDrafts({
        request_text: requestText,
        remaining_hours: remainingHours ?? undefined,
        priority: priority ?? undefined,
        constraints: constraints || undefined,
      });

      if (response.draft) {
        setReplyDraft(response.draft);
        toast({
          title: "返信案を生成しました",
          status: "success",
          duration: 3000,
          isClosable: true,
          position: "top",
        });
      }
    } catch (err) {
      if (err instanceof ApiErrorException) {
        setError(err.apiError);
      } else {
        setError({
          type: "unknown_error",
          message:
            "エラーが発生しました。しばらく時間をおいてから再度お試しください。",
          originalMessage:
            err instanceof Error ? err.message : "Unknown error occurred",
        });
      }
      console.error("API error:", err);
      toast({
        title: "エラーが発生しました",
        description:
          err instanceof ApiErrorException
            ? err.apiError.message
            : "予期しないエラーが発生しました",
        status: "error",
        duration: 5000,
        isClosable: true,
        position: "top",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!replyDraft) return;

    try {
      await navigator.clipboard.writeText(replyDraft.text);
      toast({
        title: "コピーしました",
        status: "success",
        duration: 2000,
        isClosable: true,
        position: "top",
      });
    } catch (err) {
      console.error("Copy error:", err);
      // フォールバック: テキストエリアを作成してコピー
      const textarea = document.createElement("textarea");
      textarea.value = replyDraft.text;
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
        toast({
          title: "コピーしました",
          status: "success",
          duration: 2000,
          isClosable: true,
          position: "top",
        });
      } catch (fallbackErr) {
        console.error("Fallback copy error:", fallbackErr);
        toast({
          title: "コピーに失敗しました",
          status: "error",
          duration: 3000,
          isClosable: true,
          position: "top",
        });
      }
      document.body.removeChild(textarea);
    }
  };

  const getPriorityColor = (priority: Priority | null) => {
    switch (priority) {
      case "high":
        return "red";
      case "medium":
        return "orange";
      case "low":
        return "green";
      default:
        return "gray";
    }
  };

  return (
    <Stack spacing={6}>
      <Card
        bg={cardBg}
        boxShadow="xl"
        borderRadius="2xl"
        overflow="hidden"
        className="fade-in"
        _hover={{ boxShadow: "2xl", transform: "translateY(-2px)" }}
        transition="all 0.3s"
      >
        <CardHeader
          bg="gray.600"
          color="white"
          py={6}
        >
          <HStack spacing={3}>
            <Icon as={EditIcon} boxSize={6} />
            <Heading size="lg" fontWeight="bold">
              入力フォーム
            </Heading>
          </HStack>
        </CardHeader>
        <CardBody p={6}>
          <form onSubmit={handleSubmit}>
            <VStack spacing={6} align="stretch">
              <FormControl isRequired>
                <FormLabel
                  fontSize="md"
                  fontWeight="semibold"
                  color="gray.700"
                  mb={2}
                >
                  <HStack spacing={2}>
                    <Icon as={EditIcon} color="gray.600" />
                    <Text>依頼文</Text>
                    <Badge colorScheme="gray" fontSize="xs" variant="subtle">
                      必須
                    </Badge>
                  </HStack>
                </FormLabel>
                <Textarea
                  id="request-text"
                  value={requestText}
                  onChange={(e) => setRequestText(e.target.value)}
                  rows={5}
                  placeholder="上司からの依頼文を入力してください..."
                  required
                  bg={inputBg}
                  border="2px solid"
                  borderColor="gray.200"
                  _hover={{ borderColor: "gray.300" }}
                  _focus={{
                    borderColor: "gray.500",
                    boxShadow: "0 0 0 1px var(--chakra-colors-gray-500)",
                  }}
                  transition="all 0.2s"
                />
              </FormControl>

              <HStack spacing={4} align="flex-start">
                <FormControl flex="1">
                  <FormLabel
                    fontSize="md"
                    fontWeight="semibold"
                    color="gray.700"
                    mb={2}
                  >
                    <HStack spacing={2}>
                      <Icon as={TimeIcon} color="gray.600" />
                      <Text>残り時間（時間）</Text>
                    </HStack>
                  </FormLabel>
                  <Input
                    id="remaining-hours"
                    type="number"
                    min="0"
                    step="0.5"
                    value={remainingHours ?? ""}
                    onChange={(e) => {
                      const value = e.target.value;
                      setRemainingHours(
                        value === "" ? null : parseFloat(value)
                      );
                    }}
                    placeholder="例: 2.5"
                    bg={inputBg}
                    border="2px solid"
                    borderColor="gray.200"
                    _hover={{ borderColor: "gray.300" }}
                    _focus={{
                      borderColor: "gray.500",
                      boxShadow: "0 0 0 1px var(--chakra-colors-gray-500)",
                    }}
                    transition="all 0.2s"
                  />
                </FormControl>

                <FormControl flex="1">
                  <FormLabel
                    fontSize="md"
                    fontWeight="semibold"
                    color="gray.700"
                    mb={2}
                  >
                    <HStack spacing={2}>
                      <Icon as={StarIcon} color="gray.600" />
                      <Text>優先度</Text>
                    </HStack>
                  </FormLabel>
                  <RadioGroup
                    value={priority ?? ""}
                    onChange={(value) => setPriority(value as Priority)}
                  >
                    <HStack spacing={4}>
                      <Radio
                        value="high"
                        colorScheme="red"
                        size="lg"
                        _hover={{ transform: "scale(1.1)" }}
                        transition="transform 0.2s"
                      >
                        <Badge colorScheme="red" variant="subtle" px={2} py={1}>
                          高
                        </Badge>
                      </Radio>
                      <Radio
                        value="medium"
                        colorScheme="orange"
                        size="lg"
                        _hover={{ transform: "scale(1.1)" }}
                        transition="transform 0.2s"
                      >
                        <Badge colorScheme="orange" variant="subtle" px={2} py={1}>
                          中
                        </Badge>
                      </Radio>
                      <Radio
                        value="low"
                        colorScheme="green"
                        size="lg"
                        _hover={{ transform: "scale(1.1)" }}
                        transition="transform 0.2s"
                      >
                        <Badge colorScheme="green" variant="subtle" px={2} py={1}>
                          低
                        </Badge>
                      </Radio>
                    </HStack>
                  </RadioGroup>
                </FormControl>
              </HStack>

              <FormControl>
                <FormLabel
                  fontSize="md"
                  fontWeight="semibold"
                  color="gray.700"
                  mb={2}
                >
                  <HStack spacing={2}>
                    <Icon as={InfoIcon} color="gray.600" />
                    <Text>制約（自由文）</Text>
                  </HStack>
                </FormLabel>
                <Textarea
                  id="constraints"
                  value={constraints}
                  onChange={(e) => setConstraints(e.target.value)}
                  rows={3}
                  placeholder="制約やNG事項、落とし所などを記入してください..."
                  bg={inputBg}
                  border="2px solid"
                  borderColor="gray.200"
                  _hover={{ borderColor: "gray.300" }}
                  _focus={{
                    borderColor: "gray.500",
                    boxShadow: "0 0 0 1px var(--chakra-colors-gray-500)",
                  }}
                  transition="all 0.2s"
                />
              </FormControl>

              <Divider />

              <Button
                type="submit"
                size="lg"
                isLoading={isLoading}
                loadingText="生成中..."
                disabled={!requestText.trim()}
                width="full"
                bg="gray.600"
                color="white"
                _hover={{
                  bg: "gray.700",
                  transform: "translateY(-2px)",
                  boxShadow: "lg",
                }}
                _active={{
                  transform: "translateY(0)",
                }}
                _disabled={{
                  opacity: 0.5,
                  cursor: "not-allowed",
                }}
                transition="all 0.3s"
                fontWeight="bold"
                fontSize="lg"
                py={6}
              >
                {isLoading ? "生成中..." : "✨ 返信案を生成する"}
              </Button>
            </VStack>
          </form>
        </CardBody>
      </Card>

      {error && (
        <Alert
          status="error"
          borderRadius="xl"
          boxShadow="lg"
          className="slide-in"
        >
          <AlertIcon />
          <Box>
            <AlertTitle fontSize="lg" fontWeight="bold">
              エラーが発生しました
            </AlertTitle>
            <AlertDescription>
              {error.message}
              {error.statusCode && (
                <Badge ml={2} colorScheme="red" variant="subtle">
                  HTTP {error.statusCode}
                </Badge>
              )}
            </AlertDescription>
          </Box>
        </Alert>
      )}

      {isLoading && (
        <Card bg={cardBg} boxShadow="xl" borderRadius="2xl" className="fade-in">
          <CardBody p={8}>
            <VStack spacing={4}>
              <Spinner
                size="xl"
                thickness="4px"
                speed="0.65s"
                color="gray.600"
                emptyColor="gray.200"
              />
              <Text fontSize="lg" fontWeight="semibold" color="gray.600">
                返信案を生成しています...
              </Text>
              <Text fontSize="sm" color="gray.500">
                しばらくお待ちください
              </Text>
            </VStack>
          </CardBody>
        </Card>
      )}

      {replyDraft && (
        <Card
          bg={cardBg}
          boxShadow="xl"
          borderRadius="2xl"
          overflow="hidden"
          className="fade-in"
          _hover={{ boxShadow: "2xl", transform: "translateY(-2px)" }}
          transition="all 0.3s"
        >
          <CardHeader
            bg="teal.700"
            color="white"
            py={6}
          >
            <HStack spacing={3} justify="space-between">
              <HStack spacing={3}>
                <Icon as={CheckIcon} boxSize={6} />
                <Heading size="lg" fontWeight="bold">
                  生成された返信案
                </Heading>
              </HStack>
              <Badge colorScheme="teal" variant="subtle" fontSize="md" px={3} py={1}>
                完成
              </Badge>
            </HStack>
          </CardHeader>
          <CardBody p={6}>
            <VStack spacing={4} align="stretch">
              <Box
                p={6}
                bgGradient="linear(to-br, gray.50, gray.100)"
                borderRadius="xl"
                border="2px solid"
                borderColor="gray.200"
                minH="200px"
              >
                <Text
                  whiteSpace="pre-wrap"
                  lineHeight="1.8"
                  fontSize="md"
                  color="gray.800"
                  fontWeight="normal"
                >
                  {replyDraft.text}
                </Text>
              </Box>
              <Button
                leftIcon={<CopyIcon />}
                onClick={handleCopy}
                size="lg"
                width="full"
                bg="teal.600"
                color="white"
                _hover={{
                  bg: "teal.700",
                  transform: "translateY(-2px)",
                  boxShadow: "lg",
                }}
                _active={{
                  transform: "translateY(0)",
                }}
                transition="all 0.3s"
                fontWeight="bold"
                fontSize="md"
                py={6}
              >
                クリップボードにコピー
              </Button>
            </VStack>
          </CardBody>
        </Card>
      )}
    </Stack>
  );
}
