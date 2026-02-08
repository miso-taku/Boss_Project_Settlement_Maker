# 仕様変更: 返信案チェックを10点満点×3項目・全て8以上でOK — 要求

## 背景 / 目的

- 現状、返信案チェックエージェントは「OK/NG＋指摘」の二値で判定している。
- **1〜3のチェック内容を10点満点で評価し、全てが8/10以上でなければ false として改善させる**ことで、判定基準を明確にし、作り直しの根拠を揃える。

## スコープ

### やること

- **仕様**: 返信案チェックの出力を「OK/NG＋指摘」から「3項目を各10点満点で評価し、全て8点以上でOK」に変更する。
  - チェック項目1: 角が立っていないか（丁寧さ・角の立たなさ）
  - チェック項目2: 代替案・確認質問が適切か
  - チェック項目3: 依頼文・制約に反していないか
  - 合格条件: 3項目すべてが 8 以上。1つでも 8 未満なら NG とし、作り直しエージェントに渡す。
- **永続ドキュメント**: architecture.md / functional-design.md / glossary.md を修正し、チェック基準（10点満点×3項目・全て8以上）を反映する。
- **バックエンド**: Domain の CheckResult に 3 スコアを追加、ok は「全スコア >= 8」で算出。Infrastructure の CheckResultSchema とチェックエージェントのプロンプトを変更する。
- **テスト**: ドメイン・アプリケーション・統合テストで CheckResult の新仕様に合わせる。
- **implementation-tasklist.md**: 本仕様変更を反映する。

### やらないこと

- API 契約の変更（返信案生成 API のリクエスト/レスポンスは変更しない。チェックは内部ロジックのみ）。
- フロントエンドの実装（未着手のため対象外）。
- チェック項目の追加・削除（3項目のまま）。

## 受け入れ条件

- **Given** 返信案チェックエージェントが返信案を評価する  
  **When** 3項目それぞれを0〜10でスコア付けする  
  **Then** 3項目すべてが 8 以上なら ok=true、1つでも 8 未満なら ok=false となる。

- **Given** ok=false のとき  
  **When** 作り直しエージェントに渡す  
  **Then** feedback に改善点が含まれ、作り直しに利用される。

- **Given** 永続ドキュメントを確認する  
  **When** 返信案チェックの記述を読む  
  **Then** 「10点満点で3項目を評価」「全て8以上で合格」と明記されている。

- 既存の pytest（unit + integration）がすべて通過する。

## 影響範囲

| 領域 | 内容 |
|------|------|
| BE Domain | CheckResult に score_1, score_2, score_3 追加、ok は派生 |
| BE Infrastructure | CheckResultSchema、PydanticAICheckAdapter のプロンプト・出力型 |
| BE Application | 変更なし（CheckResult.ok / .feedback の利用はそのまま） |
| BE Tests | CheckResult 生成箇所を新コンストラクタに合わせる |
| API | 変更なし（内部のみ） |
| Docs | architecture, functional-design, glossary, implementation-tasklist |

## 未決事項 / リスク / 仮定

- 仮定: スコアは 0〜10 の整数とする。LLM が範囲外を返した場合は Infrastructure 層でクランプするか、バリデーションで弾く（Domain では 0〜10 を前提に検証する）。

---

## 受け入れ条件チェック結果（モード3）

- **Given** 返信案チェックエージェントが返信案を評価する **When** 3項目それぞれを0〜10でスコア付けする **Then** 3項目すべてが 8 以上なら ok=true、1つでも 8 未満なら ok=false となる。 → **満たした**（Domain の ok プロパティで算出、CheckResultSchema で 0-10 を強制）。
- **Given** ok=false のとき **When** 作り直しエージェントに渡す **Then** feedback に改善点が含まれ、作り直しに利用される。 → **満たした**（Revise は check_result.feedback を参照、変更なし）。
- **Given** 永続ドキュメントを確認する **When** 返信案チェックの記述を読む **Then** 「10点満点で3項目を評価」「全て8以上で合格」と明記されている。 → **満たした**（architecture, functional-design, glossary を更新）。
- 既存の pytest（unit + integration）がすべて通過する。 → **満たした**（26 passed）。
