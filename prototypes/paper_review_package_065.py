"""Public document package utilities; never imports research/model modules.

Capabilities are read-only. Other modes work on public manuscript aggregates only.
No network, training, feature reads or bootstrap sampling.
"""
import argparse,csv,hashlib,importlib.util,json,os,re,shutil,struct,subprocess,sys,time,zipfile
from pathlib import Path
import xml.etree.ElementTree as ET
from html import escape

def put(p,x):
 Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def capabilities(root):
 start=time.monotonic();runtime=Path(sys.executable).parent.parent;native=runtime/'native'
 modules={name:importlib.util.find_spec(name) is not None for name in ('docx','reportlab','fitz','pypdf','PIL','matplotlib')}
 tools={name:shutil.which(name) for name in ('pandoc','soffice','pdftoppm','pdfinfo')}
 candidates=[native/'libreoffice/program/soffice.exe',native/'libreoffice/soffice.exe',runtime/'bin/override/soffice.exe',runtime/'bin/fallback/soffice.exe']
 fonts=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts';fontfiles={n:str(fonts/n) for n in ('simhei.ttf','simsun.ttc','msyh.ttc','arial.ttf') if (fonts/n).is_file()}
 result=dict(status='READ_ONLY_CAPABILITY_CHECK',modules=modules,tools=tools,bundled_libreoffice_candidates={str(p):p.is_file() for p in candidates},bundled_native_entries=[p.name for p in native.iterdir()] if native.is_dir() else [],fonts=fontfiles,python=sys.executable,outer_s=time.monotonic()-start,office_COM_used=False,installs=0)
 put(Path(root)/'capabilities.json',result);print(json.dumps(result,ensure_ascii=False),flush=True)

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))

