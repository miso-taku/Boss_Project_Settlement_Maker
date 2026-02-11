---
name: docs-and-tasklist-sync
description: 仕様/設計/用語/規約の変更があるとき、./docs と implementation-tasklist をPR内で確実に更新する
---

# Docs & Tasklist Sync

## Why
- 永続ドキュメントは ./docs が正、変更があればコードと同一PRで必ず更新。:contentReference[oaicite:33]{index=33}
- 実装進捗の正は `./docs/implementation-tasklist.md`。完了時に必ず更新。:contentReference[oaicite:34]{index=34}

## Steps
1. 変更が「仕様/画面/API/制約/用語」に触れているか判定する。
2. 触れている場合、該当する docs を更新対象に列挙する（例：requirements / functional-design / architecture / glossary 等）。:contentReference[oaicite:35]{index=35}
3. 仕様が曖昧なら「勝手に確定せず」変更提案として追記案を作る（質問を添える）。:contentReference[oaicite:36]{index=36}
4. `./docs/implementation-tasklist.md` に、該当タスクの進捗/完了チェックを反映する。
5. 最終的に「更新したdocs一覧」を提出物に明記する。:contentReference[oaicite:37]{index=37}

## Output checklist
- [ ] docs更新が“同一差分”に含まれている
- [ ] 用語が増えたら glossary が更新されている
- [ ] implementation-tasklist が最新
