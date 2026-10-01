# Monta o index.html da Dra. Francisca reaproveitando o CSS e o JS do site da
# Dra. Jessica (mesma estrutura), com paleta azul-marinho e conteúdo próprio.
# Rodar: python3 _build/montar.py  (a partir de clientes/Dra-Francisca)
import re
from pathlib import Path

base = Path(__file__).resolve().parent.parent
jessica = (base.parent / "Dra-Jessica" / "index.html").read_text(encoding="utf-8").splitlines(keepends=True)

def bloco(inicio, fim):
    return "".join(jessica[inicio - 1:fim])

css = bloco(211, 2713)
js = bloco(3440, 3852)
svg_whatsapp = bloco(2717, 2719)

# Paleta: preto -> azul-marinho dos destaques do Instagram; dourado mantido.
trocas = {
    "--black: #080808;": "--black: #061325;",
    "--black2: #101010;": "--black2: #0A1C34;",
    "--black3: #171717;": "--black3: #102745;",
    "rgba(8, 8, 8,": "rgba(6, 19, 37,",
    "rgba(12, 12, 12,": "rgba(8, 23, 44,",
    "rgba(15, 15, 15,": "rgba(10, 28, 52,",
    "rgba(10, 10, 10,": "rgba(8, 23, 44,",
}
for antigo, novo in trocas.items():
    assert antigo in css, antigo
    css = css.replace(antigo, novo)

# Fundos dos cards de serviço da Jessica -> fotos da Dra. Francisca.
css = re.sub(r"\.service-card\.(estetica|reabilitacao|ortodontia|clinica-geral|odontopediatria)::before \{[^}]*\}\n\n", "", css)
css = css.replace('url("assets/images/treatments/atendimento-hof.jpeg")', 'url("assets/images/treatments/saude-do-sorriso.jpg")')

css = css.replace("</style>", """
/* ---------- Ajustes Dra. Francisca ---------- */
.service-card.fs-botox::before { background-image: url("assets/images/portraits/dra-francisca-atendimento.jpg"); background-position: center 30%; }
.service-card.fs-preenchimento::before { background-image: url("assets/images/portraits/dra-francisca-consultorio.jpg"); background-position: center 25%; }
.service-card.fs-contorno::before { background-image: url("assets/images/treatments/tecnologia-rejuvenescimento.jpg"); background-position: center 40%; }
.service-card.fs-tecnologia::before { background-image: url("assets/images/cases/laser-co2-antes-depois.jpg"); background-position: center 45%; }
.service-card.fs-pele::before { background-image: url("assets/images/portraits/dra-francisca-retrato.jpg"); background-position: center 30%; }

.service-icon {
  position: relative;
  z-index: 2;
  display: block;
  width: 58px;
  height: 58px;
  margin-bottom: 1rem;
  border: 1px solid var(--gold-border);
  border-radius: 50%;
  object-fit: cover;
}

.brand-monogram {
  font-style: normal;
  font-size: 1.15rem;
  letter-spacing: .06em;
  border-radius: 50%;
}

/* As fotos vieram do Instagram em baixa resolução: limitamos o tamanho
   para não esticar. Trocar pelas originais quando a Dra. enviar. */
.hero-photo { max-width: 400px; margin-left: auto; }
.about-photo img,
.precision-photo img { max-height: 620px; object-fit: cover; }
.precision-photo { max-width: 420px; margin: 0 auto; }
.precision-photo img { height: auto; aspect-ratio: auto; }
.hero-photo,
.hero-photo img { min-height: 0 !important; height: auto; }
.hero-card { top: 28px; bottom: auto !important; }
.fs-cases { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.fs-cases .case-card img { aspect-ratio: 4 / 5; object-fit: cover; }
/* Link discreto entre o site pessoal e o da clínica */
.footer-sister-link { opacity: .55; }
.footer-sister-link:hover { opacity: 1; }
.clinic-photo img { max-height: 560px; object-fit: cover; object-position: center top; }
@media (max-width: 760px) {
  .fs-cases { grid-template-columns: 1fr; }
  .hero-photo { margin: 0 auto; }
}
</style>""")

