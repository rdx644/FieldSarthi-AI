"""Build and render the one-page submission pitch from its Markdown source."""
import re
import shutil
from pathlib import Path

import pymupdf as fitz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

ROOT=Path(__file__).resolve().parents[1]
target=ROOT/'output/pdf';target.mkdir(parents=True,exist_ok=True)
pdf=target/'FieldSaarthi_AI_Solution_Pitch.pdf'
styles={
    'title':ParagraphStyle('title',fontName='Helvetica-Bold',fontSize=27,leading=31,textColor=colors.HexColor('#1c4034'),spaceAfter=9),
    'subtitle':ParagraphStyle('subtitle',fontName='Helvetica',fontSize=13,leading=18,textColor=colors.HexColor('#50753c'),spaceAfter=14),
    'body':ParagraphStyle('body',fontName='Helvetica',fontSize=9.6,leading=14.3,textColor=colors.HexColor('#354a35'),spaceAfter=11),
}
story=[]
source=(ROOT/'docs/submission/solution-pitch.md').read_text(encoding='utf-8')
source=re.sub(r'(?m)^(#{1,2} .*)$',r'\n\n\1\n\n',source)
for block in source.strip().split('\n\n'):
    if not block.strip():continue
    block=block.strip()
    if block.startswith('# '):style='title';block=block[2:]
    elif block.startswith('## '):style='subtitle';block=block[3:]
    else:style='body'
    block=re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',block)
    block=block.replace('  \n','<br/>').replace('\n',' ')
    story.append(Paragraph(block,styles[style]))
doc=SimpleDocTemplate(str(pdf),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=44,bottomMargin=40,
                      title='FieldSaarthi AI - One-page solution pitch',
                      author='Shubham Putitundi and Shambhavi Kumar')
doc.build(story)
with fitz.open(pdf) as rendered:
    assert len(rendered)==1, 'Pitch must fit exactly one page'
    rendered[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(ROOT/'docs/evidence/solution-pitch-preview.png')
shutil.copyfile(pdf,ROOT/'docs/submission/solution-pitch.pdf')
print('One-page pitch generated, page count verified, and PNG rendered for visual review.')
