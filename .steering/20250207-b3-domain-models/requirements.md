# B3: 依頼文・自分の状況・返信案のドメインモデル — 要求

## 背景 / 目的

- **背景**: implementation-tasklist B2 で domain / application / infrastructure / interface のディレクトリ構成が完了。architecture 3.1 では Domain 層に「依頼文・自分の状況・返信案のドメインモデル（必要に応じて）」を置く方針。
- **目的**: 返信案生成フローで扱う入力・出力をドメイン型として定義し、B4 以降のユースケース・Port・API で一貫して利用できるようにする。

## スコープ（やること / やらないこと）

### やること

- 依頼文を表す値オブジェクト（RequestText）を定義
- 自分の状況を表す値オブジェクト（MySituation: 残り時間・優先度・制約）を定義
- 優先度を表す列挙（Priority: 3段階）を定義
- 返信案を表す値オブジェクト（ReplyDraft）を定義
- domain/__init__.py でエクスポート
- 用語は glossary に合わせる（依頼文・自分の状況・残り時間・優先度・制約・返信案）
- `./docs/implementation-tasklist.md` の B3 を完了に更新

### やらないこと

- チェック結果（CheckResult）の型定義（B4 で追加）
- ユースケース・Port・API の実装（B4, B6）
- PydanticAI エージェントの実装（B5）

## 受け入れ条件（Given-When-Then）

- **Given** architecture 3.1 の Domain 責務（エンティティ・値オブジェクト・ドメインルール、I/O 禁止）に従う
- **When** 依頼文・自分の状況・返信案のドメインモデルを実装する
- **Then** RequestText, MySituation, Priority, ReplyDraft が domain に存在し、他層から利用できる
- **And** 依頼文が空・空白のみの場合は RequestText 作成時に ValueError
- **And** 残り時間が負の場合は MySituation 作成時に ValueError

## 影響範囲

| 領域 | 内容 |
|------|------|
| FE | なし |
| BE | domain/models.py（新規）, domain/__init__.py（export 追加） |
| API | なし（B6 で DTO とマッピング） |
| DB | なし |
| Docs | implementation-tasklist.md の B3 を完了に更新 |

## 未決事項 / リスク / 仮定

- **仮定**: ドメインは dataclass（frozen）と Enum で表現。I/O は行わない。
- **仮定**: 優先度の値は "high" / "medium" / "low"（API や UI のラベル「高・中・低」と対応は B6/FE で行う）。
- 未決事項なし。

---

## 受け入れ条件チェック結果（作業完了時）

- **RequestText, MySituation, Priority, ReplyDraft**: domain/models.py に定義し、domain/__init__.py でエクスポート → **充足**。
- **依頼文が空・空白のみ**: RequestText の __post_init__ で ValueError（「依頼文は空にできません」）→ **充足**。
- **残り時間が負**: MySituation の __post_init__ で ValueError（「残り時間は0以上である必要があります」）→ **充足**。
- **implementation-tasklist.md**: B3 を完了に更新し、サマリー・進捗・更新履歴を反映 → **充足**。
- **ユニットテスト**: 事後追加で tests/unit/domain/test_models.py を追加（11 件）→ **充足**。
