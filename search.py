
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; SandarbhsAI/1.0)"
}


def domain_of(url):
    try:
        return urlparse(url).hostname.lower().removeprefix("www.")
    except Exception:
        return ""


def source_score(url):
    domain = domain_of(url)

    if domain.endswith(".gov") or domain.endswith(".gov.in"):
        return 5

    if domain.endswith(".edu") or domain.endswith(".ac.in"):
        return 4

    return 1


def read_page(url):
    """Retrieve readable text from a public webpage."""

    try:
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https"):
            return ""

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=8
        )

        response.raise_for_status()

        content_type = response.headers.get(
            "Content-Type", ""
        )

        if "text/html" not in content_type:
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup([
            "script", "style", "nav", "footer",
            "header", "aside", "form"
        ]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)

        return text[:4500]

    except Exception:
        return ""


def web_search(query, max_results=8):
    try:
        results = DDGS().text(
            query,
            region="wt-wt",
            max_results=max_results
        )

        collected = []

        for item in results:
            url = item.get("href", "")
            if not url:
                continue

            domain = domain_of(url)

            if not domain:
                continue

            collected.append({
                "title": item.get("title", ""),
                "snippet": item.get("body", ""),
                "url": url,
                "domain": domain,
                "score": source_score(url)
            })

        # Prioritize official and educational sources.
        collected.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        # Keep different domains where possible.
        unique = []
        seen_domains = set()

        for item in collected:
            if item["domain"] in seen_domains:
                continue

            seen_domains.add(item["domain"])

            # Try to retrieve the actual page.
            item["page_text"] = read_page(item["url"])

            unique.append(item)

            if len(unique) >= max_results:
                break

        return unique

    except Exception as error:
        return [{
            "error": str(error)
        }]
