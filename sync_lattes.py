#!/usr/bin/env python3
"""Import public Lattes XML into publications.json. Requires only Python stdlib."""
import json,sys,html,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parent
TYPES={
 'ARTIGOS-PUBLICADOS':('article','ARTIGO-PUBLICADO'),
 'LIVROS-PUBLICADOS-OU-ORGANIZADOS':('book','LIVRO-PUBLICADO-OU-ORGANIZADO'),
 'CAPITULOS-DE-LIVROS-PUBLICADOS':('chapter','CAPITULO-DE-LIVRO-PUBLICADO'),
 'TRABALHOS-EM-EVENTOS':('conference','TRABALHO-EM-EVENTOS'),
 'RESUMOS-EXPANDIDOS':('abstract','RESUMO-EXPANDIDO'),
}
def get(node,tag):
 x=node.find(tag);return x.attrib if x is not None else {}
def parse(path):
 root=ET.parse(path).getroot();out=[];seen=set()
 for parent,tag,typ,detail in [
 ('ARTIGOS-PUBLICADOS','ARTIGO-PUBLICADO','article','DETALHAMENTO-DO-ARTIGO'),
 ('LIVROS-PUBLICADOS-OU-ORGANIZADOS','LIVRO-PUBLICADO-OU-ORGANIZADO','book','DETALHAMENTO-DO-LIVRO'),
 ('CAPITULOS-DE-LIVROS-PUBLICADOS','CAPITULO-DE-LIVRO-PUBLICADO','chapter','DETALHAMENTO-DO-CAPITULO'),
 ('TRABALHOS-EM-EVENTOS','TRABALHO-EM-EVENTOS','conference','DETALHAMENTO-DO-TRABALHO')]:
  for node in root.iter(tag):
   b=get(node,'DADOS-BASICOS-DO-ARTIGO' if typ=='article' else 'DADOS-BASICOS-DO-LIVRO' if typ=='book' else 'DADOS-BASICOS-DO-CAPITULO' if typ=='chapter' else 'DADOS-BASICOS-DO-TRABALHO')
   d=get(node,detail)
   title=b.get('TITULO-DO-ARTIGO') or b.get('TITULO-DO-LIVRO') or b.get('TITULO-DO-CAPITULO-DO-LIVRO') or b.get('TITULO-DO-TRABALHO') or ''
   if not title:continue
   year=b.get('ANO-DO-ARTIGO') or b.get('ANO') or b.get('ANO-DO-TRABALHO') or ''
   nature=b.get('NATUREZA','')
   category=('abstract' if typ=='conference' and 'RESUMO' in nature.upper() else typ)
   venue=d.get('TITULO-DO-PERIODICO-OU-REVISTA') or d.get('TITULO-DO-LIVRO') or d.get('NOME-DO-EVENTO') or ''
   doi=b.get('DOI','').strip();url=('https://doi.org/'+doi if doi else b.get('HOME-PAGE-DO-TRABALHO','').strip())
   authors=[a.get('NOME-COMPLETO-DO-AUTOR','') for a in node.findall('AUTORES')]
   key=(title.casefold(),str(year));
   if key in seen:continue
   seen.add(key);out.append(dict(type=category,year=year,title=title,venue=venue,authors=authors,doi=doi,url=url))
 return sorted(out,key=lambda x:(int(x['year']) if str(x['year']).isdigit() else 0,x['title']),reverse=True)
if __name__=='__main__':
 path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'lattes.xml'
 if not path.exists():sys.exit(f'Arquivo não encontrado: {path}. Exporte o currículo em XML no Lattes.')
 root=ET.parse(path).getroot()
 if root.tag!='CURRICULO-VITAE' or root.get('NUMERO-IDENTIFICADOR')!='0807911743415172':
  sys.exit('O XML não corresponde ao currículo Lattes esperado (ID 0807911743415172).')
 data={'source':'Lattes XML (exportação oficial)','lattes_id':'0807911743415172','publications':parse(path)}
 projects=[];seen=set()
 for node in root.iter('PROJETO-DE-PESQUISA'):
  a=node.attrib;title=(a.get('NOME-DO-PROJETO') or a.get('TITULO-DO-PROJETO') or '').strip()
  if not title or title.casefold() in seen:continue
  seen.add(title.casefold())
  projects.append({'title':title,'description':html.unescape(a.get('DESCRICAO-DO-PROJETO','')),'start_year':a.get('ANO-INICIO',''),'end_year':a.get('ANO-FIM',''),'status':a.get('SITUACAO',''),'nature':a.get('NATUREZA','')})
 projects.sort(key=lambda x:(int(x['start_year']) if x['start_year'].isdigit() else 0,x['title']),reverse=True)
 (ROOT/'projects.json').write_text(json.dumps({'source':data['source'],'lattes_id':data['lattes_id'],'projects':projects},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (ROOT/'publications.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f"Importadas {len(data['publications'])} publicações e {len(projects)} projetos")
