# ExamAI-Portable（ポータブル版キット）使い方

ローカルAIと図表・スライド生成キットを、**インストールせずに1フォルダで持ち運ぶ**ための一式です。
フォルダごとコピーすれば、どのPCでも同じように動きます（レジストリやサービスは使いません）。

## フォルダ構成
- `00_Setup.bat` … 初回だけ実行。本体・モデル・Python一式をこのフォルダ内に取得し、検証まで行う
- `01_StartAI.bat` … AIサーバ起動（GPU版）。ブラウザが自動で開き、チャット画面になる
- `01b_StartAI_CPU.bat` … AIサーバ起動（CPU版）。GPUが使えないPCでの保険
- `02_MakeFigures.bat` … 図表と地図の画像を再生成する（kit\assets が更新される）
- `03_MakeDeckAndReport.bat` … スライド（PPTX）と報告書（DOCX）を組み立てる（kit\out に出力）
- `llama\` `llama-cpu\` `models\` `python\` … セットアップで中身が入る置き場
- `kit\scripts` … 生成スクリプト。当日はここの数値・文言を差し替える
- `kit\assets` … 図表・地図の画像とサンプルデータ（初期サンプル入り）
- `kit\out` … 組立済みサンプル（sample_deck.pptx / sample_report.docx）

## 準備（自宅などネットのある場所で）
1. このZIPを展開し、`00_Setup.bat` を実行する
   - ダウンロード合計は約20GB（モデル本体が約18.6GB）。空き容量は25GB以上を推奨
   - 終わりに「セットアップ完了: すべての検証に合格しました」と出ればOK
2. `01_StartAI.bat` を起動し、ブラウザのチャット画面で日本語の応答が出るか確認する
3. 機内モード（完全オフライン）でもう一度 01 を起動し、応答を確認する
4. フォルダごと、持込先のPCへコピーする

## 当日の流れ
1. `01_StartAI.bat` 起動 → ブラウザでAIに構成・文章・数表を作らせる
2. `kit\scripts` 内の数値・文言を課題に合わせて差し替え、`02_MakeFigures.bat` と `03_MakeDeckAndReport.bat` を実行
3. できた .pptx / .docx を PowerPoint / Word で開いて微調整し、最終確認する

## 困ったとき
- GPU版で起動しない／真っ黒なまま → `01b_StartAI_CPU.bat` を使う（速度は落ちるが動く。30B級でも活性パラメータが小さいモデルなので実用範囲）
- `00_Setup.bat` がポリシーで止まる → 手動でも同じことができます。README末尾の取得元URLからブラウザで落とし、`llama\`（CUDA版+cudartの両方）、`llama-cpu\`、`models\`、`python\` に展開してください。Pythonは展開後に `python312._pth` の `#import site` の `#` を外し、`python.exe get-pip.py` と `python.exe -m pip install python-pptx python-docx matplotlib geopandas scipy` を実行します
- ポート8080が使用中 → 01のbat内の `--port 8080` を 8081 などに変える

## 取得元（バージョン固定）
- llama.cpp b12069（GitHub: ggml-org/llama.cpp releases）
  - llama-b12069-bin-win-cuda-12.4-x64.zip / cudart-llama-bin-win-cuda-12.4-x64.zip / llama-b12069-bin-win-cpu-x64.zip
- モデル: unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF の Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf（18,556,686,752 bytes）
- Python 3.12.10 埋め込み版（python.org）

## 注意
- サンプルの数値・地名はすべて仮のもの。当日は課題の条件に差し替えること
- 図表には出典・前提（実データかサンプル表示か）を必ず明記すること
- モデルの応答は下書き用。数値と固有名詞は必ず自分で検算・確認すること
