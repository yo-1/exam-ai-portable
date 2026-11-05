# -*- coding: utf-8 -*-
"""サンプルWord報告書: 見出し+本文+図+表の定型"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

BASE = os.path.join(os.path.dirname(__file__), "..")
A = os.path.join(BASE, "assets")
doc = Document()
for sec in doc.sections:
    sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.2)

st = doc.styles["Normal"]; st.font.name = "Yu Gothic"; st.font.size = Pt(11)
t = doc.add_paragraph(); t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("空間情報解析による地区別指標の可視化について（報告書サンプル）")
r.bold = True; r.font.size = Pt(16)

doc.add_heading("1. 目的", level=1)
doc.add_paragraph("本報告書は、GISを用いた空間情報解析の基本的な流れを確認するため、合成したサンプルデータにより地区別指標のコロプレスマップと標高段彩図を作成し、その読み取り結果を整理したものである。数値はすべて仮のものであり、実在の地域・統計とは関係しない。")
doc.add_heading("2. 使用データと方法", level=1)
doc.add_paragraph("地区ポリゴンはボロノイ分割により30地区を合成し、各地区に高齢化率を模した指標値を付与した。標高データは平滑化ノイズの重ね合わせにより400×400セルのDEMを合成し、段彩図と陰影起伏図を重ねて表示した。")
doc.add_heading("3. 結果", level=1)
doc.add_paragraph("地区別指標は東部で高く西部で低い傾向を示した（図1）。標高図では中央を南北に走る尾根筋と西側の平野部が明瞭に読み取れる（図2）。")
doc.add_picture(f"{A}/map_choropleth.png", width=Cm(13.5))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.add_run("図1 地区別 高齢化率の分布（サンプル）").font.size = Pt(10)
doc.add_picture(f"{A}/map_dem.png", width=Cm(13.5))
doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
cap = doc.add_paragraph(); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.add_run("図2 標高段彩図＋陰影起伏図（サンプル）").font.size = Pt(10)

doc.add_heading("4. 検証点の較差", level=1)
tbl = doc.add_table(rows=5, cols=4); tbl.style = "Table Grid"
rows = [("検証点", "平面較差(m)", "標高較差(m)", "判定"),
        ("TP-01", "0.012", "0.018", "合格"), ("TP-02", "0.021", "0.024", "合格"),
        ("TP-03", "0.008", "0.031", "合格"), ("TP-04", "0.017", "0.015", "合格")]
for i, row in enumerate(rows):
    for j, v in enumerate(row):
        tbl.rows[i].cells[j].text = v
doc.add_heading("5. 考察", level=1)
doc.add_paragraph("地図表現は分布の傾向把握に有効だが、階級区分の設定により印象が変化する。報告書では分類方法と出典を明記し、図と表を併用して数値の裏付けを示すことが求められる。")
out = os.path.join(BASE, "out", "sample_report.docx")
doc.save(out)
print("report saved:", out, os.path.getsize(out), "bytes")
