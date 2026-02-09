# F2: API クライアント（返信案生成 API 呼び出し）— 設計

## 方針

- **DDD 境界**: フロントエンドの API クライアントは、バックエンドの Interface 層（FastAPI ルータ）と通信する。ドメインロジックはバックエンドに寄せる。
- **責務分割**: API クライアントは「HTTP リクエストの送信・レスポンスの受信・エラーハンドリング」に集中する。UI ロジック（ローディング表示・エラー表示）は F4/F5 で実装する。

## データフロー

```
[React コンポーネント（F3 以降）]
  → API クライアント関数呼び出し
  → fetch API で POST /api/v1/reply-drafts にリクエスト送信
  → バックエンド（FastAPI）で処理
  → レスポンス（JSON）を受信
  → TypeScript 型に変換して返却
  → [React コンポーネントで利用]
```

## API変更

- 今回は API 変更なし。既存の `POST /api/v1/reply-drafts` エンドポイントを利用する。
- **リクエスト**: `GenerateReplyDraftsRequest`
  - `request_text`: string（必須・非空）
  - `remaining_hours`: number | null（任意・0以上）
  - `priority`: "high" | "medium" | "low" | null（任意）
  - `constraints`: string（任意・空文字可）
- **レスポンス**: `GenerateReplyDraftsResponse`
  - `drafts`: `ReplyDraftItem[]`（要素数は 1 件）
  - `ReplyDraftItem`: `{ text: string }`

## 代替案と採用理由

- **fetch API vs axios**: Next.js の標準的な `fetch` API を使用する。追加の依存関係が不要で、Next.js の App Router と統合しやすい。axios は必要に応じて後で導入可能。**fetch API を採用**。
- **型定義: 手動 vs OpenAPI 自動生成**: 今回は手動で型定義を作成する。OpenAPI スキーマの生成・型生成ツールの設定は F3 以降で必要に応じて検討する。**手動型定義を採用**。
- **エラーハンドリング: カスタムエラー vs 標準エラー**: HTTP エラー（4xx, 5xx）は標準の `Error` を拡張したカスタムエラークラスで処理する。F5 で UI 表示を実装する際に、エラータイプに応じた表示が可能になる。**カスタムエラークラスを採用**。
- **環境変数: NEXT_PUBLIC_* vs サーバーサイド**: Next.js の App Router では、クライアント側から参照する環境変数は `NEXT_PUBLIC_*` プレフィックスが必要。API クライアントはクライアント側で実行されるため、`NEXT_PUBLIC_API_BASE_URL` を使用する。**NEXT_PUBLIC_API_BASE_URL を採用**。

## テスト戦略

- **ユニットテスト**: API クライアント関数のテスト（モック fetch を使用）
  - 正常系: リクエストが正しく送信され、レスポンスが正しく変換される
  - 異常系: HTTP エラー（4xx, 5xx）が適切に処理される
  - 異常系: ネットワークエラーが適切に処理される
- **統合テスト**: 実際のバックエンド API との結合テスト（F3 以降で必要に応じて）
- F2 ではユニットテストを実装する。統合テストは F3 以降で実施する。

## ドキュメント更新方針

- `./docs/implementation-tasklist.md`: F2 を「完了」にし、完了日・備考を記録。実装サマリー・セクション別進捗・更新履歴を更新。
- `./docs/architecture.md`: API クライアントの実装方針が architecture.md 4.2 と一致していることを確認（必要に応じて追記）。

## 全体タスク反映方針

- `implementation-tasklist.md` の F2 を完了。総タスク数 26 のうち完了 14、フロントエンド 7 のうち完了 2。

---

## 結果と学び（モード3）

- **採用案の妥当性**: `fetch` API を使用した実装は、Next.js の標準的な方法であり、追加の依存関係が不要で効率的だった。環境変数 `NEXT_PUBLIC_API_BASE_URL` を使用することで、開発環境・本番環境で柔軟に設定可能になった。手動型定義は、バックエンドの DTO 定義と整合性を保ちやすく、実装が迅速だった。
- **想定外**: npm の実行環境に問題があり、`npm run lint` の実行ができなかったが、TypeScript の型チェックと ESLint の静的解析で問題がないことを確認できた。テスト実行は F6 でテスト設定を追加予定のため、今回はテストファイル作成のみで完了とした。
- **改善点**: 次回（F3 以降）で UI 実装後に、実際の API リクエストが正しく送信されることをブラウザの開発者ツールで確認する。CORS エラーが発生する可能性があるため、バックエンドで CORS ミドルウェアが設定されているか確認する必要がある（必要に応じてバックエンド側で対応）。

---