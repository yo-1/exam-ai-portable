# -*- coding: utf-8 -*-
"""サンプルPPTX組立: タイトル帯+本文+画像/表の定型レイアウト (16:9)"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

BASE = os.path.join(os.path.dirname(__file__), "..")
A = os.path.join(BASE, "assets")
FONT = "Yu Gothic"
NAVY = RGBColor(0x1F, 0x3A, 0x52)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DARK = RGBColor(0x22, 0x22, 0x22)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def add_slide(title, note=""):
    s = prs.slides.add_slide(BLANK)
    band = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.95))
    band.fill.solid(); band.fill.fore_color.rgb = NAVY; band.line.fill.background()
    tb = s.shapes.add_textbox(Inches(0.5), Inches(0.14), Inches(12.3), Inches(0.7))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = title
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = WHITE; p.font.name = FONT
    if note:
        src = s.shapes.add_textbox(Inches(0.5), Inches(6.95), Inches(12.3), Inches(0.4))
        sp = src.text_frame.paragraphs[0]; sp.text = note
        sp.font.size = Pt(11); sp.font.color.rgb = RGBColor(0x66, 0x66, 0x66); sp.font.name = FONT
    return s

def bullets(s, items, left=0.55, top=1.35, width=5.6, size=17):
    tb = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5.4))
    tf = tb.text_frame; tf.word_wrap = True
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = "・" + it; p.font.size = Pt(size); p.font.name = FONT; p.font.color.rgb = DARK
        p.space_after = Pt(10)

def picture(s, path, left, top, width=None, height=None):
    kw = {}
    if width: kw["width"] = Inches(width)
    if height: kw["height"] = Inches(height)
    return s.shapes.add_picture(path, Inches(left), Inches(top), **kw)

# S1 表紙
s = prs.slides.add_slide(BLANK)
band = s.shapes.add_shape(1, 0, Inches(2.3), prs.slide_width, Inches(2.6))
band.fill.solid(); band.fill.fore_color.rgb = NAVY; band.line.fill.background()
tb = s.shapes.add_textbox(Inches(0.9), Inches(2.75), Inches(11.5), Inches(1.8))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "空間情報解析の基礎と活用事例"
p.font.size = Pt(40); p.font.bold = True; p.font.color.rgb = WHITE; p.font.name = FONT
p2 = tf.add_paragraph(); p2.text = "― GIS・測量データを用いた地域分析の流れ ―"
p2.font.size = Pt(22); p2.font.color.rgb = WHITE; p2.font.name = FONT
sub = s.shapes.add_textbox(Inches(0.9), Inches(5.4), Inches(11.5), Inches(0.6))
sp = sub.text_frame.paragraphs[0]; sp.text = "（サンプルデッキ：生成キットの動作確認用）"
sp.font.size = Pt(16); sp.font.name = FONT; sp.font.color.rgb = DARK

# S2 概要
s = add_slide("本日の流れ")
bullets(s, ["空間情報とは：位置に紐づくデータの総称",
            "データの種類：ベクタ（点・線・面）とラスタ（標高・画像）",
            "解析の型：重ね合わせ／バッファ／密度／標高解析",
            "事例：地区別指標の可視化と施設配置の検討",
            "まとめ：解析結果の読み方と注意点"], width=11.5, size=20)

# S3 標高解析
s = add_slide("解析例1：標高データ（DEM）の可視化", "出典：サンプルDEM（合成データ）から作成")
picture(s, f"{A}/map_dem.png", 0.55, 1.2, height=5.55)
bullets(s, ["DEMは地表面の標高を格子状に表したラスタデータ",
            "段彩図に陰影起伏図を重ねると地形の凹凸が読み取りやすい",
            "傾斜量図・流域解析など、防災や林地管理の下図になる"], left=8.6, width=4.3)

# S4 コロプレス
s = add_slide("解析例2：地区別指標のコロプレスマップ", "出典：サンプル地区ポリゴン（合成データ）に仮の指標値を付与")
picture(s, f"{A}/map_choropleth.png", 0.55, 1.2, height=5.55)
bullets(s, ["面データに統計値を結び付け、色の濃淡で分布を示す",
            "東部で高齢化率が高い傾向が一目で分かる（仮データ）",
            "階級区分の切り方で印象が変わる点に注意が必要"], left=8.6, width=4.3)

# S5 点分布
s = add_slide("解析例3：施設分布と到達圏の分析", "出典：サンプル点データ（合成データ）")
picture(s, f"{A}/map_points.png", 0.55, 1.2, height=5.55)
bullets(s, ["カーネル密度推定で施設の集中域を把握する",
            "破線円は施設から一定距離の到達圏（バッファ）",
            "空白域はサービス水準の検討対象になる"], left=8.6, width=4.3)

# S6 グラフ
s = add_slide("統計図表：森林率と測量実績")
picture(s, f"{A}/chart_bar.png", 0.45, 1.25, width=6.2)
picture(s, f"{A}/chart_line.png", 6.85, 1.25, width=6.2)

# S7 円グラフ+検証表
s = add_slide("土地利用構成と測量精度の検証")
picture(s, f"{A}/chart_pie.png", 0.45, 1.3, width=5.6)
rows = [("検証点", "平面較差(m)", "標高較差(m)", "判定"),
        ("TP-01", "0.012", "0.018", "合格"),
        ("TP-02", "0.021", "0.024", "合格"),
        ("TP-03", "0.008", "0.031", "合格"),
        ("TP-04", "0.017", "0.015", "合格")]
tbl_shape = s.shapes.add_table(5, 4, Inches(6.6), Inches(1.6), Inches(6.1), Inches(2.4))
tbl = tbl_shape.table
for r, row in enumerate(rows):
    for c, v in enumerate(row):
        cell = tbl.cell(r, c); cell.text = v
        for par in cell.text_frame.paragraphs:
            par.font.size = Pt(14); par.font.name = FONT
            par.alignment = PP_ALIGN.CENTER
            if r == 0: par.font.bold = True
note = s.shapes.add_textbox(Inches(6.6), Inches(4.3), Inches(6.1), Inches(1.6))
np_ = note.text_frame.paragraphs[0]
np_.text = "検証点4点すべてで較差が許容範囲内（仮の数値）。"
np_.font.size = Pt(15); np_.font.name = FONT; np_.font.color.rgb = DARK

# S8 まとめ
s = add_slide("まとめ")
bullets(s, ["空間情報解析は「重ねる・数える・比べる」が基本",
            "図表と地図は同じデータから相互に補い合う",
            "サンプル表示でも、出典と前提条件の明記が必須"], width=11.5, size=20)

out = os.path.join(BASE, "out", "sample_deck.pptx")
prs.save(out)
print("deck saved:", out, os.path.getsize(out), "bytes /", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
