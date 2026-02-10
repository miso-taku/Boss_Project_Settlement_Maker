/**
 * ホームページ（page.tsx）の統合テスト。
 *
 * React Testing Library を使用して、ページのレンダリング・ReplyForm の統合をテストする。
 * Chakra UIコンポーネントに対応。
 */

import { screen } from "@testing-library/react";
import { render } from "../../test-utils";
import Home from "../page";

// ReplyForm の API 呼び出しをモック（統合テストでは実際の API 呼び出しは行わない）
jest.mock("../../api/replyDrafts", () => ({
  generateReplyDrafts: jest.fn(),
  ApiErrorException: class ApiErrorException extends Error {},
}));

// useToast をモック
const mockToast = jest.fn();
jest.mock("@chakra-ui/react", () => {
  const actual = jest.requireActual("@chakra-ui/react");
  return {
    ...actual,
    useToast: () => ({
      toast: mockToast,
    }),
  };
});

describe("Home Page", () => {
  it("タイトルが表示される", () => {
    render(<Home />);

    expect(
      screen.getByText("上司案件・落とし所AIエージェント")
    ).toBeInTheDocument();
    expect(
      screen.getByText("「今日中に」を今日中にしないAI")
    ).toBeInTheDocument();
  });

  it("ReplyForm が統合されている", () => {
    render(<Home />);

    // ReplyForm の主要な要素が表示されることを確認
    expect(screen.getByLabelText(/依頼文/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /生成/ })).toBeInTheDocument();
  });
});
