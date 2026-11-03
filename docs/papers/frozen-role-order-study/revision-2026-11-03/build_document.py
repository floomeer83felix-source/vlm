"""Rebuild the paper from published aggregate tables only; no model/data replay."""
from pathlib import Path
import argparse,csv,json,os,re,subprocess

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
SEEDS=(137,263,419,557,733,911)

def rows(path):
    with (REPO/path).open() as f:return list(csv.DictReader(f))

def save_plot(fig,name):
    for ext in ['png','svg']:
        p=HERE/'figures'/(name+'.'+ext)
        fig.savefig(p,dpi=300,bbox_inches='tight')
        if ext=='svg':p.write_text('\n'.join(line.rstrip() for line in p.read_text().splitlines())+'\n')

def prepare():
    r63=rows('docs/codex-artifacts/VLM-ROLE-CONTRAST-REPLICATION-063/condition-summary.csv')
    r68=rows('docs/codex-artifacts/VLM-FROZEN-TRANSFER-READMISSION-068/condition-summary.csv')
    by63={(r['method'],int(r['seed']),r['split']):r for r in r63 if r['seed'].isdigit()}
    by68={(r['method'],int(r['seed'])):r for r in r68}
    series=[]
    for split,n in [('train_pool68',68),('validation11',11),('development54',54),('source_holdout50',50)]:
        rec={'split':split,'n_per_seed':n}
        for m in ['C_NATIVE','D_NATIVE']:
            a=[by63[m,s,split] for s in SEEDS]
            assert all(int(x['n_instances'])==n and int(x['unknown_cells'])==0 for x in a)
            rec[m]={'four_way_correct':[int(x['four_way_correct']) for x in a],
                    'question_invariant':[int(x['question_invariant']) for x in a],
                    'mean_four_way_pct':sum(int(x['four_way_correct']) for x in a)*100/(6*n)}
        series.append(rec)
    rec={'split':'VIDHALLUC_new_items','n_per_seed':50}
    for m in ['C_NATIVE','D_NATIVE']:
        a=[by68[m,s] for s in SEEDS]
        assert all(int(x['planned_items'])==50 and x['status']=='CLOSED' for x in a)
        rec[m]={'four_way_correct':[int(x['four_way_correct']) for x in a],
                'question_invariant':[int(x['question_invariant']) for x in a],
                'mean_four_way_pct':sum(int(x['four_way_correct']) for x in a)/3}
    series.append(rec)
    assert series[3]['C_NATIVE']['four_way_correct']==[3,6,1,1,2,2]
    assert series[3]['D_NATIVE']['four_way_correct']==[10,10,10,6,8,9]
    assert series[4]['C_NATIVE']['four_way_correct']==[1,0,0,0,1,2]
    assert series[4]['D_NATIVE']['four_way_correct']==[8,7,6,2,7,7]
    intervals=[{'dataset':'50Salads','axis':'family','point':38/3,'lower':17/3,'upper':61/3},
               {'dataset':'50Salads','axis':'seed','point':38/3,'lower':31/3,'upper':46/3},
               {'dataset':'VIDHALLUC','axis':'paired_unit','point':11,'lower':5,'upper':53/3},
               {'dataset':'VIDHALLUC','axis':'seed','point':11,'lower':8,'upper':40/3}]
    (HERE/'tables.json').write_text(json.dumps({'seeds':SEEDS,'series':series,'existing_intervals':intervals,
        'new_model_evaluation':False,'new_training':False,'new_resampling':False,
        'scope':'Repeated seeds are not independent source examples.'},ensure_ascii=False,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
    fig,axs=plt.subplots(1,2,figsize=(6.4,2.65),sharey=True,layout='constrained')
    for ax,rec,title in zip(axs,series[3:],['50Salads','VIDHALLUC']):
        c,d=rec['C_NATIVE']['four_way_correct'],rec['D_NATIVE']['four_way_correct']
        for i,(x,y) in enumerate(zip(c,d)):
            offset=(i-2.5)*.018
            ax.plot([offset,1+offset],[x,y],color='#9b9b9b',linewidth=.8,zorder=1)
            ax.scatter(offset,x,color='#345e87',s=26,marker='o',zorder=2)
            ax.scatter(1+offset,y,color='#ad6330',s=30,marker='^',zorder=2)
        ax.set_xticks([0,1],['C','D']);ax.set_xlim(-.32,1.32);ax.set_ylim(-.4,11.5)
        ax.set_title(title,fontsize=10);ax.grid(axis='y',color='#e5e5e5',lw=.5);ax.set_axisbelow(True)
    axs[0].set_ylabel('Four-way correct / 50')
    (HERE/'figures').mkdir(exist_ok=True)
    save_plot(fig,'paired-seeds')
    plt.close(fig)
    fig,ax=plt.subplots(figsize=(6.4,2.55),layout='constrained')
    for i,x in enumerate(intervals):
        y=3-i;color='#345e87' if x['axis']!='seed' else '#9fb4c8'
        ax.errorbar(x['point'],y,xerr=[[x['point']-x['lower']],[x['upper']-x['point']]],fmt='o',color=color,capsize=3,lw=1.7)
    ax.set_yticks([3,2,1,0],['50Salads  family axis','50Salads  seed axis','VIDHALLUC  pair axis','VIDHALLUC  seed axis'])
    ax.axvline(0,color='#777777',lw=.8);ax.set_xlim(-1,23);ax.set_ylim(-.65,3.65)
    ax.set_xlabel('D minus C in four-way accuracy (percentage points)')
    ax.grid(axis='x',color='#e5e5e5',lw=.5);ax.set_axisbelow(True)
    save_plot(fig,'conditional-intervals')
    plt.close(fig)
    return series

def make_docx():
    from docx import Document
    from docx.shared import Inches,Pt,RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_ALIGN_VERTICAL
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    intermediate=HERE/'manuscript-pandoc.docx'
    subprocess.run(['pandoc',str(HERE/'manuscript.md'),'--from','markdown+tex_math_dollars','--to','docx','--standalone','--resource-path',str(HERE),'-o',str(intermediate)],check=True)
    d=Document(intermediate);sec=d.sections[0]
    sec.page_width=Inches(8.5);sec.page_height=Inches(11)
    sec.top_margin=sec.bottom_margin=Inches(.75);sec.left_margin=sec.right_margin=Inches(.8)
    sec.footer_distance=Inches(.3)
    for style in d.styles:
        if style.type!=1:continue
        style.font.name='Liberation Serif';style.font.size=Pt(11.5);style.font.color.rgb=RGBColor(0,0,0)
        rpr=style.element.get_or_add_rPr();f=rpr.find(qn('w:rFonts'))
        if f is None:f=OxmlElement('w:rFonts');rpr.insert(0,f)
        f.set(qn('w:eastAsia'),'Noto Serif CJK SC')
        for k in ['asciiTheme','hAnsiTheme','eastAsiaTheme','cstheme']:f.attrib.pop(qn('w:'+k),None)
    styles={s.name:s for s in d.styles}
    normal=styles['Normal'];normal.paragraph_format.line_spacing=1.16;normal.paragraph_format.space_after=Pt(5)
    for name in ['Body Text','First Paragraph']:
        if name in styles:
            styles[name].paragraph_format.line_spacing=1.16
            styles[name].paragraph_format.space_after=Pt(5)
    styles['Title'].font.size=Pt(17);styles['Title'].font.bold=True
    styles['Title'].paragraph_format.space_after=Pt(12)
    for name,size in [('Heading 1',13),('Heading 2',11.7)]:
        styles[name].font.size=Pt(size);styles[name].font.bold=True
        styles[name].paragraph_format.space_before=Pt(10);styles[name].paragraph_format.space_after=Pt(5)
        styles[name].paragraph_format.keep_with_next=True
    if 'Caption' in styles:
        styles['Caption'].font.size=Pt(10);styles['Caption'].font.italic=False
    for p in d.paragraphs:
        p.paragraph_format.widow_control=True
        if p.style.name=='Title':p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        elif p.style.name.startswith('Heading'):p.alignment=WD_ALIGN_PARAGRAPH.LEFT
        elif re.match(r'^表\d+\s',p.text):
            p.paragraph_format.keep_with_next=True;p.paragraph_format.first_line_indent=Inches(0)
            for r in p.runs:r.font.size=Pt(10)
        elif p.style.name in ['Image Caption','Caption']:
            p.paragraph_format.first_line_indent=Inches(0)
            p.paragraph_format.space_before=Pt(3);p.paragraph_format.space_after=Pt(8)
            for r in p.runs:r.font.size=Pt(9.5)
        elif p.text.startswith('['):
            p.paragraph_format.first_line_indent=Inches(-.2);p.paragraph_format.left_indent=Inches(.2)
            p.paragraph_format.space_after=Pt(5)
            for r in p.runs:r.font.size=Pt(9.5)
        elif p.text and not p.text.startswith(('摘要','关键词','Abstract','Keywords','Role Contrast')):
            p.paragraph_format.first_line_indent=Pt(23)
        if p._p.xpath('.//w:drawing'):
            p.paragraph_format.keep_with_next=True;p.alignment=WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before=Pt(8)
        # Pandoc emits real Word math; retain it intact.
    for ti,table in enumerate(d.tables):
        table.autofit=False
        widths=[2.15,1.0,1.05,1.05,1.65] if ti==0 else [.7,1.55,1.55,1.55,1.55]
        widths=[w*6.9/sum(widths) for w in widths]
        for col,w in zip(table.columns,widths):col.width=Inches(w)
        for ri,row in enumerate(table.rows):
            trpr=row._tr.get_or_add_trPr();ns=OxmlElement('w:cantSplit');trpr.append(ns)
            if ri==0:
                hdr=OxmlElement('w:tblHeader');trpr.append(hdr)
            for ci,cell in enumerate(row.cells):
                cell.width=Inches(widths[ci]);cell.vertical_alignment=WD_ALIGN_VERTICAL.CENTER
                tcpr=cell._tc.get_or_add_tcPr();b=OxmlElement('w:tcBorders')
                for edge in ['top','left','bottom','right']:
                    e=OxmlElement('w:'+edge);e.set(qn('w:val'),'single');e.set(qn('w:sz'),'4');e.set(qn('w:color'),'D9D9D9');b.append(e)
                tcpr.append(b);margin=OxmlElement('w:tcMar')
                for edge in ['top','left','bottom','right']:
                    e=OxmlElement('w:'+edge);e.set(qn('w:w'),'80');e.set(qn('w:type'),'dxa');margin.append(e)
                tcpr.append(margin)
                if ri==0:
                    shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'E8EDF2');tcpr.append(shade)
                for p in cell.paragraphs:
                    p.paragraph_format.first_line_indent=Inches(0);p.paragraph_format.left_indent=Inches(0)
                    p.paragraph_format.space_after=Pt(0);p.paragraph_format.line_spacing=1.05
                    p.alignment=WD_ALIGN_PARAGRAPH.LEFT if ci==0 and ti==0 else WD_ALIGN_PARAGRAPH.CENTER
                    for r in p.runs:r.font.size=Pt(10);r.font.bold=(ri==0)
    foot=sec.footer.paragraphs[0];foot.alignment=WD_ALIGN_PARAGRAPH.CENTER
    fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');foot._p.append(fld)
    d.core_properties.author='';d.core_properties.last_modified_by='';d.core_properties.title='冻结特征时间问答中角色差分的效果及边界'
    target=HERE/'manuscript.docx';d.save(target);intermediate.unlink()
    print(json.dumps({'docx':str(target),'native_math_blocks':len(d.element.xpath('.//m:oMath')),'tables':len(d.tables),'paragraphs':len(d.paragraphs)},ensure_ascii=False))

if __name__=='__main__':
    prepare();make_docx()
