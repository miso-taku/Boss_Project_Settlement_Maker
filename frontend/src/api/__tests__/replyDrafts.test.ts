/**
 * 返信案生成 API クライアントのテスト。
 *
 * fetch API をモックして、正常系・異常系をテストする。
 */

import { ApiErrorException, generateReplyDrafts } from "../replyDrafts";
import type { GenerateReplyDraftsRequest } from "../types";

// fetch をモック
global.fetch = jest.fn();

describe("generateReplyDrafts", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("正常系: リクエストが正しく送信され、レスポンスが正しく変換される", async () => {
    const mockResponse: { drafts: Array<{ text: string }> } = {
      drafts: [{ text: "返信案の本文" }],
    };

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
      remaining_hours: 1.5,
      priority: "high",
      constraints: "制約",
    };

    const result = await generateReplyDrafts(request);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/v1/reply-drafts"),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      }
    );

    expect(result).toEqual(mockResponse);
    expect(result.drafts).toHaveLength(1);
    expect(result.drafts[0].text).toBe("返信案の本文");
  });

  it("正常系: 任意フィールドが null または undefined の場合", async () => {
    const mockResponse: { drafts: Array<{ text: string }> } = {
      drafts: [{ text: "返信案の本文" }],
    };

    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
    };

    const result = await generateReplyDrafts(request);

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining("/api/v1/reply-drafts"),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(request),
      }
    );

    expect(result).toEqual(mockResponse);
  });

  it("異常系: HTTP エラー（422: バリデーションエラー）", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: "依頼文は空にできません" }),
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "",
    };

    try {
      await generateReplyDrafts(request);
      fail("Expected ApiErrorException to be thrown");
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("validation_error");
        expect(error.apiError.message).toBe("依頼文は空にできません");
        expect(error.apiError.statusCode).toBe(422);
      }
    }
  });

  it("異常系: HTTP エラー（404: リソース未找到）", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 404,
      json: async () => ({ detail: "リソースが見つかりません" }),
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
    };

    try {
      await generateReplyDrafts(request);
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("not_found");
        expect(error.apiError.message).toBe("リソースが見つかりません");
        expect(error.apiError.statusCode).toBe(404);
      }
    }
  });

  it("異常系: HTTP エラー（500: サーバーエラー）", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({ detail: "サーバーエラーが発生しました" }),
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
    };

    try {
      await generateReplyDrafts(request);
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("server_error");
        expect(error.apiError.message).toBe("サーバーエラーが発生しました");
        expect(error.apiError.statusCode).toBe(500);
      }
    }
  });

  it("異常系: HTTP エラー（500: 詳細メッセージなし）", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({}),
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
    };

    try {
      await generateReplyDrafts(request);
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("server_error");
        expect(error.apiError.message).toBe(
          "サーバーエラーが発生しました。しばらく時間をおいてから再度お試しください。"
        );
        expect(error.apiError.statusCode).toBe(500);
      }
    }
  });

  it("異常系: ネットワークエラー", async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(
      new Error("Network error")
    );

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
    };

    try {
      await generateReplyDrafts(request);
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("network_error");
        expect(error.apiError.message).toBe(
          "ネットワークエラーが発生しました。インターネット接続を確認してください。"
        );
        expect(error.apiError.originalMessage).toBe("Network error");
      }
    }
  });

  it("異常系: HTTP エラーで JSON パースに失敗した場合", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => {
        throw new Error("Invalid JSON");
      },
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "依頼文",
    };

    try {
      await generateReplyDrafts(request);
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("server_error");
        expect(error.apiError.statusCode).toBe(500);
      }
    }
  });

  it("異常系: バリデーションエラー（配列形式）", async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({
        detail: [
          {
            loc: ["body", "request_text"],
            msg: "依頼文は必須です",
            type: "value_error",
          },
          {
            loc: ["body", "remaining_hours"],
            msg: "残り時間は0以上である必要があります",
            type: "value_error",
          },
        ],
      }),
    });

    const request: GenerateReplyDraftsRequest = {
      request_text: "",
    };

    try {
      await generateReplyDrafts(request);
    } catch (error) {
      expect(error).toBeInstanceOf(ApiErrorException);
      if (error instanceof ApiErrorException) {
        expect(error.apiError.type).toBe("validation_error");
        expect(error.apiError.message).toContain("依頼文は必須です");
        expect(error.apiError.message).toContain(
          "残り時間は0以上である必要があります"
        );
        expect(error.apiError.statusCode).toBe(422);
      }
    }
  });
});
