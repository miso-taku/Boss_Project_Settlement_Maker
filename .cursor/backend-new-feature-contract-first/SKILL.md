---
name: backend-bugfix-tdd
description: FastAPIバックエンドのバグ修正をTDDで進め、docs/steering/implementation-tasklistまで確実に整合させる
---

# Backend Bugfix (TDD)

## Principles
- テストが仕様（まず失敗する再現テスト）:contentReference[oaicite:9]{index=9}
- 小さく変更（最小差分で直す）:contentReference[oaicite:10]{index=10}

## Steps (must follow)
1. **再現テストを書く（Red）**：Domain層で書けるなら最優先でDomainテストに落とす。:contentReference[oaicite:11]{index=11}
2. **最小修正（Green）**：振る舞いを直す最小の変更だけ入れる。
3. **回帰テスト + リファクタ（Refactor）**：重複除去/命名改善、振る舞い変更なし。:contentReference[oaicite:12]{index=12}
4. API層・FE層への波及が必要なら「必要最小」で追従（契約を壊さない）。:contentReference[oaicite:13]{index=13}
5. 仕様に影響するなら `./docs` を同一PRで更新。:contentReference[oaicite:14]{index=14}
6. `./docs/implementation-tasklist.md` を進捗の正として必ず更新。:contentReference[oaicite:15]{index=15}
7. `.steering` をモード3で振り返り更新（受け入れ条件の達成結果・学び）。:contentReference[oaicite:16]{index=16}

## Output (final message should include)
- 何を変えたか / なぜ / 影響範囲 / 追加テスト / 更新docs / 更新steering / 更新implementation-tasklist / 実行コマンド :contentReference[oaicite:17]{index=17}
