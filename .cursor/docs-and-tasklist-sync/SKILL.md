---
name: backend-new-feature-contract-first
description: 新機能を「契約→Domain→Usecase→FastAPI→FE」の順で実装し、互換性・docs・全体タスクを崩さない
---

# New Feature (Contract → BE → FE)

## Must-follow flow
1. **API契約（DTO/レスポンス）を先に定義**（必要ならdocsにも反映）。:contentReference[oaicite:18]{index=18}
2. **Domain仕様をテストで固定**（Red→Green→Refactor）。:contentReference[oaicite:19]{index=19}
3. Application（Usecase）実装：トランザクション境界はApplication。:contentReference[oaicite:20]{index=20}
4. FastAPI Routerは薄く：入力検証→DTO変換→Usecase→出力DTO。
5. FE（Next.js/React）実装：契約型があるならそれに追従。
6. 結合/統合テスト（必要最小）→lint/format→docs更新→implementation-tasklist更新→モード3振り返り。:contentReference[oaicite:21]{index=21}

## Guardrails
- DomainにI/O（DB/HTTP/ファイル/環境変数）を入れない。:contentReference[oaicite:22]{index=22}
- 破壊的変更は避け、やむを得ない場合は移行手順と段階導入を用意。:contentReference[oaicite:23]{index=23}

## Output checklist
- [ ] Domainテストが仕様の正
- [ ] DTOはInterface層で検証、DomainにPydanticを持ち込まない :contentReference[oaicite:24]{index=24}
- [ ] docs と implementation-tasklist が更新済み :contentReference[oaicite:25]{index=25}
