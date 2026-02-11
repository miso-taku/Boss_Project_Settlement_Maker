---
name: steering-mode1-bootstrap
description: 新しい作業を始めるときに、.steering/[YYYYMMDD]-[task-name]/ を作り、requirements/design/tasklist をAGENTS準拠で初期化する
---

# Steering Mode1 Bootstrap

## Goal
- 作業の「要求」「設計」「タスク」を合意可能な形に固定する（モード1）。:contentReference[oaicite:3]{index=3}

## When to use
- 新規タスク開始時（バグ/機能/UI改善/調査を含む）
- 既存タスクでも意思決定が散らばりそうなとき

## Inputs you should ask first (minimum)
- task-name（kebab-case、目的が伝わる短い名前）
- 目的（1〜2行）
- 受け入れ条件（Given-When-Then で書ける粒度）
- 影響範囲（FE/BE/API/DB/Docs）

## Steps
1. `.steering/[YYYYMMDD]-[task-name]/` を作成する（同名があれば日付を変える）。:contentReference[oaicite:4]{index=4}
2. `requirements.md` を作成し、以下を必ず含める：背景/目的、スコープ、受け入れ条件、影響範囲、未決事項/リスク/仮定（※仮定は質問待ち）。:contentReference[oaicite:5]{index=5}
3. `design.md` を作成し、方針、データフロー、API変更、代替案、テスト戦略、docs更新方針、implementation-tasklist反映方針を書く。:contentReference[oaicite:6]{index=6}
4. `tasklist.md` をチェックボックスで作成（調査/Red/Green/アプリ/ルータ/FE/統合/lint/docs/implementation-tasklist/振り返り）。:contentReference[oaicite:7]{index=7}
5. 作業開始前に「目的/方針/影響範囲/テスト戦略/docs更新/ステアリング更新/全体タスクリスト更新」を必ず提示する。:contentReference[oaicite:8]{index=8}

## Output checklist
- [ ] `.steering/.../requirements.md` が「質問待ち」を明示している
- [ ] `.steering/.../design.md` に代替案がある
- [ ] `.steering/.../tasklist.md` が作業手順の正になっている
