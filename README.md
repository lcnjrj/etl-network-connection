# Network Connection ETL Pipeline (Linux / NetworkManager)

Autor: Luciana Jorge de Faria / AI
License: MIT
README in English after Portuguese version.

Pipeline ETL desenvolvido em Python para **coletar, transformar, analisar e apresentar dados de conectividade de rede** em sistemas Linux baseados em NetworkManager (ex.: Lubuntu).

O projeto foi criado como exercício prático para os módulos de **Fundamentos de ETL**, **Organização e Apresentação de Dados com Python** e **Exploração de IA Generativa em pipelines**, utilizando dados reais do sistema operacional.

---

## 🎯 Objetivo

Analisar eventos de rede locais, extraindo informações como:

* Conexões e desconexões
* Datas e horários
* Tipo de conexão (Wi-Fi ou Cabeada)
* Duração estimada das conexões
* Padrões de estabilidade e instabilidade

> ⚠️ **Privacidade preservada:** endereços IP e dados sensíveis não são coletados.

---

## 🧱 Arquitetura do Pipeline ETL

```
journalctl (NetworkManager logs)
        ↓
[ Extract ]
Leitura dos logs do systemd
        ↓
[ Transform ]
Normalização de datas
Classificação do tipo de conexão
Cálculo de duração entre eventos
        ↓
[ Load ]
Exportação para CSV
        ↓
[ Analyze ]
Análise com pandas
Agregações e métricas
```

---

## 📂 Estrutura do Projeto

```
conecta_desconecta/
├── etl_network.py        # ETL: extração e transformação dos logs
├── analyze_network.py    # Análise e agregações com pandas
├── network_report.csv    # Dados processados
├── README.md
```

####  Como usar:
python3  etl_network.py
head  network_report.csv
python3  analyze_network.py


## 🔍 Fonte dos Dados

Os dados são extraídos diretamente do **NetworkManager**, via:

```bash
journalctl -u NetworkManager
```

Eventos relevantes analisados:

* `state change`
* `connected`
* `disconnected`
* `ip-config`
* `unavailable`

---

## 📊 Sobre a Análise de Conexões Cabeadas

### ⚠️ Importante: comportamento esperado

Conexões **cabeadas (Ethernet/Fibra)** normalmente:

* Permanecem conectadas por longos períodos
* **Não geram eventos frequentes de desconexão**
* Só aparecem nos logs quando:

  * O sistema inicia
  * O cabo é fisicamente removido
  * A interface é desativada manualmente

Por esse motivo:

* A métrica de **duração baseada apenas em eventos** pode **subestimar o tempo real de uptime**
* Valores como `5.72 minutos` **não indicam instabilidade**, apenas ausência de eventos intermediários

### ✔️ Interpretação correta

| Tipo de conexão | Melhor métrica                         |
| --------------- | -------------------------------------- |
| Wi-Fi           | Eventos + duração entre estados        |
| Cabeada         | **Uptime real** ou ausência de eventos |

A ausência de eventos para a conexão cabeada deve ser interpretada como **sinal de estabilidade**, não como falha do pipeline.

---

## 📈 Exemplo de Análise

```python
import pandas as pd

df = pd.read_csv("network_report.csv")
print(df.groupby("connection_type")["duration_minutes"].sum())
```

Exemplo de saída:

```
connection_type
Cabeada     5.72
Wi-Fi      63.79
```

📌 **Observação técnica**:
Para análises mais precisas de Ethernet, recomenda-se complementar este pipeline com métricas de **uptime contínuo**, como:

* `nmcli device show`
* `/sys/class/net/*/operstate`
* ou coleta periódica por scheduler (cron/systemd timer)

---

## 🤖 Uso de IA Generativa no Pipeline

Este projeto pode ser facilmente estendido com IA Generativa para:

### 1. Geração automática de relatórios

* Converter métricas em **relatórios em linguagem natural**
* Ex.: “A conexão Wi-Fi apresentou X reconexões em Y horas…”

### 2. Identificação de padrões de instabilidade

* Detectar ciclos de reconexão
* Correlacionar horários, interfaces e estados

### 3. Sugestão de melhorias de infraestrutura

* Recomendar uso de cabeamento quando Wi-Fi é instável
* Ajustes de driver, canal ou posicionamento de AP

---

## 🛠️ Tecnologias Utilizadas

* Python 3
* pandas
* systemd / journalctl
* NetworkManager
* Linux (Lubuntu)

---

## 📌 Status

✔ Pipeline funcional
✔ Dados reais do sistema
✔ Privacidade preservada
✔ Pronto para extensão com IA Generativa

# Network Connection ETL Pipeline (Linux / NetworkManager)

