/**
 * 返信案生成 API クライアント。
 *
 * POST /api/v1/reply-drafts エンドポイントを呼び出す。
 */

import type {
  ApiError,
  ErrorType,
  GenerateReplyDraftsRequest,
  GenerateReplyDraftsResponse,
} from "./types";

/** API のベース URL（環境変数から取得、デフォルト: http://localhost:8000） */
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

/** API エンドポイント */
const REPLY_DRAFTS_ENDPOINT = `${API_BASE_URL}/api/v1/reply-drafts`;

/**
 * HTTP ステータスコードからエラータイプを判定する。
 *
 * @param statusCode - HTTP ステータスコード
 * @returns エラータイプ
 */
function getErrorTypeFromStatusCode(statusCode: number): ErrorType {
  if (statusCode === 404) {
    return "not_found";
  }
  if (statusCode >= 400 && statusCode < 500) {
    return "validation_error";
  }
  if (statusCode >= 500) {
    return "server_error";
  }
  return "unknown_error";
}

/**
 * エラータイプからユーザーフレンドリーなメッセージを生成する。
 *
 * @param type - エラータイプ
 * @param detail - API からの詳細メッセージ（オプション）
 * @param statusCode - HTTP ステータスコード（オプション）
 * @returns ユーザーフレンドリーなメッセージ
 */
function getUserFriendlyMessage(
  type: ErrorType,
  detail?: string,
  statusCode?: number
): string {
  if (detail) {
    // API からの詳細メッセージがある場合はそれを優先
    return detail;
  }

  switch (type) {
    case "validation_error":
      return "入力内容に問題があります。入力値を確認してください。";
    case "not_found":
      return "リソースが見つかりませんでした。";
    case "server_error":
      return "サーバーエラーが発生しました。しばらく時間をおいてから再度お試しください。";
    case "network_error":
      return "ネットワークエラーが発生しました。インターネット接続を確認してください。";
    default:
      return "エラーが発生しました。しばらく時間をおいてから再度お試しください。";
  }
}

/**
 * HTTP エラーから ApiError オブジェクトを作成する。
 *
 * @param response - HTTP レスポンス
 * @returns ApiError オブジェクト
 */
async function createApiErrorFromResponse(
  response: Response
): Promise<ApiError> {
  const statusCode = response.status;
  const type = getErrorTypeFromStatusCode(statusCode);
  let detail: string | undefined;

  try {
    const errorBody = await response.json();
    if (errorBody.detail) {
      // FastAPI のエラーレスポンス形式: {"detail": "..."} または {"detail": [...]}
      if (typeof errorBody.detail === "string") {
        detail = errorBody.detail;
      } else if (Array.isArray(errorBody.detail)) {
        // バリデーションエラーの配列形式: [{"loc": [...], "msg": "...", "type": "..."}]
        const messages = errorBody.detail
          .map((item: { msg?: string }) => item.msg)
          .filter((msg: string | undefined): msg is string => !!msg);
        detail = messages.length > 0 ? messages.join(" ") : undefined;
      }
    }
  } catch {
    // JSON パースエラーは無視（デフォルトメッセージを使用）
  }

  const message = getUserFriendlyMessage(type, detail, statusCode);

  return {
    type,
    message,
    statusCode,
    originalMessage: detail || `HTTP error! status: ${statusCode}`,
  };
}

/**
 * ネットワークエラーから ApiError オブジェクトを作成する。
 *
 * @param error - エラーオブジェクト
 * @returns ApiError オブジェクト
 */
function createApiErrorFromNetworkError(error: unknown): ApiError {
  const message =
    error instanceof Error
      ? error.message
      : "ネットワークエラーが発生しました。";

  return {
    type: "network_error",
    message: getUserFriendlyMessage("network_error"),
    originalMessage: message,
  };
}

/**
 * ApiError を Error オブジェクトに変換する（後方互換性のため）。
 *
 * @param apiError - ApiError オブジェクト
 * @returns Error オブジェクト
 */
export class ApiErrorException extends Error {
  public readonly apiError: ApiError;

  constructor(apiError: ApiError) {
    super(apiError.message);
    this.name = "ApiErrorException";
    this.apiError = apiError;
  }
}

/**
 * 返信案を生成する。
 *
 * @param request - 依頼文と自分の状況
 * @returns 返信案リスト
 * @throws {ApiErrorException} HTTP エラーまたはネットワークエラーが発生した場合
 */
export async function generateReplyDrafts(
  request: GenerateReplyDraftsRequest
): Promise<GenerateReplyDraftsResponse> {
  try {
    const response = await fetch(REPLY_DRAFTS_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      // HTTP エラー（4xx, 5xx）
      const apiError = await createApiErrorFromResponse(response);
      throw new ApiErrorException(apiError);
    }

    const data: GenerateReplyDraftsResponse = await response.json();
    return data;
  } catch (error) {
    // ApiErrorException の場合はそのまま再スロー
    if (error instanceof ApiErrorException) {
      throw error;
    }

    // ネットワークエラーまたはその他のエラー
    const apiError = createApiErrorFromNetworkError(error);
    throw new ApiErrorException(apiError);
  }
}
