
# 🤖 AI-Powered Brochure Generator (Streamlit Web App)
[](https://ai-brochure-generator-shera.streamlit.app/)

This project is an interactive web application built with **Streamlit** and **Python** that automatically generates a professional company brochure. It scrapes a company's website, uses a **Large Language Model (LLM)** to intelligently identify and fetch content from relevant sub-pages (like "About Us" and "Careers"), and synthesizes all the information into a well-structured **Markdown brochure**.

This version evolves the original command-line tool into a user-friendly **web interface**.

---

## ✨ Features

- **Interactive Web UI**: Clean and simple Streamlit interface for easy use.
- **Intelligent Web Scraping**: Starts with a single URL and scrapes the landing page.
- **AI-Powered Link Analysis**: Uses Gemini API to analyze homepage links and identify the most relevant ones (e.g., About, Solutions, Careers).
- **Deep Content Aggregation**: Scrapes identified pages to build a comprehensive content base.
- **Dynamic Brochure Generation**: Aggregated content is fed to Gemini API to write a cohesive brochure.
- **Customizable Tone**: Choose tone (e.g., professional, humorous, technical) via dropdown.
- **Real-Time Status & Streaming**: Displays live feedback during scraping and streams the final brochure with a typewriter effect.

---

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.8+
- [Google AI Studio API Key](https://makersuite.google.com/) or Gemini API Key from Google Cloud
- `uv` (recommended) or `pip` for dependency management

---

### 📦 Clone the Repository

```bash
git clone https://github.com/your-username/ai-brochure-generator.git
cd ai-brochure-generator
````

---

### 🧪 Create a Virtual Environment

#### ✅ Using `uv` (Recommended)

Install `uv`:

**macOS/Linux**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

Create & activate virtual environment:

```bash
uv venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows
```

#### 🧰 Using `venv` (Alternative)

**Windows**:

```bash
python -m venv venv
.\venv\Scripts\activate
```

**macOS/Linux**:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 📥 Install Dependencies

Create a `requirements.txt`:

```txt
google-generativeai
python-dotenv
requests
beautifulsoup4
streamlit
```

Install with:

```bash
# Using uv
uv add -r requirements.txt

# OR using pip
pip install -r requirements.txt
```

---

## 🔐 Configure Your API Key

### A) For Local Development (Recommended)

1. Create a `.env` file in the root directory.
2. Add the following:

```env
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### B) For Streamlit Deployment

1. Go to your app's **Settings > Secrets** on [Streamlit Community Cloud](https://streamlit.io/cloud).
2. Add a new secret:

   * **Key**: `GEMINI_API_KEY`
   * **Value**: your Gemini API key

The app automatically loads from Streamlit secrets when deployed.

---

## 🚀 How to Run the App

With your environment activated, run:

```bash
streamlit run main.py
```

Then:

1. Enter the **Company Name** in the sidebar.
2. Provide the full **Company Website URL**.
3. Select the desired **Tone** for the brochure.
4. Click **"Generate Brochure"**.

The app will display real-time updates and stream the generated brochure.

---

## ⚙️ How It Works: Code Overview

| Component                       | Description                                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `main_streamlit.py / run_app()` | Main script. Uses Streamlit components to build UI and orchestrates the workflow when "Generate" is clicked. |
| `Website` Class                 | Handles scraping and URL resolution using `urllib.parse.urljoin` for robust crawling.                        |
| `get_all_details()`             | Aggregates relevant content from sub-pages, updating the Streamlit UI with `st.info` and `st.warning`.       |
| `stream_brochure()`             | Python generator using `yield` to stream Gemini output in chunks.                                            |
| `st.write_stream()`             | Streams text live to the app using Streamlit's typewriter-like effect.                                       |

---



---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 🧠 Credits

Built with ❤️ using Python, Streamlit, and Gemini API.

