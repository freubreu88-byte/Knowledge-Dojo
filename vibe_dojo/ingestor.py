"""Content ingestion from URLs and text."""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from ulid import ULID


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = str(text).lower()  # Ensure string type
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def fetch_youtube_transcript(url: str) -> tuple[str, str]:
    """Fetch YouTube transcript with multi-language fallback (v1.2.3+)."""
    from youtube_transcript_api import YouTubeTranscriptApi

    # Extract video ID
    video_id_match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not video_id_match:
        raise ValueError("Invalid YouTube URL")

    video_id = video_id_match.group(1)
    
    try:
        # Try German first, then English
        # Use static method properly
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(["de", "en"])
        transcript_data = transcript.fetch()
        text = " ".join([entry["text"] for entry in transcript_data])
        return text, "youtube-transcript-api-v1"
    except Exception as e:
        # Fallback: catch any available transcript if specific languages fail
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            # Find any available transcript, prioritizing known languages
            # This handles auto-generated and translated transcripts
            transcript = transcript_list.find_transcript(["de", "en"])
            text = " ".join([entry["text"] for entry in transcript.fetch()])
            return text, "youtube-transcript-api-fallback"
        except Exception as fallback_err:
            raise ValueError(f"Could not retrieve transcript for {url}: {fallback_err}") from e


def fetch_reddit_content(url: str) -> tuple[str, str]:
    """Fetch Reddit post content."""
    import requests

    # Add .json to URL
    json_url = url.rstrip("/") + ".json"
    response = requests.get(json_url, headers={"User-Agent": "vibe-dojo/0.1.0"})
    response.raise_for_status()

    data = response.json()
    post = data[0]["data"]["children"][0]["data"]

    # Combine title and selftext
    text = f"# {post['title']}\n\n{post.get('selftext', '')}"
    return text, "reddit-json-api"


def fetch_article(url: str) -> tuple[str, str]:
    """Fetch article content using trafilatura."""
    import trafilatura

    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Failed to download URL")

    text = trafilatura.extract(downloaded)
    if not text:
        raise ValueError("Failed to extract content")

    return text, "trafilatura"


def fetch_url(url: str) -> tuple[str, str]:
    """Auto-detect and fetch content from URL."""
    if "youtube.com" in url or "youtu.be" in url:
        return fetch_youtube_transcript(url)
    elif "reddit.com" in url:
        return fetch_reddit_content(url)
    else:
        return fetch_article(url)


def create_source_note(
    vault_path: Path,
    url: Optional[str] = None,
    text: Optional[str] = None,
    title: Optional[str] = None,
    no_fetch: bool = False,
) -> Path:
    """Create a source note in 00_Inbox/.

    Args:
        vault_path: Path to vault
        url: URL to fetch (if provided)
        text: Manual text (if no URL or no_fetch)
        title: Optional title override
        no_fetch: If True, don't fetch URL (requires text)

    Returns:
        Path to created source note
    """
    source_id = str(ULID())
    captured_at = datetime.now().isoformat()

    # Determine content and method
    if url and not no_fetch:
        try:
            content, fetch_method = fetch_url(url)
            source_kind = "youtube" if "youtube" in url else "reddit" if "reddit" in url else "blog"
        except Exception as e:
            raise ValueError(f"Failed to fetch URL: {e}")
    elif text:
        content = text
        fetch_method = "manual"
        source_kind = "manual"
    else:
        raise ValueError("Must provide either URL or text")

    # Generate title if not provided
    if not title:
        if url:
            title = url.split("/")[-1][:50]
        else:
            title = content[:50].replace("\n", " ")

    slug = slugify(title)

    # Save large content to attachment
    inbox_path = vault_path / "00_Inbox"
    attachments_path = inbox_path / "_attachments"
    attachments_path.mkdir(parents=True, exist_ok=True)

    attachment_file = attachments_path / f"{source_id}.txt"
    attachment_file.write_text(content, encoding="utf-8")

    # Create lean source note
    frontmatter = f"""---
id: {source_id}
source_kind: {source_kind}
url: {url or ""}
captured_at: {captured_at}
fetch_method: {fetch_method}
transcript_path: 00_Inbox/_attachments/{source_id}.txt
---

# {title}

**Source:** {url or "Manual entry"}
**Captured:** {captured_at}

## Content Preview
{content[:300]}...

---
*Full content in: `{attachment_file.relative_to(vault_path)}`*
"""

    note_file = inbox_path / f"SOURCE__{slug}.md"
    note_file.write_text(frontmatter, encoding="utf-8")

    return note_file
