# フロントエンド仕様変更（React → React/Next.js）ドキュメント修正まとめ

フロントエンドを **React** から **React/Next.js** に変更し、**ルーティングは App Router を採用**する際の、ドキュメント修正内容は **ADR として正式に記録**しています。

---

## 決定事項（要約）

- **フロントエンド**: React → **React/Next.js**
- **ルーティング**: **App Router** を採用（Pages Router は採用しない）
- **ADR の管理**: `docs/adr/` で一元管理

---

## 詳細・修正一覧

**詳細な決定理由と、ファイルごとの修正内容（修正前・修正後）は次の ADR に記載しています。**

- **[ADR-0003: フロントエンドを React から React/Next.js（App Router）へ変更](adr/adr-0003-フロントエンドReactからNext.js-App-Routerへ.md)**

  - 決定事項（フロント技術変更・App Router 採用・ADR の管理場所）
  - 結果・影響
  - **付録: ドキュメント修正一覧**（architecture.md、product-requirements.md、repository-structure.md、implementation-tasklist.md、development-guidelines.md、glossary.md、AGENTS.md、README.md 等の修正箇所）

永続ドキュメントを実際に更新する際は、上記 ADR-0003 の「付録: ドキュメント修正一覧」に従ってください。

---

## 関連 ADR

| ADR | 内容 |
|-----|------|
| [ADR-0001](adr/adr-0001-上司案件落とし所AIエージェント要件決定.md) | 上司案件・落とし所AIエージェント 要件決定（FE 技術の変更は ADR-0003 で追記） |
| [ADR-0002](adr/adr-0002-複数AIエージェント生成チェック作り直しフロー.md) | 複数 AI エージェント（生成→チェック→作り直し）フロー採用 |
| [ADR-0003](adr/adr-0003-フロントエンドReactからNext.js-App-Routerへ.md) | フロントエンド React → React/Next.js（App Router）・ドキュメント修正一覧 |
