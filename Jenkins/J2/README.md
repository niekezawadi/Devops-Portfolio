# 21. J2 – Jenkins declarative pipeline

**Pad:** `~/Devops-Portfolio/Jenkins/J2/README.md`

```markdown
# J2 – Eigen Jenkins-experiment: declarative pipeline

**In één zin:** ik herschrijf de scripted pipeline van J1 naar de modernere **declarative** syntax, en voeg een wachtlus toe die een flaky (soms falende) test een aantal keer herprobeert vóór de pipeline echt faalt.

## Scripted versus declarative: het verschil

| | Scripted | Declarative |
|---|---|---|
| Syntax | vrije Groovy-code (`node { stage(...) { ... } }`) | vaste structuur (`pipeline { agent ... stages { stage(...) { steps {...} } } }`) |
| Flexibiliteit | zeer flexibel, volledige programmeertaal | beperkter, maar overzichtelijker en leesbaarder |
| Foutafhandeling | manueel met `try/catch`/`catchError` | ingebouwde `post`-sectie (`success`, `failure`, `always`) |
| Aanbevolen voor | complexe, dynamische logica | de meeste "gewone" CI/CD-pipelines |

## Het declarative pipeline-script

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Bouwen van de applicatie...'
                sh 'docker build -t samplerunning-image .'
            }
        }
        stage('Test') {
            steps {
                script {
                    def geslaagd = false
                    for (int i = 1; i <= 15; i++) {
                        echo "Testpoging ${i}/15..."
                        def resultaat = sh(script: 'python3 -m unittest discover', returnStatus: true)
                        if (resultaat == 0) {
                            geslaagd = true
                            break
                        }
                        sleep(2)
                    }
                    if (!geslaagd) {
                        error('Tests bleven falen na 15 pogingen')
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline geslaagd!'
        }
        failure {
            echo 'Pipeline gefaald - controleer de console-output.'
        }
        always {
            echo 'Pipeline afgerond (geslaagd of gefaald).'
        }
    }
}
```

## Uitvoeren

Nieuwe item → **Pipeline** → naam `DeclarativePipeline` → bovenstaand script geplakt in **Pipeline script** → **Save** → **Build Now**.

## Stappen

### 1. Pipeline aanmaken en opslaan
Declarative script geplakt en opgeslagen.

![Pipeline aanmaken](Img/01-pipeline-aanmaken.png)

### 2. Eerste run: Build-stage
Console-output toont de `docker build`-stap.

![Build stage](Img/02-build-stage.png)

### 3. Test-stage met retry-lus
De console-output toont "Testpoging 1/15...", "Testpoging 2/15...", enzovoort, tot de test slaagt of het maximum bereikt wordt.

![Test stage met retries](Img/03-test-retries.png)

### 4. Post-sectie in actie
Na afloop toont de `post`-sectie het juiste bericht (`success` of `failure`), plus altijd het `always`-bericht.

![Post sectie](Img/04-post-sectie.png)

## Mogelijke vragen

**Waarom een retry-lus voor de tests?**
Sommige tests zijn "flaky" — ze falen soms door externe factoren (timing, netwerk) zonder dat de code zelf fout is. Een retry-lus (tot 15 pogingen, met een korte pauze ertussen) geeft de test een eerlijke kans om alsnog te slagen, in plaats van de pipeline meteen te laten falen op één toevallige mislukking.

**Wat doet de `post`-sectie die scripted pipelines niet ingebouwd hebben?**
`post` met `success`/`failure`/`always` is een gestandaardiseerde plek om op te ruimen of te melden na afloop, ongeacht het resultaat — in scripted pipelines moet je dat zelf met `try/catch/finally` bouwen.

**Waarom `returnStatus: true` bij `sh(...)`?**
Standaard laat een `sh`-stap de hele pipeline falen zodra het commando een niet-nul exit code geeft. Met `returnStatus: true` krijg je die exit code als waarde terug, zodat je er zelf logica (de retry-lus) rond kan bouwen in plaats van dat Jenkins meteen stopt.

**Wanneer zou je scripted verkiezen boven declarative?**
Bij complexe, sterk conditionele logica die moeilijk in de vaste declarative structuur past — declarative laat wel toe om binnen een `script { }`-blok terug naar scripted Groovy te schakelen, zoals hierboven bij de retry-lus.

## Wat ik ondervond

Het herschrijven van de scripted pipeline naar declarative dwong me om beter na te denken over de structuur: declarative is strenger, maar daardoor ook overzichtelijker om terug te lezen. De retry-lus was de leukste toevoeging — door bewust een test soms te laten falen kon ik zien hoe de pipeline bleef proberen tot 15 pogingen, in plaats van bij de eerste mislukking meteen rood te kleuren.
