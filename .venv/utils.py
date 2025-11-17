import io
import json
import re
from typing import Optional

import docx
import fitz
import psycopg2
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup

import config

DB_NAME = config.DB_NAME
DB_USER = config.DB_USER
DB_PASS = config.DB_PASS
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT


def get_db_connection() -> Optional[psycopg2.extensions.connection]:
    """Establishes a connection to the PostgreSQL database."""
    try:
        return psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
    except ImportError:
        print("Error: psycopg2 library is required for database connection.")
        return None
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def call_gemini_api(prompt_with_data: str) -> str:
    """Sends a prompt to the Gemini API and returns the clean text response."""
    try:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        response = model.generate_content(prompt_with_data)

        cleaned_text = response.text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text.replace("```json\n", "").replace("\n```", "")
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text.replace("```\n", "").replace("\n```", "")

        return cleaned_text
    except Exception as e:
        print(f"Error in Gemini API: {e}")
        return json.dumps({"error": f"Gemini API Error: {str(e)}"})


def read_document(uploaded_file):
    """Reads an uploaded file (PDF or DOCX) and returns its text content."""
    file_name = uploaded_file.name
    text_content = ""

    try:
        uploaded_file.seek(0)

        if file_name.endswith(".pdf"):
            pdf_bytes = uploaded_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text_content += page.get_text()

            pdf_document.close()

        elif file_name.endswith(".docx"):
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            for para in doc.paragraphs:
                text_content += para.text + "\n"

        else:
            text_content = uploaded_file.read().decode("utf-8")

        return text_content

    except Exception as e:
        print(f"Error reading file {file_name}: {e}")
        return f"Error: Could not read file. {e}"


def find_links(cv_text: str):
    """Scans the CV text for relevant URLs and professional profile links."""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    links = re.findall(url_pattern, cv_text)
    found_links = set(links)

    profile_patterns = [
        (r'github\.com/([\w\-]+)', "https://github.com/"),
        (r'linkedin\.com/in/([\w\-]+)', "https://linkedin.com/in/"),
        (r'behance\.net/([\w\-]+)', "https://behance.net/"),
        (r'dribbble\.com/([\w\-]+)', "https://dribbble.com/")
    ]

    for pattern_str, url_prefix in profile_patterns:
        matches = re.findall(re.compile(pattern_str), cv_text)
        for match in matches:
            found_links.add(f"{url_prefix}{match}")

    return list(found_links)


def get_github_context(github_url: str):
    """Fetches public GitHub repository information for a given profile URL."""
    if not github_url:
        return "N/A"

    try:
        username_match = re.search(r'github\.com/([\w\-]+)', github_url)
        if not username_match:
            return "Invalid GitHub URL."

        username = username_match.group(1)
        api_url = f"https://api.github.com/users/{username}/repos"
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(api_url, headers=headers, timeout=10)

        if response.status_code != 200:
            return "Could not fetch GitHub profile. It may be private or invalid."

        repos = response.json()

        if not repos:
            return "GitHub profile found but has no public repositories."

        sorted_repos = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)
        github_context = "GitHub Context (Potential Analysis):\n"

        for repo in sorted_repos[:3]:
            name = repo.get('name', 'N/A')
            description = repo.get('description', 'No description.')
            stars = repo.get('stargazers_count', 0)
            language = repo.get('language', 'N/A')
            github_context += f"- Repo: {name} (Stars: {stars})\n  Description: {description}\n  Language: {language}\n"

        return github_context

    except Exception as e:
        print(f"Error in get_github_context: {e}")
        return "Error processing GitHub profile."


def get_portfolio_context(portfolio_url: str):
    """Scrapes text content from a portfolio website."""
    if not portfolio_url:
        return "N/A"

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(portfolio_url, timeout=10, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text(separator=' ', strip=True)
            return f"Portfolio Context ({portfolio_url}):\n{page_text[:2000]}..."

        return "Could not access portfolio."
    except Exception as e:
        return f"Error reading portfolio: {e}"


def save_to_db(filename, filepath, analysis_json, feedback_email, status):
    """Saves candidate information and analysis results to the PostgreSQL database."""
    sql_query = """
        INSERT INTO candidates
            (cv_filename, cv_filepath, analysis_360, feedback_email_html, status)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        if not conn:
            print("Failed to get database connection.")
            return False

        cursor = conn.cursor()
        cursor.execute(sql_query, (
            filename,
            filepath,
            json.dumps(analysis_json),
            feedback_email,
            status
        ))

        new_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Candidate {new_id} saved successfully to database.")
        return True

    except Exception as e:
        print(f"Error saving to database: {e}")
        if conn:
            conn.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    print("Testing utils.py functions...")

    test_connection = get_db_connection()
    if test_connection:
        print("Database connection: OK")
        test_connection.close()
    else:
        print("Database connection: FAILED")