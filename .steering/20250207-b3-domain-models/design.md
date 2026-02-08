# B3: 依頼文・自分の状況・返信案のドメインモデル — 設計

## 方針

- **DDD 境界**: Domain 層は I/O 禁止。エンティティ・値オブジェクト・ドメインルールのみ。用語は glossary に合わせる。
- **責務分割**: 依頼文・自分の状況・返信案は「値オブジェクト」として不変（frozen dataclass）で定義し、B4 のユースケース・Port の入出力型として使う。

## ドメインモデル一覧

| 型 | 種別 | 説明 | 主なフィールド・ルール |
|----|------|------|------------------------|
| **Priority** | 列挙 | 優先度（3段階） | HIGH, MEDIUM, LOW（値: "high", "medium", "low"） |
| **RequestText** | 値オブジェクト | 依頼文 | value: str。空・空白のみは不可（ValueError） |
| **MySituation** | 値オブジェクト | 自分の状況 | remaining_hours: float \| None, priority: Priority \| None, constraints: str。残り時間は 0 以上（負は ValueError） |
| **ReplyDraft** | 値オブジェクト | 返信案（1件） | text: str |

## 配置

- **backend/src/settlement_maker/domain/models.py** に上記 4 つを定義。
- **backend/src/settlement_maker/domain/__init__.py** で RequestText, MySituation, Priority, ReplyDraft を __all__ に含めてエクスポート。

## バリデーションルール

- **RequestText**: `not value or not value.strip()` のとき ValueError「依頼文は空にできません」。
- **MySituation**: `remaining_hours is not None and remaining_hours < 0` のとき ValueError「残り時間は0以上である必要があります」。
- **ReplyDraft**: 特になし（空文字も許容。AI 出力をそのまま載せる想定）。

## テスト戦略

- B3 実施時点ではユニットテストは未作成（タスクは「必要に応じて」のため）。
- 事後に対応要望があり、tests/unit/domain/test_models.py を追加。Priority / RequestText / MySituation / ReplyDraft の正常・異常系を 11 件でカバー。

## ドキュメント更新方針

- `./docs/implementation-tasklist.md`: B3 を「完了」にし、完了日・備考（domain/models.py: RequestText, MySituation, Priority, ReplyDraft）を記録。実装サマリー・セクション別進捗・更新履歴を更新。

---

## 結果と学び（作業完了時）

- **採用案の妥当性**: 4 つの型を 1 ファイル（models.py）にまとめ、frozen dataclass と Enum で表現。B4 のユースケース・Port でそのまま引数・戻り値に利用できている。
- **想定外**: 当初はユニットテスト未実施だったが、後から TDD/ユニットテストの要望で tests/unit/domain/test_models.py を追加。11 件すべてパス。
- **改善点**: 今後ドメイン追加時は B7 方針に合わせ、可能なら TDD（テスト先行または実装と同時）でユニットテストを書く。
