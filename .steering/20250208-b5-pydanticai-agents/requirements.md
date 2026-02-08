# B5: PydanticAI エージェント実装 — 要求

## 背景 / 目的

- **背景**: B4 で返信案生成ユースケースと AI 呼び出し Port（GenerateReplyDraftsPort, CheckReplyDraftsPort, ReviseReplyDraftsPort）が完了。Application 層からは Port 経由で AI を呼ぶ形になっている。次に Infrastructure 層で各 Port の具体実装として、PydanticAI を用いた 3 エージェント（生成・チェック・作り直し）を実装する必要がある。
- **目的**: architecture 3.5 に従い、生成・チェック・作り直しの 3 つの PydanticAI エージェントを実装し、各 Port を満たす Adapter を用意する。プロンプトとモデル（gpt-5-mini または API で利用可能な同等モデル）を設定する。

## スコープ（やること / やらないこと）

### やること

- Infrastructure 層に 3 つの Adapter を実装し、各 Port を満たす
  - **生成エージェント**: 依頼文＋自分の状況 → 返信案リスト（初稿）。プロンプトで「角の立たない断り・代替案・確認質問・次の一手」を指示
  - **チェックエージェント**: 返信案リスト＋依頼文・状況 → チェック結果（OK/NG＋指摘）。プロンプトでチェック基準（角の立たなさ・代替案の有無・制約違反の有無など）を指示
  - **作り直しエージェント**: 返信案＋チェック指摘＋依頼文・状況 → 返信案リスト（修正版）。プロンプトで指摘を反映して修正するよう指示
- モデルは architecture に従い gpt-5-mini を想定し、実装時に API で利用可能なモデル名に合わせる（例: gpt-4o-mini）。環境変数でモデル名を上書き可能とする。
- OpenAI API キーは環境変数で注入（OPENAI_API_KEY）
- `./docs/implementation-tasklist.md` の B5 を完了に更新

### やらないこと

- FastAPI ルータ・DTO・API 実装（B6 で実施）
- ドメイン/アプリケーション/API の自動テスト（B7 で実施）
- 認証・DB（本プロダクトでは不要）

## 受け入れ条件（Given-When-Then）

- **Given** B4 の Port（GenerateReplyDraftsPort, CheckReplyDraftsPort, ReviseReplyDraftsPort）とドメインモデル（RequestText, MySituation, ReplyDraft, CheckResult）が存在する
- **When** Infrastructure 層に 3 つの PydanticAI エージェントを実装する
- **Then** 各 Adapter が対応する Port を実装し、generate / check / revise の入出力がドメイン型と整合している
- **And** プロンプトで生成・チェック・作り直しの役割が明確に指示されている
- **And** モデル名は環境変数で上書き可能で、デフォルトは API で利用可能なモデル（例: gpt-4o-mini）とする
- **And** OpenAI API キーは環境変数から読み込む

## 影響範囲

| 領域 | 内容 |
|------|------|
| FE | なし |
| BE | infrastructure/（PydanticAI エージェント実装、3 Adapter）, pyproject.toml（openai 依存の追加が必要な場合） |
| API | なし（B6 で実施） |
| DB | なし |
| Docs | implementation-tasklist.md の B5 を完了に更新 |

## 未決事項 / リスク / 仮定

- **仮定**: モデル名は「gpt-5-mini」が API で未提供の場合は「gpt-4o-mini」をデフォルトとし、環境変数 `OPENAI_MODEL` で上書き可能とする（architecture の「実装時に API で利用可能なモデル名に合わせる」に従う）。
- **仮定**: PydanticAI の output_type には Pydantic BaseModel を用い、LLM 出力を Domain の ReplyDraft / CheckResult に変換して返す。
- **リスク**: OpenAI API キー未設定時は実行時エラーとなる。B6 以降で API 層で適切にハンドリングする。

---

## 受け入れ条件チェック結果（モード3）

- **3 Adapter が Port を実装**: PydanticAIGenerateAdapter, PydanticAICheckAdapter, PydanticAIReviseAdapter が各 Port の generate / check / revise を実装し、入出力がドメイン型と整合 → **充足**。
- **プロンプト**: 生成・チェック・作り直しの役割が各 system_prompt で明確に指示されている → **充足**。
- **モデル名**: OPENAI_MODEL 環境変数で上書き可能、デフォルト gpt-4o-mini → **充足**。
- **OpenAI API キー**: 環境変数から読み込み（PydanticAI/OpenAI プロバイダの既定動作）→ **充足**。
- **implementation-tasklist.md**: B5 を完了に更新し、サマリー・進捗・更新履歴を反映 → **充足**。
