# ExamAI-Portable セットアップ
# 本体・モデル・Python一式を「このフォルダの中」に取得します。PCへのインストールは行いません。
$ErrorActionPreference = 'Stop'
$Root = $PSScriptRoot
Write-Host "=== ExamAI-Portable セットアップ ==="
Write-Host "キットの場所: $Root"
if (-not (Test-Path (Join-Path $Root 'README_使い方.md'))) {
  Write-Host 'README_使い方.md が見つかりません。展開したフォルダの場所を確認してください。'
  exit 1
}

$Tag = 'b12069'
$ModelFile = 'Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf'
$ModelSize = 18556686752
$ModelUrl = "https://huggingface.co/unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF/resolve/main/$ModelFile"
$GhBase = "https://github.com/ggml-org/llama.cpp/releases/download/$Tag"

function Get-File($Url, $Dest, $Expected) {
  $Parent = Split-Path $Dest -Parent
  if (-not (Test-Path $Parent)) { New-Item -ItemType Directory $Parent -Force | Out-Null }
  if ((Test-Path $Dest) -and $Expected -gt 0 -and (Get-Item $Dest).Length -eq $Expected) {
    Write-Host "取得済みのため省略: $Dest"; return
  }
  Write-Host "ダウンロード中: $Url"
  & curl.exe -L -C - --retry 5 --retry-delay 5 -o $Dest $Url
  if ($LASTEXITCODE -ne 0) { throw "ダウンロード失敗: $Url" }
  if ($Expected -gt 0 -and (Get-Item $Dest).Length -ne $Expected) { throw "サイズ不一致: $Dest" }
}
function Expand-Into($Zip, $Dir) {
  if (-not (Test-Path $Dir)) { New-Item -ItemType Directory $Dir | Out-Null }
  Expand-Archive -Path $Zip -DestinationPath $Dir -Force
}

foreach ($d in @('llama', 'llama-cpu', 'models', 'python')) {
  if (-not (Test-Path (Join-Path $Root $d))) { New-Item -ItemType Directory (Join-Path $Root $d) -Force | Out-Null }
}
$Tmp = Join-Path $Root '_downloads'
if (-not (Test-Path $Tmp)) { New-Item -ItemType Directory $Tmp | Out-Null }

Write-Host '--- 1/4 llama.cpp (GPU版 + CUDAランタイム) ---'
Get-File "$GhBase/llama-$Tag-bin-win-cuda-12.4-x64.zip" (Join-Path $Tmp 'llama-cuda.zip') 286851724
Expand-Into (Join-Path $Tmp 'llama-cuda.zip') (Join-Path $Root 'llama')
Get-File "$GhBase/cudart-llama-bin-win-cuda-12.4-x64.zip" (Join-Path $Tmp 'cudart.zip') 391443627
Expand-Into (Join-Path $Tmp 'cudart.zip') (Join-Path $Root 'llama')
# DLLがサブフォルダに入った場合は llama 直下へ集める
$LlamaDir = Join-Path $Root 'llama'
Get-ChildItem $LlamaDir -Recurse -Filter '*.dll' | Where-Object { $_.DirectoryName -ne $LlamaDir } |
  Copy-Item -Destination $LlamaDir -Force

Write-Host '--- 2/4 llama.cpp (CPU版・保険) ---'
Get-File "$GhBase/llama-$Tag-bin-win-cpu-x64.zip" (Join-Path $Tmp 'llama-cpu.zip') 24609224
Expand-Into (Join-Path $Tmp 'llama-cpu.zip') (Join-Path $Root 'llama-cpu')

Write-Host '--- 3/4 モデル (約18.6GB、時間がかかります) ---'
Get-File $ModelUrl (Join-Path $Root "models\$ModelFile") $ModelSize

Write-Host '--- 4/4 Python 埋め込み版 + ライブラリ ---'
Get-File 'https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip' (Join-Path $Tmp 'python-embed.zip') 11133606
Expand-Into (Join-Path $Tmp 'python-embed.zip') (Join-Path $Root 'python')
$Pth = Join-Path $Root 'python\python312._pth'
(Get-Content $Pth) -replace '^#import site', 'import site' | Set-Content $Pth -Encoding ASCII
$Py = Join-Path $Root 'python\python.exe'
Get-File 'https://bootstrap.pypa.io/get-pip.py' (Join-Path $Tmp 'get-pip.py') 0
& $Py (Join-Path $Tmp 'get-pip.py') --no-warn-script-location
& $Py -m pip install --no-warn-script-location python-pptx python-docx matplotlib geopandas scipy

Write-Host '--- 検証 ---'
$ok = $true
if (-not (Test-Path (Join-Path $Root 'llama\llama-server.exe'))) { Write-Host 'NG: GPU版 llama-server.exe がありません'; $ok = $false }
if (-not (Test-Path (Join-Path $Root 'llama-cpu\llama-server.exe'))) { Write-Host 'NG: CPU版 llama-server.exe がありません'; $ok = $false }
if ((Get-Item (Join-Path $Root "models\$ModelFile")).Length -ne $ModelSize) { Write-Host 'NG: モデルのサイズが一致しません'; $ok = $false }
& $Py -c "import pptx, docx, matplotlib, geopandas, scipy; print('Python ライブラリ OK')"
if ($LASTEXITCODE -ne 0) { Write-Host 'NG: Python ライブラリの読み込みに失敗しました'; $ok = $false }
if ($ok) { Write-Host '=== セットアップ完了: すべての検証に合格しました ===' }
else { Write-Host '=== セットアップ不完全: 上の NG を確認してください ==='; exit 1 }
