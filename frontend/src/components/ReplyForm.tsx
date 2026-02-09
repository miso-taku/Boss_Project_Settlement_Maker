"use client";

import { useState } from "react";
import type { ApiError, Priority, ReplyDraftItem } from "../api/types";
import { ApiErrorException, generateReplyDrafts } from "../api/replyDrafts";
import LoadingSpinner from "./LoadingSpinner";

/**
 * 返信案生成フォームコンポーネント。
 *
 * 依頼文・残り時間・優先度・制約を入力し、返信案を生成・表示・コピーする。
 */
export default function ReplyForm() {
  const [requestText, setRequestText] = useState("");
  const [remainingHours, setRemainingHours] = useState<number | null>(null);
  const [priority, setPriority] = useState<Priority | null>(null);
  const [constraints, setConstraints] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);
  const [replyDraft, setReplyDraft] = useState<ReplyDraftItem | null>(null);
  const [isCopied, setIsCopied] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setReplyDraft(null);
    setIsCopied(false);

    try {
      const response = await generateReplyDrafts({
        request_text: requestText,
        remaining_hours: remainingHours ?? undefined,
        priority: priority ?? undefined,
        constraints: constraints || undefined,
      });

      if (response.drafts.length > 0) {
        setReplyDraft(response.drafts[0]);
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
    } finally {
      setIsLoading(false);
    }
  };

  const handleCopy = async () => {
    if (!replyDraft) return;

    try {
      await navigator.clipboard.writeText(replyDraft.text);
      setIsCopied(true);
      // 3秒後に「コピー済み」表示をリセット
      setTimeout(() => {
        setIsCopied(false);
      }, 3000);
    } catch (err) {
      console.error("Copy error:", err);
      // フォールバック: テキストエリアを作成してコピー
      const textarea = document.createElement("textarea");
      textarea.value = replyDraft.text;
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
        setIsCopied(true);
        setTimeout(() => {
          setIsCopied(false);
        }, 3000);
      } catch (fallbackErr) {
        console.error("Fallback copy error:", fallbackErr);
      }
      document.body.removeChild(textarea);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="request-text">
          依頼文 <span style={{ color: "red" }}>*</span>
        </label>
        <textarea
          id="request-text"
          value={requestText}
          onChange={(e) => setRequestText(e.target.value)}
          rows={5}
          required
          style={{ width: "100%", padding: "8px" }}
        />
      </div>

      <div style={{ marginTop: "16px" }}>
        <label htmlFor="remaining-hours">残り時間（時間）</label>
        <input
          id="remaining-hours"
          type="number"
          min="0"
          step="0.5"
          value={remainingHours ?? ""}
          onChange={(e) => {
            const value = e.target.value;
            setRemainingHours(value === "" ? null : parseFloat(value));
          }}
          style={{ width: "100%", padding: "8px" }}
        />
      </div>

      <div style={{ marginTop: "16px" }}>
        <label>優先度</label>
        <div style={{ marginTop: "8px" }}>
          <label style={{ marginRight: "16px" }}>
            <input
              type="radio"
              name="priority"
              value="high"
              checked={priority === "high"}
              onChange={() => setPriority("high")}
            />
            高
          </label>
          <label style={{ marginRight: "16px" }}>
            <input
              type="radio"
              name="priority"
              value="medium"
              checked={priority === "medium"}
              onChange={() => setPriority("medium")}
            />
            中
          </label>
          <label>
            <input
              type="radio"
              name="priority"
              value="low"
              checked={priority === "low"}
              onChange={() => setPriority("low")}
            />
            低
          </label>
        </div>
      </div>

      <div style={{ marginTop: "16px" }}>
        <label htmlFor="constraints">制約（自由文）</label>
        <textarea
          id="constraints"
          value={constraints}
          onChange={(e) => setConstraints(e.target.value)}
          rows={3}
          style={{ width: "100%", padding: "8px" }}
        />
      </div>

      <div style={{ marginTop: "24px" }}>
        <button
          type="submit"
          disabled={isLoading || !requestText.trim()}
          style={{
            padding: "12px 24px",
            fontSize: "16px",
            backgroundColor: isLoading ? "#ccc" : "#0070f3",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor:
              isLoading || !requestText.trim() ? "not-allowed" : "pointer",
            display: "flex",
            alignItems: "center",
            gap: "8px",
          }}
        >
          {isLoading && <LoadingSpinner />}
          {isLoading ? "生成中..." : "生成実行"}
        </button>
      </div>

      {error && (
        <div
          style={{
            marginTop: "16px",
            padding: "12px",
            backgroundColor: "#fee",
            border: "1px solid #fcc",
            borderRadius: "4px",
            color: "#c00",
          }}
          role="alert"
          aria-live="polite"
        >
          <strong>エラー:</strong> {error.message}
          {error.statusCode && (
            <span style={{ fontSize: "12px", marginLeft: "8px" }}>
              (HTTP {error.statusCode})
            </span>
          )}
        </div>
      )}

      {replyDraft && (
        <div
          style={{
            marginTop: "24px",
            padding: "16px",
            backgroundColor: "#f5f5f5",
            border: "1px solid #ddd",
            borderRadius: "4px",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "12px" }}>返信案</h3>
          <div
            style={{
              whiteSpace: "pre-wrap",
              lineHeight: "1.6",
              marginBottom: "12px",
            }}
          >
            {replyDraft.text}
          </div>
          <button
            type="button"
            onClick={handleCopy}
            style={{
              padding: "8px 16px",
              fontSize: "14px",
              backgroundColor: isCopied ? "#28a745" : "#0070f3",
              color: "white",
              border: "none",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            {isCopied ? "コピー済み" : "コピー"}
          </button>
        </div>
      )}
    </form>
  );
}
