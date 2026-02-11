# 上司案件・落とし所AIエージェント - 開発サーバー起動スクリプト
# バックエンド（FastAPI）とフロントエンド（Next.js）をそれぞれ別ウィンドウで起動する。

$ProjectRoot = $PSScriptRoot
$BackendPath = Join-Path $ProjectRoot "backend"
$FrontendPath = Join-Path $ProjectRoot "frontend"

if (-not (Test-Path $BackendPath)) {
    Write-Error "backend フォルダが見つかりません: $BackendPath"
    exit 1
}
if (-not (Test-Path $FrontendPath)) {
    Write-Error "frontend フォルダが見つかりません: $FrontendPath"
    exit 1
}

Write-Host "バックエンド（FastAPI）を起動します..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$BackendPath'; Write-Host 'Backend (FastAPI) - http://localhost:8000' -ForegroundColor Green; uv run uvicorn settlement_maker.interface.app:app --reload"
)

Start-Sleep -Seconds 2

Write-Host "フロントエンド（Next.js）を起動します..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$FrontendPath'; Write-Host 'Frontend (Next.js) - http://localhost:3000' -ForegroundColor Green; npm run dev"
)

Write-Host ""
Write-Host "起動しました。各ウィンドウを閉じるとサーバーが停止します。" -ForegroundColor Yellow
Write-Host "  - バックエンド: http://localhost:8000" -ForegroundColor Gray
Write-Host "  - フロントエンド: http://localhost:3000" -ForegroundColor Gray
Write-Host "  - API ドキュメント: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "※ バックエンドで AI 生成を使う場合は、バックエンドのウィンドウで OPENAI_API_KEY を設定してください。" -ForegroundColor DarkGray
