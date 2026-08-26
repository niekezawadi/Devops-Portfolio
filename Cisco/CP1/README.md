CP1 – Cisco Platforms / examenvoorbereiding

**Pad:** `~/Devops-Portfolio/Cisco-Platforms/CP1/README.md`

```markdown
# CP1 – Automation, IaC & Cisco Platforms: voorbereiding op het examen

**In één zin:** een overzichtstabel (Google Sheet) waarin ik per Cisco-platform/tool (bv. Meraki, DNA Center, Webex, UCS, ACI, ...) samenvat wat het platform doet, welke API het aanbiedt, en hoe dat aansluit op wat ik in de andere oefeningen van dit portfolio al heb toegepast.

## Waarom een spreadsheet in plaats van code

Dit onderdeel van de cursus gaat niet over zelf code schrijven, maar over **overzicht en begrip** van het brede Cisco-automatiseringslandschap — een tabel leent zich daar beter toe dan een script.

## Werkwijze

1. Het gedeelde Google Sheet-sjabloon van de docent geopend.
2. Omdat de DEVASC-VM een verouderde/embedded Chromium-versie gebruikt, blokkeerde Google het inloggen met "This browser or app may not be secure" — een gekende beperking van oudere ingebedde browsers, niet oplosbaar via instellingen in de VM zelf.
3. **Oplossing:** de kopie van het sjabloon gemaakt op mijn eigen, gewone computer (waar ik al ingelogd was met mijn Google-account), de tabel daar volledig ingevuld, en enkel de resulterende deel-link overgenomen naar de VM voor dit README-bestand en de git-commando's.
4. De acht rijen in één keer als tabgescheiden tekst gekopieerd en in één keer geplakt in de spreadsheet (in plaats van cel per cel), wat veel sneller ging.

## Inhoud van de tabel (samenvatting)

| Platform/tool | Wat het doet | API-type | Link naar eigen ervaring |
|---|---|---|---|
| Meraki | Cloud-beheerd netwerkbeheer (switches, AP's, camera's) | REST API | Zelfde REST-principes als Ap1 (GET/POST met token) |
| Cisco DNA Center | Netwerk-automatisering en -assurance | REST API + Intent API | Vergelijkbaar met Ansible-aanpak (gewenste eindtoestand) uit A1/A2 |
| Webex | Team-samenwerking, chat, meetings | REST API | Rechtstreeks toegepast in W1 |
| UCS Manager | Serverhardwarebeheer (Cisco Unified Computing System) | XML API / REST (UCS Central) | Infrastructure as Code-principe, vergelijkbaar met Docker-images als "blauwdruk" |
| ACI (Application Centric Infrastructure) | Softwarematig gedefinieerd datacenternetwerk | REST API (APIC) | Policy-gebaseerde configuratie, vergelijkbaar met idempotency in Ansible |
| NSO (Network Services Orchestrator) | Multi-vendor netwerkorkestratie via YANG-modellen | NETCONF/RESTCONF | Orchestratie-laag, vergelijkbaar met hoe Jenkins J1/J2 losse jobs orkestreert |
| SD-WAN (vManage) | Beheer van software-defined WAN | REST API | Centraal dashboard + API, zoals Jenkins een centraal CI/CD-dashboard is |
| PSIRT / openVuln API | Cisco-beveiligingsadvisories opvragen | REST API | Zelfde authenticatiepatroon (token/OAuth) als in Ap1/W1 |

*(Volledige, ingevulde tabel met bronvermeldingen staat in het gedeelde Google Sheet — link opgenomen in de commit/portfolio-index.)*

## Link naar het Google Sheet

`[LINK_NAAR_GEDEELDE_GOOGLE_SHEET_HIER]`

## Stappen

### 1. Sjabloon geopend, inlogblokkade vastgesteld
Poging om in te loggen in de VM's Chromium gaf "Couldn't sign you in — This browser or app may not be secure".

![Inlogblokkade](Img/01-inlogblokkade.png)

### 2. Overgestapt naar eigen computer
Op mijn eigen, normale computer ingelogd, kopie van het sjabloon gemaakt via **Bestand → Een kopie maken**.

![Kopie gemaakt](Img/02-kopie-gemaakt.png)

### 3. Tabel in één keer ingevuld
Alle acht rijen als tabgescheiden tekst in één keer geplakt in plaats van cel per cel.

![Tabel ingevuld](Img/03-tabel-ingevuld.png)

### 4. Link teruggekopieerd naar de VM
Deel-link van het Google Sheet gekopieerd en in dit README-bestand op de VM geplakt.

![Link in README](Img/04-link-in-readme.png)

## Mogelijke vragen

**Waarom kon je niet inloggen in de VM zelf?**
De ingebedde/verouderde Chromium-versie in de DEVASC-VM voldoet niet meer aan Google's moderne beveiligingsvereisten voor inloggen, dus blokkeert Google het sign-in-proces preventief — een bekende beperking van oudere embedded browsers, niet van mijn account of instellingen.

**Wat is het gemeenschappelijke thema tussen al deze Cisco-platformen?**
Ze bieden allemaal een API (REST, NETCONF/RESTCONF, of XML) waarmee je configuratie en beheer kan automatiseren in plaats van via een grafische interface te klikken — exact hetzelfde principe dat doorheen dit hele portfolio terugkomt (API's, Ansible, Docker, Jenkins).

**Waarom is Infrastructure as Code relevant voor UCS/ACI?**
Omdat je de gewenste configuratie (serverprofiel, netwerkpolicy) als code/model beschrijft, en het platform zelf zorgt dat de werkelijke toestand overeenkomt — hetzelfde idempotency-principe als bij Ansible (A1/A2).

## Wat ik ondervond

Het lastigste aan deze opdracht was niet de inhoud, maar de technische blokkade bij het inloggen in Google vanuit de VM — in plaats van te blijven vechten tegen een verouderde browser, was de eenvoudigste oplossing om het gewoon op mijn eigen computer te doen en enkel de link mee te nemen. Inhoudelijk was het overzicht leerzaam omdat ik pas tijdens het invullen goed besefte hoeveel van de Cisco-platformen uiteindelijk hetzelfde onderliggende principe delen (een API aanspreken) als wat ik al in Ap1, A2 en W1 had toegepast.
```

---
