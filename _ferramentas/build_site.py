# Converte as pranchetas .dc.html do canvas em um site estático (GitHub Pages).
import re, shutil, sys, json
from pathlib import Path

SRC = Path(sys.argv[1])          # pasta project/ do canvas
OUT = Path(sys.argv[2])          # pasta do site
SCR = Path(sys.argv[3])          # scratchpad com fotos/ e capas/

IMGS = {
 'e2b09b218b8d23ee84cafc2f8ebf8215': 'fotos/fabiane2.jpg', 'd6a6d108c9c224dc8f9742c55be33387': 'fotos/fernanda.jpg',
 '475f2657f76d65542fed609ebe3f51a6': 'fotos/fernando2.jpg', 'a84849010818a247ef2f351fee66192d': 'fotos/mauricio.jpg',
 '2d732764741e71107d6d6448993ebfc5': 'fotos/odail.jpg', 'dee4ee5c976bac72fa5795cae81e5e1e': 'fotos/raissa.jpg',
 '2d3e9a8cae59c068a9fd088e4ef9add2': 'fotos/sthefany.jpg',
 '231f028518e4922ebe9d504ad9e785c3': 'capas/ep_6qL9PA95LwE.jpg', 'b8e64f427b1c904b0048c4153f8cbab7': 'capas/ep_8rmGwotuvws.jpg',
 '459693fccc24e73ec6f3cc116fc272a2': 'capas/ep_VZ3aTpJfYBs.jpg', '90dfec55b32faf16e7f0db6108b95328': 'capas/ep_cUrNZci9TfM.jpg',
 '86ae29f2a21c200e489bc7109c4f7e89': 'capas/ep_gaOH_AL_jcY.jpg', 'f129ba50f53a4e5a50663680092dfb58': 'capas/ep_miaoVsojBrw.jpg',
 '3cedd99171deb304ed52ff70446b6e4f': 'capas/ep_o8SoRkSbmmk.jpg', 'e5049f0e136c1417f6fc70185de89e6c': 'capas/sh_0BkvV9-HHI4.jpg',
 '6568d57a9d7cd8f16d48a1016613d707': 'capas/sh_A56QoesBkow.jpg', '72b956241e6b13fb91dcd1a560a2232c': 'capas/sh_HcYl41eIR4M.jpg',
 '69acdf15faa0dfba7a4a6a4b1edd5892': 'capas/sh_PW4N77mWaHQ.jpg', 'bcbfd5ee09a926625b703097dfd864bc': 'capas/sh_X3xpdkUL410.jpg',
 '3bae03beecfa5f9543cccc358e6c8eea': 'capas/sh_f5emrfGdW50.jpg', 'bb2ccf566d0ad94b5c8f8ddef6ac42d8': 'capas/sh_rw_BJX91NHw.jpg',
}
PAGES = {'Main': 'index', 'Equipe': 'equipe', 'Fernando': 'fernando', 'Fernanda': 'fernanda', 'Odail': 'odail',
         'Raissa': 'raissa', 'AnaElisa': 'ana-elisa', 'Tatiane': 'tatiane', 'Mauricio': 'mauricio',
         'Sthefany': 'sthefany', 'Fabiane': 'fabiane'}
EQUIPE_LINKS = {8: 'fernando', 9: 'fernanda', 10: 'odail', 11: 'raissa', 12: 'ana-elisa', 13: 'tatiane',
                14: 'mauricio', 15: 'sthefany', 16: 'fabiane'}

EPS = [
 ['8rmGwotuvws', 'T2 · Ep. 5', 'O peso do silêncio masculino', 'Com Maurício Vaz e Odail Marques de Carvalho.'],
 ['o8SoRkSbmmk', 'T2 · Ep. 4', 'Quando comer vira desafio', 'Com Nathalia Rossi e Raíssa Morato Duarte.'],
 ['miaoVsojBrw', 'T2 · Ep. 3', 'Reescrevendo a própria história', 'Com Sthefany Silva e Maurício Vaz.'],
 ['cUrNZci9TfM', 'T2 · Ep. 2', 'Entre o fim e o recomeço', 'Com Fernanda Signato Marques e Odail Marques de Carvalho.'],
 ['gaOH_AL_jcY', 'T2 · Ep. 1', 'Novos olhares para a aprendizagem', 'Com Raíssa Morato Duarte e Fernanda Signato Marques.'],
 ['VZ3aTpJfYBs', 'T1 · Ep. 5', 'Saúde mental no desenvolvimento infantil', 'Com Jhonatta Ribeiro e Fernanda Signato Marques.'],
 ['6qL9PA95LwE', 'T1 · Ep. 1', 'A saúde mental da mulher', 'Com a equipe de psicologia da Clínica Gratitud.'],
]
EPS_JSON = json.dumps([{'tag': t, 'title': ti, 'who': w, 'url': 'https://www.youtube.com/watch?v=' + i,
                        'img': f'capas/ep_{i}.jpg'} for i, t, ti, w in EPS], ensure_ascii=False)

