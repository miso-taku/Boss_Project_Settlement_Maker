/**
 * 返信案生成 API のリクエスト/レスポンス型定義。
 *
 * バックエンドの DTO（backend/src/settlement_maker/interface/dto/reply_drafts.py）
 * と整合性を保つ。
 */

/** 優先度（3段階） */
export type Priority = "high" | "medium" | "low";

/** 返信案生成 API のリクエスト body */
export interface GenerateReplyDraftsRequest {
  /** 依頼文（必須・非空） */
  request_text: string;
  /** 残り時間（時間単位）。任意。0以上。 */
  remaining_hours?: number | null;
  /** 優先度（high/medium/low）。任意。 */
  priority?: Priority | null;
  /** 制約（自由文）。任意。空文字可。 */
  constraints?: string;
}

/** 返信案 1 件（API レスポンス用） */
export interface ReplyDraftItem {
  /** 返信案の本文 */
  text: string;
}

/** 返信案生成 API のレスポンス body */
export interface GenerateReplyDraftsResponse {
  /** 返信案 1 件 */
  draft: ReplyDraftItem;
}

/** エラータイプ */
export type ErrorType =
  | "validation_error" // バリデーションエラー（400, 422）
  | "not_found" // リソース未找到（404）
  | "server_error" // サーバーエラー（500, 502, 503等）
  | "network_error" // ネットワークエラー（接続エラー、タイムアウト等）
  | "unknown_error"; // その他のエラー

/** API エラー情報 */
export interface ApiError {
  /** エラータイプ */
  type: ErrorType;
  /** エラーメッセージ（ユーザー向け） */
  message: string;
  /** HTTP ステータスコード（HTTP エラーの場合） */
  statusCode?: number;
  /** 元のエラーメッセージ（デバッグ用） */
  originalMessage?: string;
}
