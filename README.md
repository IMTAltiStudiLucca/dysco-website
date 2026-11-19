# Manuale Utente e Guida alla Manutenzione - DYSCO Website

Questo repository contiene il sito web della Research Unit **DYSCO** (*Dynamical Systems, Control, and Optimization*) della Scuola IMT Alti Studi Lucca.

Il sito è sviluppato come **Single-Page Application statica e responsive**, basata su HTML5, Tailwind CSS e JavaScript vanilla (senza dipendenze pesanti o framework complessi).

## Licenza e Crediti

* **Codice sorgente (HTML/CSS):** rilasciato sotto licenza [MIT](LICENSE).
* **Testi:** rilasciati sotto licenza [CC BY-NC-ND 4.0](https://creativecommons.org).
* **Asset grafici e marchi:**
  * L'immagine di header proviene da [Pexels](https://pexels.com) ed è soggetta alla relativa [licenza Pexels](https://pexels.comlicense/).
  * Il logo della Scuola e la favicon (IRIS) sono di proprietà dei rispettivi titolari e sono esclusi da qualsiasi licenza di riutilizzo (*Tutti i diritti riservati*).

---

## Indice

- [Manuale Utente e Guida alla Manutenzione - DYSCO Website](#manuale-utente-e-guida-alla-manutenzione---dysco-website)
  - [Licenza e Crediti](#licenza-e-crediti)
  - [Indice](#indice)
  - [1. Struttura dei File](#1-struttura-dei-file)
  - [2. Identità Visiva e Linee Guida di Stile](#2-identità-visiva-e-linee-guida-di-stile)
  - [3. Guida alla Modifica delle Sezioni](#3-guida-alla-modifica-delle-sezioni)
    - [3.1 Head, SEO, Favicon e Analytics](#31-head-seo-favicon-e-analytics)
      - [Come aggiungere Google Analytics 4 (GA4):](#come-aggiungere-google-analytics-4-ga4)
    - [3.2 Header e Menu di Navigazione](#32-header-e-menu-di-navigazione)
      - [Come aggiungere o modificare una voce di menu:](#come-aggiungere-o-modificare-una-voce-di-menu)
    - [3.3 Presentation \& Hero](#33-presentation--hero)
      - [Come regolare l'opacità dello sfondo fotografico:](#come-regolare-lopacità-dello-sfondo-fotografico)
    - [3.4 Sezione People](#34-sezione-people)
      - [Template per aggiungere un nuovo membro:](#template-per-aggiungere-un-nuovo-membro)
    - [3.5 Research Topics](#35-research-topics)
    - [3.6 Teaching (PhD Courses)](#36-teaching-phd-courses)
    - [3.7 Software Tools](#37-software-tools)
      - [Template per aggiungere un nuovo Software Tool:](#template-per-aggiungere-un-nuovo-software-tool)
    - [3.8 Applications](#38-applications)
    - [3.9 Network (Collaborations, Funding, Events)](#39-network-collaborations-funding-events)
    - [3.10 Spinoff (ODYS S.r.l.)](#310-spinoff-odys-srl)
    - [3.11 Footer e Pulsante "Torna su"](#311-footer-e-pulsante-torna-su)
  - [4. Test Locale e Deploy in Produzione](#4-test-locale-e-deploy-in-produzione)
    - [Come visualizzare e testare il sito in locale](#come-visualizzare-e-testare-il-sito-in-locale)
    - [Validazione e Manutenzione del codice](#validazione-e-manutenzione-del-codice)

---

## 1. Struttura dei File

```text
/var/www/dysco/
├── dysco.html                      # File HTML principale del sito
├── README.md                       # Questo manuale utente
└── assets/
    ├── logo.svg                    # Logo vettoriale ufficiale IMT Lucca / DYSCO
    ├── iris-ico.ico                # Icona ufficiale IRIS per i profili dei ricercatori
    ├── pexels-header-27141316.jpg  # Immagine di sfondo ad alta risoluzione per l'hero header
    └── originale.html              # Copia storica del vecchio sito (per archivio/consultazione)
```

---

## 2. Identità Visiva e Linee Guida di Stile

Il sito adotta uno stile **editoriale e brutalist moderno**, caratterizzato da:

- **Palette colori**:
  - `imt-blue`: `#003366` (Blu istituzionale IMT Lucca).
  - `imt-white`: `#ffffff` (Bianco puro).
- **Tipografia**: Font `Inter`, con interlinea compatta e tracking stretto (`editorial-heading`, `tracking-tighter`).
- **Griglie e Bordi**: Linee nette di separazione da 2px (`border-2 border-imt-blue`, `divide-imt-blue`).
- **Comportamento dei Link**:
  - Tutti i collegamenti a siti esterni (pagine personali, IRIS, tool GitHub, MathWorks, ecc.) devono avere sempre:
    - `target="_blank"` (apertura in nuova scheda).
    - `rel="noopener noreferrer"` (sicurezza e performance).
    - `title="..."` (tooltip descrittivo per accessibilità e SEO).
    - Eventuale indicatore freccia `↗` per coerenza visiva.

---

## 3. Guida alla Modifica delle Sezioni

Di seguito le istruzioni dettagliate sezione per sezione.

---

### 3.1 Head, SEO, Favicon e Analytics

Posizione: righe `1` - `65`.

```html
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>DYSCO | IMT Lucca Research Unit</title>
  <meta name="description" content="..." />
  <link rel="canonical" href="https://dysco.imtlucca.it/" />

  <!-- Favicon -->
  <link rel="icon" type="image/svg+xml" href="assets/logo.svg" />
  ...
</head>
```

#### Come aggiungere Google Analytics 4 (GA4):

Laddove servisse anche l'ID di misurazione GA4 (`G-XXXXXXXXXX`), incollare il seguente blocco subito prima della chiusura `</head>`:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

### 3.2 Header e Menu di Navigazione

Posizione: righe `75` - `175`.

L'header è fissato in cima alla pagina (`sticky top-0 z-50`). Contiene:

- **Logo DYSCO** a sinistra (link rapido a `#presentation`).
- **Menu Desktop** (`hidden md:flex`): visibile da tablet orizzontale/desktop in su.
- **Pulsante Hamburger** con dropdown mobile (`md:hidden`): si apre al tocco, anima l'icona trasformando le tre linee in una `✕`, si chiude cliccando su un link o all'esterno.

#### Come aggiungere o modificare una voce di menu:

Per aggiungere una voce (es. `News`), aggiungerla sia nel menu desktop che in quello mobile:

1. **Desktop**:
   
   ```html
   <a href="#news" class="flex-grow px-4 py-4 editorial-link text-center flex items-center justify-center">News</a>
   ```

2. **Mobile**:
   
   ```html
   <a href="#news" class="block px-6 py-4 editorial-link">News</a>
   ```

---

### 3.3 Presentation & Hero

Posizione: righe `175` - `335`.

È composta da due blocchi:

1. **Hero superiore** con logo SVG scalabile, titolo `DYSCO` gigante, sottotitolo e sfondo fotografico sfumato con `opacity-20` (`assets/pexels-header-27141316.jpg`).
2. **Griglia di presentazione inferiore**:
   - Colonna sinistra blu (`Research Unit Presentation`) con link a `https://imtlucca.it`.
   - Colonna destra con la mission, gli ambiti di ricerca e l'affiliazione scientifica.

#### Come regolare l'opacità dello sfondo fotografico:

Cercare la riga:

```html
<img src="assets/pexels-header-27141316.jpg" class="... opacity-20" />
```

È possibile modificare `opacity-20` con `opacity-15`, `opacity-25`, ecc., a seconda della luminosità desiderata.

---

### 3.4 Sezione People

Posizione: righe `335` - `600`.

La sezione è suddivisa in 4 macro-colonne responsive (`grid-cols-1 lg:grid-cols-4`):

1. **Faculty**: Professori Ordinari, Associati, Tenure-track e Ricercatori a tempo determinato.
2. **Postdocs**: Ricercatori post-dottorato e borsisti.
3. **PhD Students**: Dottorandi attuali.
4. **Former Members / Alumni**: Collaboratori ed ex-membri.

#### Template per aggiungere un nuovo membro:

Ciascuna persona è inserita dentro un `<li>` con layout flessibile `flex items-center gap-2`. Il nome rimanda alla pagina personale sul sito IMT, seguito dall'icona IRIS con touch target ottimizzato per smartphone:

```html
<li class="flex items-center gap-2">
  <a
    href="https://www.imtlucca.it/nome.cognome"
    target="_blank"
    rel="noopener noreferrer"
    title="Pagina Personale - Nome Cognome"
    class="hover:underline"
    >Nome Cognome</a
  >
  <a
    href="https://iris.imtlucca.it/browse?type=author&authority=rpXXXXX&authority_lang=*"
    target="_blank"
    rel="noopener noreferrer"
    title="IRIS - Nome Cognome"
    class="p-1 -m-1 inline-flex items-center hover:opacity-75 transition-opacity"
  >
    <img
      src="assets/iris-ico.ico"
      alt="IRIS"
      class="w-5 h-5 object-contain"
    />
  </a>
</li>
```

> **Nota:** Se un membro non ha ancora il profilo IRIS o la pagina personale, è sufficiente inserire il solo nome dentro `<li>Nome Cognome</li>` oppure omettere il tag `<a>` corrispondente.

---

### 3.5 Research Topics

Posizione: righe `600` - `660`.

Descrive i filoni di ricerca del gruppo (Model Predictive Control, Embedded Optimization, Machine Learning, ecc.). È strutturata a riquadri border-2. Per modificare un testo o aggiungere un tema, basta aggiornare i rispettivi blocchi `<p>`.

---

### 3.6 Teaching (PhD Courses)

Posizione: righe `660` - `750`.

Elenco dei corsi di dottorato attivati presso IMT Lucca. Ogni corso è racchiuso in un link `<a>` interamente cliccabile che si evidenzia in blu allo scorrimento del mouse:

```html
<li>
  <a
    href="URL_DEL_CORSO"
    target="_blank"
    rel="noopener noreferrer"
    title="Titolo Corso - Course Details"
    class="py-4 border-b-2 border-imt-blue text-xl md:text-2xl uppercase font-bold hover:pl-6 transition-all duration-300 hover:bg-imt-blue hover:text-imt-white flex items-center justify-between gap-4 group"
  >
    <span class="flex items-center gap-4">
      <span class="block w-3 h-3 bg-current flex-shrink-0"></span>
      Nome del Corso
    </span>
    <span class="text-base font-bold pr-2 opacity-0 group-hover:opacity-100 transition-opacity flex-shrink-0">↗</span>
  </a>
</li>
```

---

### 3.7 Software Tools

Posizione: righe `750` - `1050`.

Griglia 3x3 di pacchetti e librerie open-source per MATLAB/Python. Ogni scheda include:

1. Riquadro con **icona vettoriale semantica SVG** (`w-10 h-10 border-2 border-imt-blue group-hover:border-imt-white`).
2. Indicatore di link esterno `↗` ad apparizione su hover.
3. Titolo con sottolineatura (`group-hover:underline`).
4. Descrizione del software.
5. Badge tecnologico a fondo scheda (es. `Python / JAX`, `MATLAB/Simulink`, `European Space Agency`).

#### Template per aggiungere un nuovo Software Tool:

```html
<a
  href="https://github.com/tuo-software"
  target="_blank"
  rel="noopener noreferrer"
  title="Nome Software"
  class="p-6 md:p-8 hover:bg-imt-blue hover:text-imt-white transition-colors duration-200 group flex flex-col justify-between h-full min-h-[220px] border-t-2 border-imt-blue"
>
  <div>
    <div class="flex justify-between items-start gap-2 mb-4">
      <div class="w-10 h-10 border-2 border-imt-blue group-hover:border-imt-white flex items-center justify-center p-2 flex-shrink-0 transition-colors">
        <svg class="w-full h-full fill-none stroke-current" viewBox="0 0 24 24" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <!-- Inserire qui i path dell'icona SVG -->
          <circle cx="12" cy="12" r="9" />
        </svg>
      </div>
      <span class="text-lg opacity-0 group-hover:opacity-100 transition-opacity font-bold flex-shrink-0">↗</span>
    </div>
    <h3 class="text-2xl font-bold uppercase mb-2 group-hover:underline underline-offset-4">
      Nome Software
    </h3>
    <p class="text-base font-medium">
      Breve descrizione dell'algoritmo o della libreria.
    </p>
  </div>
  <p class="text-sm font-bold uppercase tracking-widest opacity-70 mt-4">
    MATLAB / Python
  </p>
</a>
```

---

### 3.8 Applications

Posizione: righe `1050` - `1160`.

Divisa in due aree: colonna identificativa a sinistra (`Applications`) e griglia a quattro riquadri:

- **Automotive**
- **Aerospace**
- **Industrial Process**
- **Energy & Finance**

I testi sono modificabili direttamente nei rispettivi paragrafi.

---

### 3.9 Network (Collaborations, Funding, Events)

Posizione: righe `1160` - `1250`.

Raccoglie in un'unica sezione organica dotata di testata:

- **Collaborations**: Collaborazioni industriali e accademiche globali.
- **Funding**: Finanziamenti e progetti di ricerca (con pulsante `See here →` collegato alla pagina bandi/progetti).
- **Events**: Seminari e conferenze (con pulsante `See here →` collegato alla pagina eventi).

Per aggiornare gli URL dei pulsanti:

```html
<!-- Funding -->
<a href="http://cse.lab.imtlucca.it/~bemporad/projects.html" target="_blank" rel="noopener noreferrer" ...>See here →</a>

<!-- Events -->
<a href="http://cse.lab.imtlucca.it/~bemporad/events.html" target="_blank" rel="noopener noreferrer" ...>See here →</a>
```

---

### 3.10 Spinoff (ODYS S.r.l.)

Posizione: righe `1250` - `1310`.

Realizzata in formato **banner orizzontale compatto**:

- A sinistra: Badge `Spinoff Company` e titolo `ODYS Srl ↗` collegato a `https://www.odys.it`.
- A destra: Breve profilo aziendale con link diretto sia alla scuola IMT che al sito ufficiale.

---

### 3.11 Footer e Pulsante "Torna su"

Posizione: righe `1310` - fine file.

- **Footer**: Include copyright con link alla scuola IMT, indirizzo civico e contatto e-mail istituzionale (`dysco@imtlucca.it`).
- **Floating Button (`#back-to-top`)**: Pulsante quadrato fisso in basso a destra (`fixed bottom-6 right-6`), invisibile in testata, che compare automaticamente dopo aver scrollato 400px.
- **Script JS**: Gestisce l'animazione di comparsa del tasto top e il toggle del menu mobile.

---

## 4. Test Locale e Deploy in Produzione

### Come visualizzare e testare il sito in locale

È possibile avviare un server web locale leggero senza installare Apache o Nginx:

```bash
cd /var/www/dysco # aggiornare il proprio path
python3 -m http.server 8000
```

Aprire il browser all'indirizzo: `http://localhost:8000/dysco.html`

### Validazione e Manutenzione del codice

Per verificare che tutti i tag HTML siano correttamente chiusi e bilanciati prima di pubblicare modifiche:

```bash
python3 -c "
from html.parser import HTMLParser
class C(HTMLParser):
    def __init__(self): super().__init__(); self.s=[]
    def handle_starttag(self,t,a): 
        if t not in {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}: self.s.append(t)
    def handle_endtag(self,t):
        if self.s and self.s[-1]==t: self.s.pop()
with open('dysco.html') as f:
    c = C(); c.feed(f.read())
print('Tag aperti non chiusi:', c.s)
"
```

Se il risultato restituisce `Tag aperti non chiusi: []`, il markup è perfetto.

---