def markup(text):
 text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',text).replace('`','')
 text=escape(text)
 text=text.replace('10⁻⁸','10<super>−8</super>').replace('²','<super>2</super>')
 text=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',text)
 # Typed sub/superscripts, not raw LaTeX in the PDF.
 text=text.replace('z_j(q)_d','z<sub>j</sub>(q)<sub>d</sub>')
 text=re.sub(r'([zTsμ])_\{([^}]+)\}',r'\1<sub>\2</sub>',text)
 text=re.sub(r'Σ_\{([^}]+)\}',r'Σ<sub>\1</sub>',text)
 text=text.replace('Σ_d','Σ<sub>d</sub>')
 text=re.sub(r'(?<![A-Za-z])([zTsμ])_([CDNj])(?![A-Za-z0-9_])',r'\1<sub>\2</sub>',text)
 text=re.sub(r'\bc_(ivq)(?![A-Za-z0-9_])',r'c<sub>\1</sub>',text)
 text=re.sub(r'\bp_(i\d\d)(?![A-Za-z0-9_])',r'p<sub>\1</sub>',text)
 text=text.replace('−','<font name="PaperLatin">−</font>')
 # Proportional Latin type, while keeping identifiers/URLs literal and Chinese in Song.
 pieces=re.split(r'(<[^>]+>)',text)
 for i in range(0,len(pieces),2):
  pieces[i]=re.sub(r'&[A-Za-z0-9#]+;|[\x20-\x7e]+',lambda m:m[0] if m[0].startswith('&') else '<font name="PaperLatin">'+m[0]+'</font>',pieces[i])
 text=''.join(pieces)
 return text

def build_pdf(repo,root,font):
 from reportlab.pdfbase import pdfmetrics
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.lib import colors
 from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY
 from reportlab.lib.pagesizes import A4
 from reportlab.lib.styles import ParagraphStyle
 from reportlab.lib.units import mm
 from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,KeepTogether
 import reportlab.platypus.paragraph as paragraph_module
 import reportlab.lib.textsplit as textsplit_module
 paragraph_module.ALL_CANNOT_START+='，；：！？）》】”’'
 textsplit_module.ALL_CANNOT_START+='，；：！？）》】”’'
 repo=Path(repo);root=Path(root);paper=repo/'docs/papers/frozen-role-order-study/review065';text=(paper/'manuscript.md').read_text(encoding='utf-8')
 pdfmetrics.registerFont(TTFont('PaperCJK',font,subfontIndex=0));pdfmetrics.registerFont(TTFont('PaperLatin',str(Path(font).parent/'arial.ttf')))
 # One embedded Chinese font covers all body and mathematical glyphs; record misses instead of silently substituting.
 face=pdfmetrics.getFont('PaperCJK').face;latin=pdfmetrics.getFont('PaperLatin').face;plain=re.sub(r'<[^>]+>','',markup(re.sub(r'!\[[^\]]*\]\([^)]+\)','',text)));miss=sorted({ord(c) for c in plain if ord(c)>127 and ord(c) not in (latin.charToGlyph if c=='−' else face.charToGlyph)})
 if miss:raise ValueError('FONT_MISSING_GLYPHS:'+','.join(hex(x) for x in miss))
 normal=ParagraphStyle('Body',fontName='PaperCJK',fontSize=11,leading=17,spaceAfter=7,wordWrap='CJK',textColor=colors.black,splitLongWords=True)
 title=ParagraphStyle('Title',parent=normal,fontSize=18,leading=25,spaceAfter=12,alignment=TA_CENTER,keepWithNext=True)
 h1=ParagraphStyle('H1',parent=normal,fontSize=14,leading=21,spaceBefore=12,spaceAfter=7,keepWithNext=True)
 h2=ParagraphStyle('H2',parent=normal,fontSize=12,leading=18,spaceBefore=9,spaceAfter=6,keepWithNext=True)
 caption=ParagraphStyle('Caption',parent=normal,fontSize=9.5,leading=14,spaceAfter=9)
 tabletext=ParagraphStyle('Table',parent=normal,fontSize=9,leading=13,spaceAfter=0,alignment=TA_CENTER)
 refs=ParagraphStyle('Reference',parent=normal,fontSize=9.5,leading=14,spaceAfter=7)
 formula=ParagraphStyle('Formula',parent=normal,fontSize=10.5,leading=18,leftIndent=7,spaceBefore=3,spaceAfter=9)
 width=A4[0]-40*mm;story=[];lines=text.splitlines();i=0;references=False;figures=0;tables=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('#'):
   level=len(line)-len(line.lstrip('#'));value=line[level:].strip();references=references or value=='参考文献';story.append(Paragraph(markup(value),title if level==1 else h1 if level==2 else h2));i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    vals=[s.strip() for s in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',s) for s in vals):rows.append(vals)
    i+=1
   cells=[[Paragraph(markup(s),tabletext) for s in row] for row in rows];n=len(rows[0]);colwidths=[width/n]*n
   if n==6:colwidths=[width*.22]+[width*.156]*5
   if n==8:colwidths=[width*.08]+[width*.105]*6+[width*.29]
   table=Table(cells,colWidths=colwidths,repeatRows=1,hAlign='CENTER');table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEABOVE',(0,0),(-1,0),.7,colors.black),('LINEBELOW',(0,0),(-1,0),.4,colors.black),('LINEBELOW',(0,-1),(-1,-1),.7,colors.black),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#F1F1F1'))]));story.extend([table,Spacer(1,8)]);tables+=1;continue
  if line.startswith('!['):
   match=re.search(r'\]\(([^)]+)\)',line);path=(paper/match[1]).with_suffix('.png').resolve();body=path.read_bytes();w,h=struct.unpack('>II',body[16:24]);im=Image(str(path),width=width,height=width*h/w)
   i+=1
   while i<len(lines) and not lines[i].strip():i+=1
   cap=lines[i].strip() if i<len(lines) and re.match('图[123]　',lines[i].strip()) else ''
   if cap:i+=1
   story.append(KeepTogether([im,Spacer(1,5),Paragraph(markup(cap),caption)]));figures+=1;continue
  para=[line];i+=1
  while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','![')):para.append(lines[i].strip());i+=1
  value=' '.join(para);style=refs if references else formula if value.startswith(('z_C','μ_j','T_j')) else caption if value.startswith(('表1　','表2　')) else normal
  p=Paragraph(markup(value),style)
  if value.startswith(('表1　','表2　')):p.keepWithNext=True
  story.append(p)
 def footer(canvas,doc):
  canvas.setAuthor('');canvas.setCreator('Public manuscript document builder');canvas.setTitle('冻结特征时间问答的角色差分与顺序效应');canvas.setSubject('Empirical manuscript revision');canvas.setFont('PaperLatin',9);canvas.drawCentredString(A4[0]/2,12*mm,str(doc.page))
 target=paper/'manuscript.pdf';doc=SimpleDocTemplate(str(target),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=19*mm,bottomMargin=19*mm,title='冻结特征时间问答的角色差分与顺序效应',author='')
 doc.build(story,onFirstPage=footer,onLaterPages=footer)
 put(root/'build.json',dict(status='PDF_GENERATED_NOT_YET_VISUALLY_VERIFIED',figures=figures,tables=tables,font_missing_glyphs=miss,PDF_bytes=target.stat().st_size,formula_format='selectable PDF typography with subscript tags;not Word OMML',docx='EXPORT_NOT_GENERATED_NO_RELIABLE_RENDERER'));print('PDF_BUILT',target.stat().st_size,'FIGURES',figures,'TABLES',tables,flush=True)

def audit_content(repo,root):
 repo=Path(repo);root=Path(root);base=repo/'docs/papers/frozen-role-order-study';p=base/'review065';t=(p/'manuscript.md').read_text(encoding='utf-8');s=(p/'supplement.md').read_text(encoding='utf-8');data=load(base/'tables.json');rep=data['replication063'];checks=0
 def check(ok,msg):
  nonlocal checks
  checks+=1
  if not ok:raise AssertionError(msg)
 body='## 1 引言'+t.split('## 1 引言',1)[1].split('## 参考文献',1)[0];body='\n'.join(x for x in body.splitlines() if not x.startswith(('|','![')));han=len(re.findall('[\u4e00-\u9fff]',body));check(5000<=han<=6500,'body length')
 check(not re.search(r'【E\d|\b0(?:60|61|62|63|64|65)\b|READY|本轮合同|验收',t),'main no audit identifiers')
 for abstract in (t.split('## 中文摘要')[1].split('## English abstract')[0],t.split('## English abstract')[1].split('## 1 引言')[0]):
  for item in ('5.00%','17.67%','12.67','[5.67,20.33]','[10.33,15.33]','52.67%','19.00%','20%'):check(item in abstract,'bilingual number '+item)
 for item in ('seed733由13降至11','seed557为6/50','[−14,22]','19例子层','低于B0','不是容量匹配','不添加稳定化epsilon','FAILED','NOT_RUN','NA','10.13/50','同形式标准化'):
  check(item in t,'limitation/method '+item)
 for seed in (19,73,137,263,419,557,733,911):
  line=next(x for x in t.splitlines() if x.startswith('| '+str(seed)+'，'));cells=[x.strip() for x in line.split('|')[1:-1]];sr=next(x for x in rep['seed_summary'] if x['seed']==seed and x['split']=='source_holdout50');dr=next(x for x in rep['seed_summary'] if x['seed']==seed and x['split']=='development54');check([int(x) for x in cells[1:]]==[sr['C_correct'],sr['D_correct'],sr['net'],dr['C_correct'],dr['D_correct']],'table1')
 for seed in (19,73):
  line=next(x for x in t.splitlines() if x.startswith('| '+str(seed)+' |'));cells=[x.strip() for x in line.split('|')[1:-1]];expect=[next(x['four_way_correct'] for x in rep['conditions'] if (x['method'],x['seed'],x['split'])==(m,seed,'source_holdout50')) for m in ('C_NATIVE','D_NATIVE','C_HASH','D_HASH')];check([int(x) for x in cells[1:5]]==expect,'table2');z=next(x for x in rep['interactions'] if x['seed']==seed);check(int(cells[5])==expect[1]-expect[3] and int(cells[6])==z['net_instances'],'table2 deltas')
 rows=[x for x in s.splitlines() if re.match(r'\| I\d\d/',x)];check(len(rows)==34,'all interval indices')
 for i,(line,row) in enumerate(zip(rows,rep['intervals'])):
  cells=[x.strip() for x in line.split('|')[1:-1]];check(cells[0]==f'I{i+1:02}/{i}','interval identity');check([float(x) for x in cells[-3:]]==[row['estimate_pp'],row['ci_low_pp'],row['ci_high_pp']],'original interval precision')
 with open(p/'evidence-map.csv',encoding='utf-8',newline='') as f:ev=list(csv.DictReader(f))
 check(len(ev)==25 and [x['claim_id'] for x in ev]==[f'E{i:02}' for i in range(1,26)],'25 claims')
 for row in ev:check(bool(row['paragraph']) and (repo/row['relative_path']).is_file() and len(row['commit'])==40 and bool(row['exact_numeric_anchor']),'claim source and location')
 figures=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',t);check(len(figures)==3,'three old figures')
 for path in figures:check(path.startswith('../figures/') and (p/path).is_file() and (p/path).with_suffix('.png').is_file(),'relative original figures')
 for i in range(1,9):check(bool(re.search(r'^\['+str(i)+r'\].+https://',t,re.M)),'standalone reference '+str(i))
 check(len(re.findall(r'^## \d+ ',(p/'reviewer-questions.md').read_text(encoding='utf-8'),re.M))>=6,'reviewer questions')
 def git(*args):return subprocess.check_output(['git',*args],cwd=repo)
 sha='df50bf1c8389d20418bc56b5641f13f8f8392bfa';names=git('diff-tree','--no-commit-id','--name-only','-r',sha).decode().splitlines();sizes={n:int(git('cat-file','-s',sha+':'+n)) for n in names};old_result=int(git('cat-file','-s',sha+'^:docs/codex-results.md'));total=sum(sizes.values());added=sum(v for n,v in sizes.items() if n!='docs/codex-results.md');delta=sizes['docs/codex-results.md']-old_result
 check(len(names)==16 and (total,added,sizes['docs/codex-results.md'],delta,added+delta)==(1105663,809017,296646,2704,811721),'064 immutable blob size clarification')
 put(root/'content-audit.json',dict(status='PASS',checks=checks,body_han_characters=han,count_definition='Sections1-6 including headings/captions;Han U+4E00-U+9FFF;excludes abstracts/tables/image lines/references',intervals_quoted_exactly=34,bootstrap_recomputed=False,old064_sizes=dict(total16_blob_bytes=total,new15_blob_bytes=added,results_full_blob_bytes=sizes['docs/codex-results.md'],results_increment_bytes=delta,new_payload_including_increment_bytes=added+delta,old_reported_bytes=1121474,difference_reason='UNKNOWN;public evidence insufficient'),scientific_values_changed=False));print('CONTENT_AUDIT_PASS',checks,'HAN',han,flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['capabilities','build_pdf','audit_content']);p.add_argument('--root',required=True);p.add_argument('--repo');p.add_argument('--font');a=p.parse_args()
 if a.mode=='capabilities':capabilities(a.root)
 elif a.mode=='build_pdf':build_pdf(a.repo,a.root,a.font)
 else:audit_content(a.repo,a.root)
