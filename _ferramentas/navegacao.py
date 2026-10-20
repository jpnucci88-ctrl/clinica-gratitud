# Liga todas as páginas do site: menu no topo, seção Equipe na inicial e cards clicáveis.
# Pode rodar de novo: remove o que inseriu antes (marcadores <!--nav:...-->) e reinsere.
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PROS = [  # slug, nome, área, foto (ou None), cor do card
    ('fernando', 'Fernando', 'Psicólogo · Psicanálise', 'fotos/fernando2.jpg', '#2A0F4F'),
    ('fernanda', 'Fernanda', 'Psicóloga e psicopedagoga · ACP', 'fotos/fernanda.jpg', '#D9C8FF'),
    ('odail', 'Odail', 'Psicólogo · ACP', 'fotos/odail.jpg', '#FFC93C'),
    ('mauricio', 'Maurício', 'Psicólogo · TCC', 'fotos/mauricio.jpg', '#2A0F4F'),
    ('sthefany', 'Sthefany', 'Psicóloga · TCC', 'fotos/sthefany.jpg', '#D9C8FF'),
    ('tatiane', 'Tatiane', 'Psicóloga · TCC', None, '#EBDFFF'),
    ('ana-elisa', 'Ana Elisa', 'Psicanalista', None, '#8E5CF0'),
    ('raissa', 'Raíssa', 'Fonoaudióloga', 'fotos/raissa.jpg', '#5A22C8'),
    ('fabiane', 'Fabiane', 'Nutricionista', 'fotos/fabiane2.jpg', '#FFC93C'),
]
WHATS = 'https://wa.me/5519996384455?text=Ol%C3%A1!%20Gostaria%20de%20agendar%20um%20hor%C3%A1rio.'

NAV_CSS = """<style>
.gnav{position:sticky;top:0;z-index:50;background:#2A0F4F;font:600 15px 'Figtree',system-ui,sans-serif}
.gnav-in{max-width:1240px;margin:0 auto;padding:0 16px;display:flex;align-items:center;gap:6px;overflow-x:auto;white-space:nowrap;scrollbar-width:none}
.gnav-in::-webkit-scrollbar{display:none}
.gnav a{color:#E9DFFF;text-decoration:none;padding:14px 10px;display:inline-block;border-bottom:3px solid transparent}
.gnav a:hover{color:#FFFFFF}
.gnav a[aria-current=page]{color:#FFC93C;border-bottom-color:#FFC93C}
.gnav .sep{width:1px;height:20px;background:#5A4A80;flex:none;margin:0 6px}
.gnav .cta{margin-left:auto;background:#FFC93C;color:#2A0F4F;border-radius:999px;padding:8px 16px;border:0}
.gnav .cta:hover{background:#FFFFFF;color:#2A0F4F}
.gnav a:focus-visible{outline:3px solid #FFC93C;outline-offset:-3px}
</style>"""

def nav(slug):
    def link(href, label, s):
        cur = ' aria-current="page"' if s == slug else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    items = [link('index.html', 'Início', 'index'), link('equipe.html', 'Equipe', 'equipe'), '<span class="sep" aria-hidden="true"></span>']
    items += [link(f'{s}.html', n, s) for s, n, *_ in PROS]
    items.append(f'<a class="cta" href="{WHATS}" target="_blank" rel="noopener">Agendar</a>')
    return ('<!--nav:menu-->' + NAV_CSS + '<nav class="gnav" aria-label="Páginas do site"><div class="gnav-in">'
            + ''.join(items) + '</div></nav><!--/nav:menu-->')

# Card da inicial com a cara da página de cada profissional (mesmas cores, fontes e símbolo).
BUTTERFLY = ('<svg aria-hidden="true" width="64" height="54" viewBox="0 0 120 100" style="position:absolute;top:-14px;right:-10px">'
             '<path d="M60 50C46 18 14 8 8 22c-6 14 12 30 40 30C20 56 12 78 26 86c14 8 28-12 34-30 6 18 20 38 34 30 14-8 6-30-22-34 28 0 46-16 40-30-6-14-38-4-52 28z" fill="#FF8A75"/>'
             '<path d="M60 30v44" stroke="#2B1F3A" stroke-width="4" stroke-linecap="round"/></svg>')
