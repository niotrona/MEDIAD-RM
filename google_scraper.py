import requests
from bs4 import BeautifulSoup

def google_search_titles_snippets(keyword: str, max_results: int = 10):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    query = keyword.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for result in soup.select("div.g")[:max_results]:
        title = result.select_one("h3")
        snippet = result.select_one(".VwiC3b")
        if title and snippet:
            results.append({
                "title": title.text.strip(),
                "snippet": snippet.text.strip()
            })
    return results