This project implements a complete **ETL (Extract, Transform, Load) pipeline** in Python to collect, process, analyze, and present **network connectivity events** from a Linux system using NetworkManager (tested on Lubuntu).

It was developed as a practical project for the **Santander 2025 – Data Science with Python** bootcamp, covering the modules:

* Fundamentals of ETL
* Organizing and Presenting Data with Python
* Exploring Generative AI in an ETL Pipeline

All data comes from the local operating system logs, using real-world system information.

---

## 🎯 Project Objective

Analyze network connection behavior by extracting and transforming system logs to obtain:

* Connection and disconnection events
* Date and time of events
* Connection type (Wired or Wi‑Fi)
* Estimated connection duration
* Indicators of stability and instability

> 🔒 **Privacy by design**: IP addresses and any sensitive network identifiers are intentionally excluded.

---

## 🧱 ETL Pipeline Architecture

```
NetworkManager logs (journalctl)
            ↓
        [Extract]
Read systemd logs
            ↓
       [Transform]
Date normalization
Connection type classification
Duration calculation between events
            ↓
          [Load]
Export structured CSV dataset
            ↓
        [Analyze]
Aggregations and metrics with pandas
```

---

## 📂 Project Structure

```
conecta_desconecta/
├── etl_network.py        # ETL: extract and transform network logs
├── analyze_network.py    # Data analysis with pandas
├── network_report.csv    # Generated dataset
├── README.md
```

---

## 🔍 Data Source

Data is extracted from **NetworkManager** using systemd logs:

```bash
journalctl -u NetworkManager
```

Relevant events include:

* `state change`
* `connected`
* `disconnected`
* `ip-config`
* `unavailable`

---

## 📊 Interpreting Wired vs Wi‑Fi Connections

### ⚠️ Important Technical Note

**Wired (Ethernet / Fiber) connections** behave differently from Wi‑Fi in system logs:

* They usually remain connected for long periods
* They **do not generate frequent connect/disconnect events**
* Events typically appear only when:

  * The system boots
  * The cable is physically unplugged
  * The interface is manually disabled

Because of this behavior:

* Event-based duration calculations may **underestimate real uptime**
* Low duration values for wired connections **do not indicate instability**

### ✅ Correct Interpretation

| Connection type | Recommended quality metric             |
| --------------- | -------------------------------------- |
| Wi‑Fi           | Event frequency + duration             |
| Wired           | Continuous uptime or absence of events |

In this pipeline, the **absence of events for wired connections is interpreted as stability**, not as missing data.

---

## 📈 Example Analysis

```python
import pandas as pd

df = pd.read_csv("network_report.csv")
print(df.groupby("connection_type")["duration_minutes"].sum())
```

Example output:

```
connection_type
Wired      5.72
Wi-Fi     63.79
```

📌 **Technical note**: For production-grade monitoring, wired connections should be complemented with:

* `nmcli device show`
* `/sys/class/net/*/operstate`
* Periodic sampling via cron or systemd timers

---

## 🤖 Exploring Generative AI in the ETL Pipeline

This project demonstrates how **Generative AI** can be integrated into a data pipeline to enhance analysis and decision-making.

### 1️⃣ Automatic Natural Language Reports

Generative AI models can transform structured metrics into **human-readable reports**, for example:

> "During the analyzed period, the Wi‑Fi connection experienced multiple reconnections, while the wired connection remained stable with no significant interruptions."

This allows technical data to be easily understood by non-technical stakeholders.

---

### 2️⃣ Detection of Instability Patterns

By feeding the processed dataset into a generative or analytical AI model, it is possible to:

* Identify recurring reconnection cycles
* Detect time-based patterns (e.g., instability at specific hours)
* Correlate interface states with connection drops

Generative AI can summarize these findings and highlight potential issues automatically.

---

### 3️⃣ Infrastructure Improvement Suggestions

Based on detected patterns, Generative AI can suggest improvements such as:

* Prefer wired connections when Wi‑Fi instability is recurrent
* Adjust Wi‑Fi channel or access point positioning
* Update drivers or firmware
* Improve physical network layout

These recommendations can be generated dynamically from the data, closing the loop between **analysis and action**.

---

## 🛠️ Technologies Used

* Python 3
* pandas
* systemd / journalctl
* NetworkManager
* Linux (Lubuntu)

---

## 📌 Project Status

* ✔ Functional ETL pipeline
* ✔ Real system data
* ✔ Privacy-preserving design
* ✔ Ready for Generative AI extensions

---

This repository demonstrates the practical application of **ETL concepts, data organization, and Generative AI exploration** using real Linux system data, aligned with the objectives of the Santander 2025 Data Science with Python program.
