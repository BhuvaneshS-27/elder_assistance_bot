import re
import requests
import feedparser
from datetime import datetime, timedelta

# Short-lived cache per category, purely to avoid re-fetching on every
# repeat question — same policy as weather_client.py: a failed live
# fetch returns None honestly, it never serves stale data as current.
CACHE_FRESHNESS = timedelta(minutes=20)

# Google News RSS, India edition (hl/gl/ceid=IN) — aggregates from
# Indian publishers (Times of India, NDTV, Hindustan Times, etc.)
# automatically per category. Chosen over hardcoding individual
# publishers' category feeds since those numeric/slug-based URLs
# couldn't be reliably verified as currently live from here, whereas
# this URL pattern has been stable for years and is well documented.
_GOOGLE_NEWS_IN = "https://news.google.com/rss"
_IN_PARAMS = "hl=en-IN&gl=IN&ceid=IN:en"

FEEDS = {
    "general": f"{_GOOGLE_NEWS_IN}?{_IN_PARAMS}",
    "world": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/WORLD?{_IN_PARAMS}",
    "technology": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/TECHNOLOGY?{_IN_PARAMS}",
    "business": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/BUSINESS?{_IN_PARAMS}",
    "health": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/HEALTH?{_IN_PARAMS}",
    "science": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/SCIENCE?{_IN_PARAMS}",
    "entertainment": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/ENTERTAINMENT?{_IN_PARAMS}",
    "sports": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/SPORTS?{_IN_PARAMS}",
    "politics": f"{_GOOGLE_NEWS_IN}/headlines/section/topic/NATION?{_IN_PARAMS}",
}

_cache = {}  # category -> {"data": [...], "fetched_at": datetime}


def _strip_html(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&nbsp;", " ")
    )
    return text.strip()


def _clean_google_title(title):
    """
    Google News titles are usually "Headline - Publisher Name".
    Strip the trailing publisher name for cleaner speech.
    """
    title = title.strip()
    if " - " in title:
        title = title.rsplit(" - ", 1)[0].strip()
    return title


def _fetch_live(category, count):
    url = FEEDS.get(category, FEEDS["general"])

    # Fetch via requests (not feedparser's own fetching) so we get a
    # controlled timeout and clean exceptions — same pattern as
    # weather_client.py — rather than feedparser potentially hanging
    # with no internet.
    response = requests.get(url, timeout=5)
    response.raise_for_status()

    parsed = feedparser.parse(response.content)

    headlines = []
    for entry in parsed.entries[:count]:
        title = _clean_google_title(entry.get("title", ""))
        if title:
            # Google News' RSS "summary" is a jumbled HTML list of
            # related article links, not a clean one-line summary —
            # unlike BBC's feeds, so it's intentionally left empty
            # here rather than producing garbled speech.
            headlines.append({"title": title, "summary": ""})

    return headlines


def get_headlines(category="general", count=3):
    """
    Returns a list of {"title", "summary"} dicts, or None if a live
    fetch failed and there's no fresh cache to fall back on.
    """
    now = datetime.now()
    cached = _cache.get(category)

    if cached and (now - cached["fetched_at"] < CACHE_FRESHNESS):
        return cached["data"]

    try:
        data = _fetch_live(category, count)
        if not data:
            return None
        _cache[category] = {"data": data, "fetched_at": now}
        return data
    except Exception as e:
        print("News fetch error:", e)
        return None