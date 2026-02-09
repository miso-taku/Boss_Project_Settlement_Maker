/**
 * ローディングスピナーコンポーネント。
 *
 * CSS アニメーションで実装されたシンプルなスピナー。
 * グローバル CSS（globals.css）の `spin` アニメーションを使用する。
 */

export default function LoadingSpinner() {
  return (
    <div
      style={{
        display: "inline-block",
        width: "20px",
        height: "20px",
        border: "3px solid #f3f3f3",
        borderTop: "3px solid #0070f3",
        borderRadius: "50%",
        animation: "spin 1s linear infinite",
      }}
      role="status"
      aria-label="読み込み中"
    />
  );
}
