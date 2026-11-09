"""Build the downloadable resume from the reviewed UTF-8 Markdown source.

Dependencies: python-docx, reportlab. Fonts default to Windows Arial; set
RESUME_FONT_DIR to a directory containing arial.ttf and arialbd.ttf elsewhere.
"""
from __future__ import annotations

import html
import os
import re
import shutil
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-11-09'
ASSETS = ROOT / 'assets'
FONT_DIR = Path(os.environ.get('RESUME_FONT_DIR', r'C:\Windows\Fonts'))
SOURCE = ROOT / 'resume.md'


def blocks():
    text = SOURCE.read_text(encoding='utf-8')
    result = []
    section = ''
    for raw in text.split('\n\n'):
        raw = raw.strip()
        if not raw:
            continue
        if raw.startswith('# '):
            result.append(('title', raw[2:], False))
        elif raw.startswith('## '):
            section = raw[3:]
            result.append(('h1', section, False))
        elif raw.startswith('### '):
            title = raw[4:]
            new_page = title.startswith(('Loyalty Platform', 'Dozhimator'))
            result.append(('h2', title, new_page))
        elif not section and raw.startswith('**'):
            result.append(('subtitle', raw.strip('*'), False))
        elif not section:
            lines = [line.strip() for line in raw.splitlines()]
            result.append(('contact', lines[0] + '  |  ' + lines[1], False))
            result.append(('contact', lines[2] + '  |  ' + lines[3], False))
        elif raw.startswith('- '):
            for line in raw.splitlines():
                result.append(('bullet', line.removeprefix('- ').strip(), False))
        elif raw.startswith(('**Стек:', '**Направления:')):
            result.append(('stack', raw, False))
        elif section == 'Технические навыки':
            result.append(('skill', raw, False))
        else:
            for line in raw.splitlines():
                result.append(('body', line.strip(), False))
    return result


def rich(text):
    text = html.escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'(https://[^\s<]+)', r'<link href="\1" color="#000000">\1</link>', text)
    return text


def add_docx_runs(paragraph, text):
    for part in re.split(r'(\*\*.*?\*\*)', text):
        if not part:
            continue
        run = paragraph.add_run(part[2:-2] if part.startswith('**') else part)
        run.bold = part.startswith('**')


def make_docx(items, path):
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    section.top_margin = section.bottom_margin = Inches(.56)
    section.left_margin = section.right_margin = Inches(.60)
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = Pt(14)
    normal.paragraph_format.space_after = Pt(2)
    for name, size, before, after in [('Title',24,0,4),('Subtitle',11.2,0,7),('Heading 1',13,9,4),('Heading 2',11.3,6,2)]:
        style = doc.styles[name]
        style.font.name = 'Arial'
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0,0,0)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.line_spacing = Pt(size + 3)
        style.paragraph_format.keep_with_next = True
    for kind, text, new_page in items:
        style = {'title':'Title','subtitle':'Subtitle','h1':'Heading 1','h2':'Heading 2'}.get(kind,'Normal')
        p = doc.add_paragraph(style=style)
        if new_page:
            p.paragraph_format.page_break_before = True
        if kind == 'bullet':
            p.paragraph_format.left_indent = Pt(10)
            p.paragraph_format.first_line_indent = Pt(-8)
            p.add_run('• ')
            p.paragraph_format.space_after = Pt(1.5)
        if kind in ('contact','skill','stack'):
            size = {'contact':9.3,'skill':10.1,'stack':9.3}[kind]
            p.paragraph_format.line_spacing = Pt(size+2.7)
            p.paragraph_format.space_after = Pt(2 if kind != 'stack' else 5)
        add_docx_runs(p,text)
        if kind in ('contact','skill','stack'):
            for run in p.runs:
                run.font.size = Pt(size)
        if kind == 'contact':
            # Word auto-link recognition is not required for the PDF counterpart.
            p.paragraph_format.keep_with_next = True
    footer = section.footer.paragraphs[0]
    footer.alignment = 2
    run = footer.add_run()
    run.font.name = 'Arial'
    run.font.size = Pt(8)
    field = OxmlElement('w:fldSimple')
    field.set(qn('w:instr'),'PAGE')
    run._r.addnext(field)
    doc.core_properties.title = 'Максим Асатуров Fullstack-разработчик'
    doc.core_properties.author = 'Максим Асатуров'
    doc.core_properties.subject = 'Backend, AI-интеграции и автоматизация'
    doc.save(path)


def make_pdf(items, path):
    pdfmetrics.registerFont(TTFont('Arial',str(FONT_DIR/'arial.ttf')))
    pdfmetrics.registerFont(TTFont('ArialBold',str(FONT_DIR/'arialbd.ttf')))
    pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
    base = dict(fontName='Arial',fontSize=11,leading=14,textColor=colors.black,alignment=TA_LEFT,spaceAfter=2,allowWidows=0,allowOrphans=0)
    body = ParagraphStyle('body',**base)
    def styled(name, **kw):
        return ParagraphStyle(name,parent=body,**kw)
    styles = {
        'body':body,
        'title':styled('title',fontName='ArialBold',fontSize=24,leading=27,spaceAfter=4,keepWithNext=True),
        'subtitle':styled('subtitle',fontName='ArialBold',fontSize=11.2,leading=14.2,spaceAfter=7,keepWithNext=True),
        'contact':styled('contact',fontSize=9.3,leading=12,spaceAfter=2,keepWithNext=True),
        'h1':styled('h1',fontName='ArialBold',fontSize=13,leading=16,spaceBefore=9,spaceAfter=4,keepWithNext=True),
        'h2':styled('h2',fontName='ArialBold',fontSize=11.3,leading=14.3,spaceBefore=6,spaceAfter=2,keepWithNext=True),
        'skill':styled('skill',fontSize=10.1,leading=12.8,spaceAfter=2),
        'stack':styled('stack',fontSize=9.3,leading=12,spaceAfter=5),
        'bullet':styled('bullet',leftIndent=10,firstLineIndent=-8,spaceAfter=1.5),
    }
    story=[]
    for kind,text,new_page in items:
        if new_page:
            story.append(PageBreak())
        story.append(Paragraph(('• ' if kind=='bullet' else '')+rich(text),styles[kind]))
    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Arial',8)
        canvas.setFillColor(colors.HexColor('#505050'))
        canvas.drawRightString(letter[0]-43.2,24,str(doc.page))
        canvas.restoreState()
    pdf=SimpleDocTemplate(str(path),pagesize=letter,leftMargin=43.2,rightMargin=43.2,topMargin=40.32,bottomMargin=40.32,title='Максим Асатуров — Fullstack-разработчик',author='Максим Асатуров')
    pdf.build(story,onFirstPage=footer,onLaterPages=footer)


if __name__ == '__main__':
    items=blocks()
    docx_path=ASSETS/f'resume-maxim-asaturov-{DATE}.docx'
    pdf_path=ASSETS/f'resume-maxim-asaturov-{DATE}.pdf'
    make_docx(items,docx_path)
    make_pdf(items,pdf_path)
    shutil.copyfile(docx_path,ASSETS/'resume-maxim-asaturov.docx')
    print(f'Built {docx_path.name}, {pdf_path.name}, and legacy Word alias from {SOURCE.name}')