# JS: sem GTM até a Dra. ter o próprio contêiner; sem service worker.
js = js.replace('const GTM_ID = "GTM-P476T6J7";', 'const GTM_ID = ""; // preencher com o GTM da Dra. Francisca quando existir')
js = js.replace("function loadGTM() {\n  if (window.__gtmLoaded) return;", "function loadGTM() {\n  if (!GTM_ID || window.__gtmLoaded) return;")
js = js.replace('"draJessicaCookieConsent"', '"draFranciscaCookieConsent"')
js = re.sub(r'if \("serviceWorker" in navigator\) \{.*?\n\}\n', "", js, flags=re.S)
assert "GTM-P476T6J7" not in js and "serviceWorker" not in js

def montar_corpo(arquivo):
    corpo = (base / "_build" / arquivo).read_text(encoding="utf-8")
    return re.sub(r'(<a class="whatsapp-float"[^>]*>\n).*?(</a>)', lambda m: m.group(1) + svg_whatsapp + m.group(2), corpo, count=1, flags=re.S)


def montar_head(titulo, descricao, schema):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#061325">
<meta name="color-scheme" content="dark">
<meta name="format-detection" content="telephone=no">
<meta name="robots" content="index, follow">
<meta name="description" content="{descricao}">
<meta name="author" content="Dra. Francisca Silva">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Dra. Francisca Silva">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{descricao}">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/images/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<title>{titulo}</title>
<link rel="icon" type="image/svg+xml" href="assets/icons/favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400;1,600&family=Jost:wght@300;400;500;600&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema}
</script>
"""


paginas = [
    {
        # Site pessoal (CPF) da Dra. Francisca
        "corpo": "body.html",
        "saida": "index.html",
        "titulo": "Harmonização Facial em São Paulo | Dra. Francisca Silva",
        "descricao": "Harmonização facial em São Paulo com a Dra. Francisca Silva, CRO-SP 102541. Botox, preenchimento labial, lipo de papada, bichectomia, fios de PDO, Laser CO₂ e endolifting com avaliação individual.",
        "schema": """{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "name": "Dra. Francisca Silva - Harmonização Facial",
  "description": "Cirurgiã-dentista especialista em Harmonização Facial em São Paulo - SP.",
  "image": "assets/images/portraits/dra-francisca-consultorio.jpg",
  "telephone": "+55-11-99995-8264",
  "address": { "@type": "PostalAddress", "addressLocality": "São Paulo", "addressRegion": "SP", "addressCountry": "BR" },
  "sameAs": ["https://www.instagram.com/drafranciscasilva/"],
  "medicalSpecialty": "Harmonização Facial",
  "availableService": ["Botox", "Preenchimento labial", "Preenchimento de mandíbula e mento", "Lipo de papada", "Bichectomia", "Fios de PDO", "Endolifting", "Ultrassom microfocado", "Laser CO2", "Jato de plasma", "Gengivoplastia"]
}""",
    },
    {
        # Site da clínica (CNPJ). DADOS DE EXEMPLO até a Dra. aprovar e mandar os reais:
        # nome, endereço, CNPJ, horário e Instagram da clínica.
        "corpo": "body-clinica.html",
        "saida": "clinica.html",
        "titulo": "Clínica FS | Estética Facial e Odontologia em São Paulo",
        "descricao": "Clínica de estética facial e odontologia em São Paulo, com responsabilidade técnica da Dra. Francisca Silva, CRO-SP 102541. Harmonização facial, Botox, preenchimentos e tecnologias de rejuvenescimento.",
        "schema": """{
  "@context": "https://schema.org",
  "@type": "MedicalClinic",
  "name": "Clínica FS - Estética Facial e Odontologia",
  "telephone": "+55-11-99995-8264",
  "address": { "@type": "PostalAddress", "addressLocality": "São Paulo", "addressRegion": "SP", "addressCountry": "BR" },
  "employee": { "@type": "Person", "name": "Dra. Francisca Silva", "jobTitle": "Cirurgiã-dentista responsável técnica" }
}""",
    },
]

for pagina in paginas:
    head = montar_head(pagina["titulo"], pagina["descricao"], pagina["schema"])
    saida = head + css + "\n</head>\n" + montar_corpo(pagina["corpo"]) + "\n" + js + "</body>\n</html>\n"
    (base / pagina["saida"]).write_text(saida, encoding="utf-8")
    print(pagina["saida"], "gerado:", len(saida), "bytes")
