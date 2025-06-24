# main.py
import os
import json
import requests
from typing import List, Dict, Generator
#from dotenv import load_dotenv
from bs4 import BeautifulSoup
import google.generativeai as genai
import streamlit as st
from urllib.parse import urljoin, urlparse

# --- Configuration and Initialization ---

def configure_api():
    """
    Configures the Generative AI API by fetching the API key primarily from
    Streamlit secrets, with a fallback to a local .env file for development.
    """
    # For deployed apps on Streamlit Community Cloud, use st.secrets.
    # We check if the key exists in secrets.
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.info("Configuring API using key from Streamlit secrets.")
    else:
        pass()
        # For local development, load the key from a .env file.
        #st.info("Streamlit secret not found. Attempting to load API key from .env file for local development.")
        #load_dotenv(override=True)
        #api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("Error: GEMINI_API_KEY not found. Please add it to your Streamlit secrets for deployment or to a local .env file.")
        st.stop()
        
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to configure Gemini API: {e}")
        st.stop()


# --- Web Scraping Class ---

class Website:
    """
    A class to represent and scrape a single webpage.
    It fetches the content, extracts the title, clean text, and all links.
    """
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    def __init__(self, url: str):
        self.url = url
        self.title = "No title found"
        self.text = ""
        self.links = []
        
        try:
            response = requests.get(url, headers=self.HEADERS, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            
            self.title = soup.title.string if soup.title else "No title found"
            
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input", "nav", "footer", "header"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)
            else:
                self.text = ""
                
            page_links = [link.get('href') for link in soup.find_all('a')]
            # Convert relative links to absolute and filter
            self.links = [urljoin(self.url, link) for link in page_links if link and not link.startswith(('#', 'mailto:', 'tel:'))]

        except requests.exceptions.RequestException as e:
            st.warning(f"Could not fetch website {self.url}: {e}")

    def get_contents(self) -> str:
        return f"Webpage Title: {self.title}\nWebpage Contents:\n{self.text}\n\n"

# --- AI-Powered Functions ---

def get_relevant_links(website: Website) -> List[Dict[str, str]]:
    """
    Uses Gemini AI to analyze links and identify relevant ones for a brochure.
    """
    st.info(f"AI is analyzing links from {website.url}...")
    
    system_prompt = (
        "You are an expert assistant analyzing website links to identify pages for a company brochure. "
        "Focus on 'About Us', 'Company', 'Solutions', 'Products', or 'Careers'. "
        "Ensure all URLs are absolute. Ignore 'Terms of Service', 'Privacy Policy', social media, or login pages. "
        "Respond ONLY with a JSON object: {\"links\": [{\"type\": \"page type\", \"url\": \"full_url\"}, ...]}"
    )

    user_prompt = (
        f"Base URL: {website.url}\n"
        f"Here are the links from the website. Return the relevant ones in the specified JSON format.\n\n"
        f"Links:\n" + "\n".join(website.links)
    )

    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        response = model.generate_content([system_prompt, user_prompt])
        
        result_json = json.loads(response.text)
        st.success("AI analysis complete. Found relevant links.")
        return result_json.get("links", [])
    except Exception as e:
        st.error(f"An error occurred during AI link analysis: {e}")
        return []

def get_all_details(url: str) -> str:
    """
    Gathers all textual content from the main page and other relevant pages.
    """
    st.info("Step 1: Scraping landing page...")
    main_site = Website(url)
    all_text = f"== START: Content from Landing Page ({url}) ==\n{main_site.get_contents()}== END: Content from Landing Page ==\n\n"

    st.info("Step 2: Finding and scraping relevant sub-pages...")
    relevant_links = get_relevant_links(main_site)

    if not relevant_links:
        st.warning("No relevant sub-pages found by AI. Proceeding with landing page content only.")
        return all_text

    for link_info in relevant_links:
        link_url = link_info.get("url")
        link_type = link_info.get("type", "page")
        if link_url:
            st.info(f"Scraping '{link_type}' page: {link_url}")
            page_content = Website(link_url).get_contents()
            all_text += f"== START: Content from {link_type.title()} Page ({link_url}) ==\n{page_content}== END: Content from {link_type.title()} Page ==\n\n"

    return all_text

def stream_brochure(company_name: str, all_text: str, tone: str) -> Generator[str, None, None]:
    """
    Generates and streams a company brochure, yielding chunks of text.
    """
    system_prompt = (
        f"You are an expert marketing assistant. Write a compelling, {tone} company brochure "
        "in Markdown format. Use the provided text scraped from the company's website. "
        "Structure the brochure logically with clear headings. Highlight company culture, "
        "products/solutions, and career opportunities if available."
    )

    user_prompt = (
        f"Company Name: {company_name}\n\n"
        "Here is the collected content from the company's website. Use this to create the brochure.\n\n"
        f"--- WEBSITE CONTENT ---\n{all_text}"
    )

    try:
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        stream = model.generate_content(
            [system_prompt, user_prompt],
            stream=True
        )
        for chunk in stream:
            yield chunk.text
    except Exception as e:
        st.error(f"An error occurred during brochure generation: {e}")
        yield ""

# --- Streamlit UI ---

def run_app():
    """
    Defines the Streamlit user interface and runs the main application logic.
    """
    st.set_page_config(page_title="AI Brochure Generator", page_icon="🤖", layout="wide")
    st.title("🤖 AI-Powered Company Brochure Generator")
    st.markdown("Enter a company's name and website, and the AI will generate a brochure for prospective clients, investors, and recruits.")
    
    # Configure API at the start
    configure_api()

    with st.sidebar:
        st.header("Configuration")
        company_name = st.text_input("Company Name", placeholder="e.g., Hugging Face")
        url = st.text_input("Company Website URL", placeholder="https://huggingface.co")
        tone = st.selectbox(
            "Select Brochure Tone",
            ("professional", "humorous", "inspirational", "technical")
        )

        generate_button = st.button("Generate Brochure", type="primary")
    
    # Main content area
    if generate_button:
        # Input validation
        if not company_name or not url:
            st.warning("Please enter both a company name and a URL.")
            st.stop()
        
        parsed_url = urlparse(url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
             st.warning("Please enter a valid, full URL (e.g., https://example.com).")
             st.stop()

        st.subheader(f"Generating Brochure for {company_name}...")
        
        # This container will hold all the status updates and the final output
        container = st.container()
        
        with container:
            with st.spinner("Processing... This may take a moment."):
                all_text = get_all_details(url)
                
                st.subheader("Your Generated Brochure")
                st.markdown("---")
                # Use st.write_stream to render the generator's output
                st.write_stream(stream_brochure(company_name, all_text, tone))
                st.success("Brochure generation complete!")


if __name__ == "__main__":
    run_app()