BANNER = ''  # JP: no ar, sem aviso; só fora do Google

CAROUSEL_JS = """<script>
(function(){
var eps=%s, ring='%s', i=0;
var root=document.querySelector('[data-car]'); if(!root) return;
var strip=root.querySelector('.strip');
eps.forEach(function(e,k){
  var b=document.createElement('button'); b.type='button'; b.className='thumb'; b.setAttribute('aria-label',e.title);
  b.innerHTML='<img src="'+e.img+'" alt="" loading="lazy"><span>'+e.tag+'</span>';
  b.onclick=function(){i=k;draw();}; strip.appendChild(b);
});
function draw(){
  var e=eps[i];
  root.querySelectorAll('[data-k]').forEach(function(el){
    var k=el.getAttribute('data-k');
    if(k==='url'){el.href=e.url;el.setAttribute('aria-label','Assistir: '+e.title);}
    else if(k==='img'){el.src=e.img;}
    else if(k==='pos'){el.textContent=(i+1)+' / '+eps.length;}
    else {el.textContent=e[k];}
  });
  strip.querySelectorAll('.thumb').forEach(function(b,k){b.style.outline=(k===i?'3px solid '+ring:'3px solid transparent');});
}
root.querySelector('[data-act=prev]').onclick=function(){i=(i-1+eps.length)%%eps.length;draw();};
root.querySelector('[data-act=next]').onclick=function(){i=(i+1)%%eps.length;draw();};
draw();
})();
</script>"""

def convert(name, slug):
    s = (SRC / f'{name}.dc.html').read_text(encoding='utf-8')
    title = re.search(r'<title>(.*?)</title>', s).group(1)
    helmet = re.search(r'<helmet>(.*?)</helmet>', s, re.S).group(1)
    helmet = helmet.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
    body = re.search(r'<x-dc>(.*?)</x-dc>', s, re.S).group(1)
    body = re.sub(r'<helmet>.*?</helmet>', '', body, flags=re.S)
    carousel = '{{' in body
    if carousel:
        body = body.replace('href="{{cur.url}}"', 'href="#" data-k="url" target="_blank" rel="noopener"', 1)
        body = re.sub(r'\s*target="_blank" rel="noopener" aria-label="Assistir: \{\{cur\.title\}\}"', '', body)
        body = body.replace('src="{{cur.img}}"', 'src="" data-k="img"')
        body = re.sub(r'(<span[^>]*?)>\{\{cur\.(\w+)\}\}<', r'\1 data-k="\2"><', body)
        body = re.sub(r'(<span[^>]*?)>\{\{pos\}\}<', r'\1 data-k="pos"><', body)
        body = body.replace('onClick="{{prev}}"', 'data-act="prev"').replace('onClick="{{next}}"', 'data-act="next"')
        body = re.sub(r'<sc-for.*?</sc-for>', '', body, flags=re.S)
        body = body.replace('<a class="feat"', '<a class="feat"', 1)
        # o bloco do carrossel fica dentro da section do podcast
        body = re.sub(r'(<section id="(?:podcast|podtud)"[^>]*)>', r'\1 data-car>', body, count=1)
        assert '{{' not in body, name
    for bid, path in IMGS.items():
        body = body.replace(f'/_blob/{bid}', path)
    assert '/_blob/' not in body, name
    # logo volta para a página inicial
    body = re.sub(r'<a href="#topo"( style="display:flex;align-items:center;gap:12px;text-decoration:none)',
                  r'<a href="index.html"\1', body, count=1) if slug != 'index' else body
    if slug == 'index':
        body = body.replace('<a class="navlink" href="#atendimento">Atendimento</a>',
                            '<a class="navlink" href="equipe.html">Equipe</a>\n<a class="navlink" href="#atendimento">Atendimento</a>', 1)
    if slug == 'equipe':
        for n, target in EQUIPE_LINKS.items():
            body = body.replace(f'color:#5C4A80">Página {n}</span>',
                                f'color:#5C4A80"><a href="{target}.html" style="color:#5A22C8">Ver página</a></span>', 1)
    js = CAROUSEL_JS % (EPS_JSON, '#FF4FB4' if slug == 'fernando' else '#FFC93C') if carousel else ''
    html = f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
{helmet.strip()}
</head>
<body>
{BANNER}
{body.strip()}
{js}
</body>
</html>
"""
    (OUT / f'{slug}.html').write_text(html, encoding='utf-8', newline='\n')

OUT.mkdir(parents=True, exist_ok=True)
for sub in ('fotos', 'capas'):
    (OUT / sub).mkdir(exist_ok=True)
for path in IMGS.values():
    shutil.copy(SCR / path, OUT / path)
for name, slug in PAGES.items():
    convert(name, slug)
(OUT / 'robots.txt').write_text('User-agent: *\nDisallow: /\n', encoding='utf-8')
(OUT / '.nojekyll').write_text('', encoding='utf-8')
print('ok', sorted(p.name for p in OUT.glob('*.html')))