CAT = ('<svg aria-hidden="true" width="64" height="52" viewBox="0 0 120 96" style="position:absolute;top:-40px;left:50%;margin-left:-32px">'
       '<path d="M88 86c18-4 26-20 18-34" fill="none" stroke="#0B0820" stroke-width="7" stroke-linecap="round"/>'
       '<path d="M30 92c-4-26 6-48 20-56l-6-22 14 12c4-1 8-1 12 0l14-12-6 22c14 8 24 30 20 56z" fill="#0B0820"/>'
       '<circle cx="52" cy="40" r="3.4" fill="#E8C15A"/><circle cx="68" cy="40" r="3.4" fill="#E8C15A"/></svg>')
STAR = ('<svg aria-hidden="true" width="40" height="40" viewBox="0 0 24 24" fill="#FFE45C" style="position:absolute;top:-12px;right:-8px">'
        '<path d="M12 0l2.6 9.4L24 12l-9.4 2.6L12 24l-2.6-9.4L0 12l9.4-2.6z"/></svg>')
TATTOO_STAR = ('<svg aria-hidden="true" width="48" height="48" viewBox="0 0 64 64" style="position:absolute;bottom:-16px;left:-16px">'
               '<path d="M32 6l7 16 17 2-13 11 4 17-15-9-15 9 4-17L8 24l17-2z" fill="#F4EEE3" stroke="#151515" stroke-width="3.5" stroke-linejoin="round"/></svg>')
LEAF = ('<svg aria-hidden="true" width="48" height="48" viewBox="0 0 64 64" style="position:absolute;bottom:-10px;left:-14px">'
        '<path d="M10 54C10 26 30 8 56 8c0 26-18 46-46 46z" fill="#7CC08F"/><path d="M12 52L46 18" stroke="#1F5C38" stroke-width="3" stroke-linecap="round"/></svg>')
ENSO = ('<svg aria-hidden="true" viewBox="0 0 400 400" style="position:absolute;inset:-8%;width:116%;height:116%">'
        '<circle cx="200" cy="200" r="180" fill="none" stroke="#1E1E1E" stroke-width="16" stroke-linecap="round" stroke-dasharray="1050 1200" transform="rotate(-70 200 200)"/></svg>')

THEMES = {  # fundo, cor do texto, cor de destaque, fonte do nome, moldura da foto, enfeite, inicial
 'fernando': ('#0E0420', '#FFFFFF', '#FF4FB4', "'Anton',Impact,sans-serif;text-transform:uppercase", 'border:8px solid #FFFFFF;border-radius:16px;transform:rotate(-4deg);box-shadow:10px 10px 0 #FF4FB4', STAR, ''),
 'mauricio': ('#F4EEE3', '#151515', '#C8202F', "'Bebas Neue',Impact,sans-serif", 'border:4px solid #151515;border-radius:22px;box-shadow:10px 10px 0 #C8202F', TATTOO_STAR, ''),
 'odail': ('#F3EADB', '#2B211B', '#2F4A3A', "'Cormorant Garamond',Georgia,serif;font-weight:600", 'border-radius:50%;border:5px solid #F3EADB;outline:2px solid #B08D57;outline-offset:5px', '', ''),
 'fernanda': ('#EBDFFF', '#2A0F4F', '#5A22C8', "'Young Serif',Georgia,serif", 'border-radius:50% 50% 18px 18px', '', ''),
 'sthefany': ('#F3EEFF', '#2A0F4F', '#5A22C8', "'Young Serif',Georgia,serif", 'border-radius:999px 999px 0 0', '', ''),
 'tatiane': ('#FBF4EE', '#2B1F3A', '#8E4FD8', "'Fraunces',Georgia,serif", 'border-radius:999px 999px 24px 24px;background:#EBDDFB', BUTTERFLY, 'T'),
 'ana-elisa': ('#F7F3EA', '#1E1E1E', '#B3262E', "'Shippori Mincho',Georgia,serif", 'border-radius:50%;background:#EDE6D8', ENSO + '<span aria-hidden="true" style="position:absolute;right:-6px;bottom:-6px;width:44px;height:44px;border:3px solid #B3262E;border-radius:6px;color:#B3262E;display:flex;align-items:center;justify-content:center;font:700 26px \'Shippori Mincho\',serif;transform:rotate(-6deg);background:#F7F3EA">聴</span>', 'A'),
 'raissa': ('#14102E', '#F4ECD8', '#E8C15A', "'Cinzel',Georgia,serif;font-weight:700", 'border:3px solid #E8C15A;border-radius:999px 999px 14px 14px', CAT, ''),
 'fabiane': ('#FFF4EA', '#3A2418', '#D9472B', "'Fredoka',system-ui,sans-serif;font-weight:600", 'border-radius:36px;border:6px solid #FFFFFF;box-shadow:0 0 0 3px #F6B8A2', LEAF, ''),
}
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Cinzel:wght@700'
         '&family=Cormorant+Garamond:wght@600&family=Fraunces:opsz,wght@9..144,500&family=Fredoka:wght@600'
         '&family=Shippori+Mincho:wght@700&display=swap" rel="stylesheet">')

