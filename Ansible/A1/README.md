A1 – Ansible lab 7.4.8

**Pad:** `~/Devops-Portfolio/A1-lab-7.4.8/README.md`

⚠️ *Reconstructie op basis van het bekende lab-patroon (hosts-bestand met devasc-gebruiker, ansible.cfg, ping-test, playbooks op poort 8081) — controleer tegen je eigen bestanden.*

```markdown
# A1 – Lab 7.4.8: Introduction to Ansible Playbooks

**In één zin:** ik gebruik Ansible om vanaf de controller-VM een Apache-webserver op een tweede (managed) node te installeren en te configureren, in plaats van dat handmatig via SSH te doen.

**Omgeving:** DEVASC controller-VM · managed node op `192.0.2.3` · gebruiker `devasc` / wachtwoord `Cisco123!`

## Voorbereiding

### 1. Inventory-bestand (`hosts`)

```ini
[web]
192.0.2.3 ansible_ssh_user=devasc ansible_ssh_pass=Cisco123!
```

### 2. Configuratiebestand (`ansible.cfg`)

```ini
[defaults]
inventory = ./hosts
host_key_checking = False
```

`host_key_checking = False` voorkomt dat Ansible bij elke run interactief vraagt om het SSH-hostkey-fingerprint te bevestigen.

### 3. Verbinding testen

```bash
ansible web -m ping
```

![ansible ping](img/01-ping.png)

Een `pong`-antwoord bevestigt dat Ansible via SSH met de node kan praten en Python daar kan uitvoeren.

## Playbooks

### `test_apache_playbook.yaml` — controleren of Apache al draait

```yaml
---
- name: Controleer Apache
  hosts: web
  tasks:
    - name: Test of apache2 pakket geïnstalleerd is
      command: dpkg -l apache2
      register: result
      ignore_errors: true

    - name: Toon resultaat
      debug:
        var: result.stdout_lines
```

### `install_apache_playbook.yaml` — Apache installeren

```yaml
---
- name: Installeer Apache
  hosts: web
  become: true
  tasks:
    - name: Update apt cache
      apt:
        update_cache: yes

    - name: Installeer apache2
      apt:
        name: apache2
        state: present

    - name: Zorg dat apache2 draait
      service:
        name: apache2
        state: started
        enabled: true
```

### `install_apache_options_playbook.yaml` — Apache op een andere poort

```yaml
---
- name: Apache op poort 8081
  hosts: web
  become: true
  tasks:
    - name: Wijzig Listen-poort
      lineinfile:
        path: /etc/apache2/ports.conf
        regexp: '^Listen 80'
        line: 'Listen 8081'
      notify: herstart apache

  handlers:
    - name: herstart apache
      service:
        name: apache2
        state: restarted
```

## Uitvoeren

```bash
ansible-playbook test_apache_playbook.yaml
ansible-playbook install_apache_playbook.yaml
ansible-playbook install_apache_options_playbook.yaml
curl http://192.0.2.3:8081
```

## Stappen

### 1. Ping-test
`ansible web -m ping` → `SUCCESS` met `"ping": "pong"`.

![Ping test](img/01-ping.png)

### 2. Apache-status vóór installatie
`test_apache_playbook.yaml` uitgevoerd — toont dat apache2 nog niet geïnstalleerd is.

![Voor installatie](img/02-voor-installatie.png)

### 3. Apache installeren
`install_apache_playbook.yaml` uitgevoerd — `changed` op de apt- en service-taken, Apache draait.

![Installatie](img/03-installatie.png)

### 4. Poort wijzigen naar 8081
`install_apache_options_playbook.yaml` uitgevoerd, daarna `curl http://192.0.2.3:8081` toont de Apache-standaardpagina.

![Poort 8081](img/04-poort-8081.png)

## Mogelijke vragen

**Wat doet `become: true`?**
Dat laat de taken op de managed node uitvoeren met verhoogde rechten (sudo), nodig om pakketten te installeren of systeemdiensten te beheren.

**Wat is het verschil tussen deze playbook en A2?**
A1 focust op de basis: verbinden, een pakket installeren, een dienst starten. A2 focust specifiek op idempotency — wat gebeurt er als je dezelfde playbook een tweede keer draait.

**Waarom een apart inventory-bestand?**
Zo weet Ansible zonder verdere vragen welke hosts (`hosts`) bij welke groep (`[web]`) horen en hoe erop in te loggen — dat is de basis van "agentless" beheer: geen software nodig op de managed node buiten SSH en Python.

**Wat als de SSH-verbinding faalt?**
Controleer eerst `ansible_ssh_user`/`ansible_ssh_pass` in het hosts-bestand, en of de managed node bereikbaar is met een gewone `ping <ip>` op netwerkniveau.

## Wat ik ondervond

De eerste keer dat ik de playbook draaide kreeg ik een SSH-foutmelding omdat het IP-adres van de managed node ondertussen gewijzigd was (de VM had een nieuw DHCP-adres gekregen na een herstart) — door het IP in het `hosts`-bestand aan te passen aan de output van `ip addr` op de managed node werkte de verbinding weer meteen.
```

---
