/**
 * 返信案生成フォームコンポーネントのテスト。
 *
 * React Testing Library を使用して、フォームの表示・入力・状態管理・API呼び出し・返信案表示・コピー機能をテストする。
 */

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import ReplyForm from "../ReplyForm";
import { generateReplyDrafts } from "../../api/replyDrafts";
import { ApiErrorException } from "../../api/replyDrafts";
import type { ApiError, GenerateReplyDraftsResponse } from "../../api/types";

// API クライアント関数をモック（ApiErrorException は実際のクラスを使用）
jest.mock("../../api/replyDrafts", () => {
  const actual = jest.requireActual("../../api/replyDrafts");
  return {
    ...actual,
    generateReplyDrafts: jest.fn(),
  };
});

describe("ReplyForm", () => {
  let mockWriteText: jest.SpyInstance;

  beforeEach(() => {
    jest.clearAllMocks();
    // navigator.clipboard.writeText をモック（jest.setup.ts で設定済み）
    mockWriteText = jest.spyOn(navigator.clipboard, "writeText");
    mockWriteText.mockResolvedValue(undefined);
  });

  afterEach(() => {
    if (mockWriteText) {
      mockWriteText.mockRestore();
    }
  });

  it("各入力フィールドが表示される", () => {
    render(<ReplyForm />);

    expect(screen.getByLabelText(/依頼文/)).toBeInTheDocument();
    expect(screen.getByLabelText(/残り時間/)).toBeInTheDocument();
    expect(screen.getByText(/優先度/)).toBeInTheDocument();
    expect(screen.getByLabelText(/制約/)).toBeInTheDocument();
  });

  it("依頼文に入力できる", async () => {
    const user = userEvent.setup();
    render(<ReplyForm />);

    const textarea = screen.getByLabelText(/依頼文/);
    await user.type(textarea, "今日中に資料を作成してください");

    expect(textarea).toHaveValue("今日中に資料を作成してください");
  });

  it("残り時間に入力できる", async () => {
    const user = userEvent.setup();
    render(<ReplyForm />);

    const input = screen.getByLabelText(/残り時間/);
    await user.type(input, "1.5");

    expect(input).toHaveValue(1.5);
  });

  it("優先度を選択できる", async () => {
    const user = userEvent.setup();
    render(<ReplyForm />);

    const highRadio = screen.getByLabelText("高");
    await user.click(highRadio);

    expect(highRadio).toBeChecked();
  });

  it("制約に入力できる", async () => {
    const user = userEvent.setup();
    render(<ReplyForm />);

    const textarea = screen.getByLabelText(/制約/);
    await user.type(textarea, "最小限の範囲で対応したい");

    expect(textarea).toHaveValue("最小限の範囲で対応したい");
  });

  it("生成実行ボタンが表示される", () => {
    render(<ReplyForm />);

    expect(screen.getByRole("button", { name: /生成/ })).toBeInTheDocument();
  });

  it("生成実行ボタンをクリックすると API が呼び出される", async () => {
    const user = userEvent.setup();
    const mockResponse: GenerateReplyDraftsResponse = {
      drafts: [{ text: "返信案の本文" }],
    };
    (generateReplyDrafts as jest.Mock).mockResolvedValueOnce(mockResponse);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "今日中に資料を作成してください");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(generateReplyDrafts).toHaveBeenCalledWith({
        request_text: "今日中に資料を作成してください",
        remaining_hours: undefined,
        priority: undefined,
        constraints: undefined,
      });
    });
  });

  it("API レスポンスを受け取ると返信案が表示される", async () => {
    const user = userEvent.setup();
    const mockResponse: GenerateReplyDraftsResponse = {
      drafts: [{ text: "返信案の本文\n改行を含むテキスト" }],
    };
    (generateReplyDrafts as jest.Mock).mockResolvedValueOnce(mockResponse);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText(/返信案の本文/)).toBeInTheDocument();
    });
  });

  it("コピーボタンが表示される", async () => {
    const user = userEvent.setup();
    const mockResponse: GenerateReplyDraftsResponse = {
      drafts: [{ text: "返信案の本文" }],
    };
    (generateReplyDrafts as jest.Mock).mockResolvedValueOnce(mockResponse);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: /コピー/ })
      ).toBeInTheDocument();
    });
  });

  it("コピーボタンをクリックするとクリップボードにコピーされる", async () => {
    const user = userEvent.setup();
    const mockResponse: GenerateReplyDraftsResponse = {
      drafts: [{ text: "返信案の本文" }],
    };
    (generateReplyDrafts as jest.Mock).mockResolvedValueOnce(mockResponse);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: /コピー/ })
      ).toBeInTheDocument();
    });

    const copyButton = screen.getByRole("button", { name: /コピー/ });
    await user.click(copyButton);

    // コピー処理が完了するまで待機
    await waitFor(
      () => {
        expect(mockWriteText).toHaveBeenCalledWith("返信案の本文");
      },
      { timeout: 3000 }
    );
  });

  it("コピー成功時にフィードバックが表示される", async () => {
    const user = userEvent.setup();
    const mockResponse: GenerateReplyDraftsResponse = {
      drafts: [{ text: "返信案の本文" }],
    };
    (generateReplyDrafts as jest.Mock).mockResolvedValueOnce(mockResponse);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(
        screen.getByRole("button", { name: /コピー/ })
      ).toBeInTheDocument();
    });

    const copyButton = screen.getByRole("button", { name: /コピー/ });
    await user.click(copyButton);

    await waitFor(() => {
      expect(screen.getByText(/コピー済み/)).toBeInTheDocument();
    });
  });

  it("ローディング中にスピナーが表示される", async () => {
    const user = userEvent.setup();
    const mockResponse: GenerateReplyDraftsResponse = {
      drafts: [{ text: "返信案の本文" }],
    };
    // レスポンスを遅延させる
    (generateReplyDrafts as jest.Mock).mockImplementation(
      () =>
        new Promise((resolve) => {
          setTimeout(() => resolve(mockResponse), 100);
        })
    );

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    // ローディング中にスピナーが表示される
    await waitFor(() => {
      expect(screen.getByLabelText("読み込み中")).toBeInTheDocument();
    });

    // ローディング完了後にスピナーが非表示になる
    await waitFor(
      () => {
        expect(screen.queryByLabelText("読み込み中")).not.toBeInTheDocument();
      },
      { timeout: 200 }
    );
  });

  it("HTTP エラー（422: バリデーションエラー）時に適切なエラーメッセージが表示される", async () => {
    const user = userEvent.setup();
    const apiError: ApiError = {
      type: "validation_error",
      message: "入力内容に問題があります。入力値を確認してください。",
      statusCode: 422,
      originalMessage: "依頼文は空にできません",
    };
    const errorException = new ApiErrorException(apiError);
    (generateReplyDrafts as jest.Mock).mockRejectedValueOnce(errorException);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(screen.getByText(/入力内容に問題があります/)).toBeInTheDocument();
      expect(screen.getByText(/HTTP 422/)).toBeInTheDocument();
    });
  });

  it("HTTP エラー（500: サーバーエラー）時に適切なエラーメッセージが表示される", async () => {
    const user = userEvent.setup();
    const apiError: ApiError = {
      type: "server_error",
      message:
        "サーバーエラーが発生しました。しばらく時間をおいてから再度お試しください。",
      statusCode: 500,
      originalMessage: "Internal Server Error",
    };
    const errorException = new ApiErrorException(apiError);
    (generateReplyDrafts as jest.Mock).mockRejectedValueOnce(errorException);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(
        screen.getByText(/サーバーエラーが発生しました/)
      ).toBeInTheDocument();
      expect(screen.getByText(/HTTP 500/)).toBeInTheDocument();
    });
  });

  it("ネットワークエラー時にユーザーフレンドリーなメッセージが表示される", async () => {
    const user = userEvent.setup();
    const apiError: ApiError = {
      type: "network_error",
      message:
        "ネットワークエラーが発生しました。インターネット接続を確認してください。",
      originalMessage: "Network error",
    };
    const errorException = new ApiErrorException(apiError);
    (generateReplyDrafts as jest.Mock).mockRejectedValueOnce(errorException);

    render(<ReplyForm />);

    const requestTextarea = screen.getByLabelText(/依頼文/);
    await user.type(requestTextarea, "依頼文");

    const generateButton = screen.getByRole("button", { name: /生成/ });
    await user.click(generateButton);

    await waitFor(() => {
      expect(
        screen.getByText(/ネットワークエラーが発生しました/)
      ).toBeInTheDocument();
    });
  });
});