def team_section():
    cards = []
    for s, n, area, foto, _ in PROS:
        bg, fg, ac, font, frame, deco, ini = THEMES[s]
        inner = (f'<img src="{foto}" alt="" style="width:100%;height:100%;object-fit:cover;display:block">' if foto else
                 f'<span style="font-family:{font};font-size:84px;color:{ac}">{ini}</span>')
        aspect = '1' if s == 'ana-elisa' else '3/4'
        cards.append(
            f'<a class="tc" href="{s}.html" style="background:{bg};color:{fg}">'
            f'<div style="position:relative;width:72%;margin:18px auto 6px">'
            f'<div style="aspect-ratio:{aspect};overflow:hidden;display:flex;align-items:center;justify-content:center;{frame}">{inner}</div>{deco}</div>'
            f'<b style="font-weight:400;font-family:{font};font-size:clamp(30px,3vw,40px);line-height:1">{n}</b>'
            f'<span style="font-size:15px;font-weight:700;color:{ac}">{area}</span>'
            f'<span class="go" style="color:{fg}">Ver página →</span></a>')
    return ('<!--nav:equipe-->' + FONTS + '<style>'
            '.tgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:24px}'
            '.tc{display:flex;flex-direction:column;align-items:center;text-align:center;gap:10px;padding:32px 24px 28px;border-radius:32px;text-decoration:none;box-sizing:border-box;transition:transform .25s,box-shadow .25s}'
            '.tc:hover{transform:translateY(-6px);box-shadow:0 18px 40px rgba(42,15,79,.18)}'
            '.tc .go{margin-top:6px;font-size:15px;font-weight:700;text-decoration:underline;text-underline-offset:4px}'
            '.tc:focus-visible{outline:3px solid #8E5CF0;outline-offset:4px}'
            '@media (prefers-reduced-motion: reduce){.tc{transition:none}}</style>'
            '<section id="equipe" style="background:#FFFFFF"><div style="max-width:1200px;margin:0 auto;padding:104px 24px;box-sizing:border-box;display:flex;flex-direction:column;gap:48px">'
            '<div style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px 48px">'
            '<h2 class="display" style="margin:0;font-size:clamp(48px,7vw,96px);line-height:1;color:#2A0F4F">Conheça quem cuida de você.</h2>'
            '<p style="margin:0;flex:0 1 380px;font-size:19px;line-height:1.55;color:#3D2766">Cada profissional tem o seu jeito. Toque no card para conhecer a página de cada um.</p></div>'
            f'<div class="tgrid">{"".join(cards)}</div>'
            '<div><a class="pill pill-grape" href="equipe.html">Ver as abordagens da equipe</a></div>'
            '</div></section><!--/nav:equipe-->')

def strip_old(s):
    return re.sub(r'<!--nav:(\w+)-->.*?<!--/nav:\1-->', '', s, flags=re.S)

for f in sorted(SITE.glob('*.html')):
    slug = f.stem
    s = strip_old(f.read_text(encoding='utf-8'))
    s = s.replace('<body>\n', '<body>\n' + nav(slug) + '\n', 1)
    if slug == 'index':
        assert s.count('<section id="atendimento"') == 1
        s = s.replace('<section id="atendimento"', team_section() + '\n<section id="atendimento"', 1)
        s = s.replace('<a class="navlink" href="equipe.html">Equipe</a>', '<a class="navlink" href="#equipe">Equipe</a>', 1)
    if slug == 'equipe':  # card inteiro vira link
        s = re.sub(r'<div class="card">(.*?)<span style="margin-top:8px;([^"]*)"><a href="([a-z-]+\.html)" style="color:#5A22C8">Ver página</a></span>\n</div>\n</div>',
                   r'<a class="card" href="\3" style="text-decoration:none;color:inherit">\1<span style="margin-top:8px;\2;color:#5A22C8">Ver página →</span>\n</div>\n</a>',
                   s, flags=re.S)
    f.write_text(s, encoding='utf-8', newline='\n')
    print(f.name, 'menu' if '<!--nav:menu-->' in s else 'SEM MENU')
