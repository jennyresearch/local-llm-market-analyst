# Market Metrics Analysis & Ticker App
Result from **`metrics_app.py`** 👉🏻 <https://local-llm-market-analyst-metrics.streamlit.app>

## 📌 Project Overview

This repository provides a **market analysis toolkit** and a **web-based ticker application** for financial data exploration, powered by your choice of **local LLM via Ollama** or **OpenAI API**.

The project consists of:

* **`market_analyst.py`** → Core data processing, technical indicator calculation, and LLM analysis functions.
* **`llm_provider.py`** → LLM provider abstraction — switches between Ollama (local) and OpenAI based on user selection.
* **`ticker_app.py`** → Streamlit web app for AI-powered stock analysis with LLM provider selection.
* **`metrics_app.py`** → Streamlit web app showing SMA (20/50-day), RSI, and MACD charts for any ticker over 2 years.
* **`market_metrics_EDA.ipynb`** → Jupyter Notebook for exploratory data analysis (EDA) on market metrics.
* **`requirements.txt`** → Dependency list to replicate the environment.

---

## 🚀 Features

* Fetch live & historical market data using **Yahoo Finance (yfinance)**.
* Run **natural language analysis** on market metrics with your choice of LLM provider:
  * **Ollama (local)** — fully offline, no API key required, privacy-friendly.
  * **OpenAI** — cloud-based GPT-4o, enter your API key directly in the sidebar.
* Interactive charts: **Candlestick, SMA, RSI, MACD** powered by Plotly.
* Clean Streamlit UI with a **Run Analysis** button — analysis only runs when triggered.
* Ready-to-use **exploratory data analysis notebook** for research.

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/market-metrics.git
cd market-metrics
```

### 2. Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate   # On macOS/Linux
.venv\Scripts\activate      # On Windows

pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ LLM Provider Setup

### Option A — Ollama (Local, No API Key)

Ollama lets you run large language models locally on your machine.

**Install Ollama:**

| Platform | Command |
|----------|---------|
| macOS | `brew install ollama` |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh` |
| Windows | Download from [ollama.com/download](https://ollama.com/download) |

**Pull the model:**

```bash
ollama pull gemma3n
```

**Start the Ollama service** (must be running before launching the app):

```bash
ollama serve
```

### Option B — OpenAI (Cloud)

No local setup required. You will enter your OpenAI API key directly in the app sidebar at runtime. The app uses `gpt-4o` by default.

Get an API key at [platform.openai.com](https://platform.openai.com).

---

## ▶️ Usage

### Run the Ticker Analysis App (LLM-powered)

```bash
streamlit run ticker_app.py
```

* Opens at `http://localhost:8501`
* Select your **LLM Provider** (ollama or openai) in the sidebar
* If using OpenAI, paste your **API key** in the sidebar
* Enter a stock ticker and click **Run Analysis**

### Run the Market Metrics Charts App

```bash
streamlit run metrics_app.py
```

* Enter any ticker to view interactive **Candlestick, SMA, RSI, and MACD** charts over 2 years
* Deployed version: 👉🏻 <https://local-llm-market-analyst-metrics.streamlit.app>

### Explore EDA in Jupyter Notebook

```bash
jupyter notebook market_metrics_EDA.ipynb
```

---

## 📈 App Preview

**Ticker Analysis App (`ticker_app.py`)**

<img src="images/local_LLM_visual.png" alt="Local LLM Visual" width="700"/>

> Since it requires complex deployment on Streamlit Community Cloud, only the metrics app is publicly deployed.

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.

##### Remarks: This project is not for investment advice purposes.
