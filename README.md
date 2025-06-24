🤖 AI-Powered Brochure Generator (Streamlit Web App)
This project is an interactive web application, built with Streamlit and Python, that automatically generates a professional company brochure. It scrapes a company's website, uses a Large Language Model (LLM) to intelligently identify and fetch content from relevant sub-pages (like "About Us" and "Careers"), and then synthesizes all the information into a well-structured brochure in Markdown format.

This version evolves the original command-line tool into a user-friendly web interface.

✨ Features
Interactive Web UI: A clean, simple interface built with Streamlit for easy use.

Intelligent Web Scraping: Starts with a single URL and scrapes the landing page.

AI-Powered Link Analysis: Uses the Gemini API to analyze all links on the homepage and identify the most relevant ones for a brochure (e.g., about, solutions, careers).

Deep Content Aggregation: Scrapes the content from the identified relevant pages to build a comprehensive knowledge base.

Dynamic Brochure Generation: Feeds the aggregated content to the Gemini API to write a cohesive and well-structured brochure.

Customizable Tone: Easily change the tone of the brochure (e.g., professional, humorous, technical) via a dropdown menu.

Real-Time Status & Streaming: Provides live feedback during the scraping and generation process and streams the final brochure to the screen.

🛠️ Setup & Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Python 3.8+

A Google AI Studio API Key (or a Gemini API key from Google Cloud).

uv (recommended) or pip for package management.

2. Clone the Repository
git clone <your-repository-url>
cd <repository-directory>

3. Create a Virtual Environment
You can use either the fast uv tool or Python's built-in venv.

Using uv (Recommended):

# Install uv if you don't already have it
# On macOS/Linux:
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
# On Windows:
powershell -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"

# Create and activate the virtual environment
uv venv
source .venv/bin/activate  # On macOS/Linux
.venv\Scripts\activate    # On Windows

Using venv (Alternative):

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

4. Install Dependencies
Create a requirements.txt file with the following content:

google-generativeai
python-dotenv
requests
beautifulsoup4
streamlit

Now, install the packages using your chosen tool.

Using uv:

uv add -r requirements.txt

Using pip:

pip install -r requirements.txt

5. Configure Your API Key
The application securely loads your Gemini API key.

A) For Local Development (Recommended):

Create a file named .env in the root of your project directory.

Add your API key to this file:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

B) For Deployment (Best Practice):
When deploying to Streamlit Community Cloud, use the built-in secrets management.

Go to your app's settings on Streamlit Cloud.

Add a new secret with the name GEMINI_API_KEY and paste your API key as the value.

The application will automatically use the Streamlit secret when deployed.

🚀 How to Run the App
With your environment activated and dependencies installed, run the following command in your terminal:

streamlit run main.py

Your web browser will automatically open with the application running.

Enter the Company Name in the sidebar.

Enter the full Company Website URL.

Select the desired Tone for the brochure.

Click the "Generate Brochure" button.

The main area of the app will show the process status and then display the final, AI-generated brochure.

⚙️ How It Works: The Code Explained
main_streamlit.py / run_app(): This is the main script. The run_app() function uses Streamlit components (st.title, st.sidebar, st.text_input, st.button, etc.) to build the user interface. When the "Generate" button is clicked, it orchestrates the entire process.

Website Class: This class handles web scraping. It now includes logic to convert relative URLs (/about) into absolute URLs (https://company.com/about) using urllib.parse.urljoin, making the scraping more robust.

get_all_details(): This function manages the content aggregation, logging its progress to the Streamlit interface using st.info and st.warning instead of printing to the console.

stream_brochure(): This function has been refactore into a Python generator using the yield keyword. Instead of returning the whole brochure at once, it yields small chunks of text as they are received from the Gemini API.

st.write_stream(): In the run_app function, this powerful Streamlit feature is used to consume the generator (stream_brochure). It automatically renders the text chunks to the screen as they are yielded, creating the live, typewriter-style streaming effect without complex frontend code.
