# リポジトリ構造定義書（Repository Structure）

本プロダクト「上司案件・落とし所AIエージェント」のリポジトリ構成の目標形。実装に合わせて更新する。

---

## 1. ルート直下

```
Boss_Project_Settlement_Maker/
├── .gitignore
├── AGENTS.md              # AI/開発の最優先ルール
├── idea.md                # プロダクトアイデア（参照用）
├── README.md              # プロジェクト概要・起動方法（必要に応じて作成）
├── backend/               # バックエンド（FastAPI）
├── frontend/              # フロントエンド（Next.js, App Router）
├── docs/                  # 永続ドキュメント
└── .steering/             # 作業単位のステアリング（要求・設計・タスク・振り返り）
```

---

## 2. docs/（永続ドキュメント）

```
docs/
├── product-requirements.md    # プロダクト要求定義書
├── functional-design.md       # 機能設計書
├── architecture.md            # 技術仕様書
├── repository-structure.md    # 本ドキュメント（リポジトリ構造）
├── development-guidelines.md  # 開発ガイドライン
├── glossary.md                # ユビキタス言語定義
├── implementation-tasklist.md # 実装全体のタスクリスト（全体進捗の正）
├── doc-update-summary-react-to-nextjs.md  # FE 仕様変更時の修正まとめ（詳細は adr/ADR-0003）
└── adr/                       # Architecture Decision Records
    ├── adr-0001-上司案件落とし所AIエージェント要件決定.md
    ├── adr-0002-複数AIエージェント生成チェック作り直しフロー.md
    └── adr-0003-フロントエンドReactからNext.js-App-Routerへ.md
```

---

## 3. backend/（FastAPI）

DDD 方針に従い、Domain / Application / Infrastructure / Interface を分離する。

```
backend/
├── pyproject.toml / requirements.txt   # 依存管理（uv 想定）
├── src/
│   └── settlement_maker/               # パッケージ名は実装時に確定
│       ├── __init__.py
│       ├── domain/                     # ドメイン層（I/O禁止）
│       │   ├── __init__.py
│       │   └── ...                     # エンティティ・値オブジェクト等
│       ├── application/                # アプリケーション層（ユースケース）
│       │   ├── __init__.py
│       │   ├── generate_reply_drafts.py # 返信案生成（生成→チェック→作り直し）
│       │   ├── get_calendar_situation.py # カレンダーから自分の状況を取得
│       │   ├── ports.py                 # Port 定義（生成・チェック・作り直し・カレンダー）
│       │   └── ...                     # その他
│       ├── infrastructure/             # インフラ層（Adapter）
│       │   ├── __init__.py
│       │   ├── pydantic_ai_adapters.py # 返信案生成・チェック・作り直しの PydanticAI 実装
│       │   ├── calendar_mcp_adapter.py # Google Calendar 予定取得（MCP mcp-google）
│       │   └── ...                     # その他
│       └── interface/                  # プレゼンテーション層（FastAPI）
│           ├── __init__.py
│           ├── routes/                 # ルータ
│           ├── dto/                    # リクエスト/レスポンス DTO
│           └── ...
├── tests/                              # テスト
│   ├── unit/
│   ├── integration/
│   └── ...
└── ...
```

- 既存のディレクトリ構成がある場合はそちらに従う。勝手に新構成へ移行しない。

---

## 4. frontend/（Next.js, App Router）

```
frontend/
├── package.json
├── (pnpm-lock.yaml | package-lock.json | yarn.lock)
├── next.config.js          # または next.config.mjs / next.config.ts
├── src/
│   ├── app/                # App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── ...
│   ├── api/                # API クライアント集約
│   ├── components/
│   ├── hooks/
│   └── ...
├── public/
└── ...
```

- Next.js の **App Router** を採用する。ルーティングは `app/` 配下で行う。
- 既存のフロント構成がある場合はそちらに従う。

---

## 5. .steering/（ステアリング）

```
.steering/
└── YYYYMMDD-task-name/      # 例: 20250207-initial-docs
    ├── requirements.md     # 要求（背景・スコープ・受け入れ条件）
    ├── design.md           # 設計（方針・API・テスト戦略）
    └── tasklist.md         # タスクリスト（チェックボックス）
```

- 命名規則: `YYYYMMDD-task-name`（task-name は kebab-case）。
- 作業完了時に振り返りを追記し、`docs/implementation-tasklist.md` を更新する。

---

## 6. 更新方針

- ディレクトリ・ファイルの追加・削除・移動が発生したら、本ドキュメントをコード変更と同一PRで更新する。
- 実装開始後、実際の構成に合わせて本定義を合わせる。

---

## 7. 参照

- [AGENTS.md](../AGENTS.md) — ステアリング・永続ドキュメント一覧
- [architecture.md](architecture.md) — レイヤ責務・技術スタック
