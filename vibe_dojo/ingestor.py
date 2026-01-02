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



def format_timestamp(seconds: float) -> str:
    """Format seconds to MM:SS or HH:MM:SS."""
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def parse_iso8601_duration(duration_str: str) -> int:
    """Parse ISO 8601 duration string to minutes."""
    match = re.search(
        r'P(?:(?P<weeks>\d+)W)?(?:(?P<days>\d+)D)?T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?',
        duration_str
    )
    if not match:
        return 0
    
    parts = match.groupdict()
    total_minutes = 0
    if parts['weeks']:
        total_minutes += int(parts['weeks']) * 7 * 24 * 60
    if parts['days']:
        total_minutes += int(parts['days']) * 24 * 60
    if parts['hours']:
        total_minutes += int(parts['hours']) * 60
    if parts['minutes']:
        total_minutes += int(parts['minutes'])
    # Ignore seconds for minutes granularity
    
    return total_minutes


def fetch_youtube_metadata_official(video_id: str) -> dict:
    """Fetch official metadata using YouTube Data API v3."""
    import os
    from googleapiclient.discovery import build
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        return {}
        
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.videos().list(
            part='snippet,contentDetails',
            id=video_id
        ).execute()
        
        if not response['items']:
            return {}
            
        item = response['items'][0]
        snippet = item['snippet']
        content_details = item['contentDetails']
        
        # Simple chapter extraction from description
        chapters = []
        description = snippet.get('description', '')
        # Regex for "00:00 Chapter Name" or "0:00 Chapter Name"
        chapter_matches = re.findall(r'(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)', description)
        for timestamp, title in chapter_matches:
            chapters.append({"timestamp": timestamp, "title": title})
            
        return {
            'title': snippet['title'],
            'description': description,
            'duration': content_details['duration'],
            'duration_minutes': parse_iso8601_duration(content_details['duration']),
            'upload_date': snippet['publishedAt'],
            'channel': snippet['channelTitle'],
            'chapters': chapters
        }
    except Exception:
        # Silently fail back to basic metadata if API errors
        return {}


def fetch_youtube_transcript(url: str) -> tuple[str, str, dict]:
    """Fetch YouTube transcript with timestamps and official metadata."""
    from youtube_transcript_api import YouTubeTranscriptApi
    
    # Extract video ID
    video_id_match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not video_id_match:
        raise ValueError("Invalid YouTube URL")
        
    video_id = video_id_match.group(1)
    
    # Fetch Official Metadata
    metadata = fetch_youtube_metadata_official(video_id)
    metadata["video_id"] = video_id
    
    try:
        # Fetch transcript
        # Compatibility: Handling different library versions found in wild
        if hasattr(YouTubeTranscriptApi, 'list_transcripts'):
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        elif hasattr(YouTubeTranscriptApi, 'list'):
            # Fallback for version requiring instantiation
            transcript_list = YouTubeTranscriptApi().list(video_id)
        else:
             # Try instantiation with list_transcripts (just in case)
             transcript_list = YouTubeTranscriptApi().list_transcripts(video_id)
             
        transcript = transcript_list.find_transcript(["de", "en"])
        transcript_data = transcript.fetch()
        
        # Format with timestamps
        formatted_lines = []
        for entry in transcript_data:
            # Handle both dict (standard) and object (legacy/variant) responses
            if isinstance(entry, dict):
                start = entry['start']
                text = entry['text']
            else:
                # Assume object attributes
                start = getattr(entry, 'start', 0)
                text = getattr(entry, 'text', "")
                
            timestamp = format_timestamp(start)
            formatted_lines.append(f"[{timestamp}] {text}")
            
        full_text = "\n".join(formatted_lines)
        
        return full_text, "youtube-transcript-api-v1.2.3+timestamps", metadata
        
    except Exception as e:
        raise ValueError(f"Could not retrieve transcript for {url}: {e}")


def fetch_reddit_content(url: str) -> tuple[str, str, dict]:
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
    metadata = {
        "title": post['title'],
        "author": post['author'],
        "subreddit": post['subreddit'],
    }
    return text, "reddit-json-api", metadata


def fetch_article(url: str) -> tuple[str, str, dict]:
    """Fetch article content using trafilatura."""
    import trafilatura
    
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Failed to download URL")
        
    text = trafilatura.extract(downloaded)
    if not text:
        raise ValueError("Failed to extract content")
        
    # Basic metadata extraction could be added here
    metadata = {}
    return text, "trafilatura", metadata


def fetch_url(url: str) -> tuple[str, str, dict]:
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
    extra_metadata = {}

    # Determine content and method
    if url and not no_fetch:
        try:
            content, fetch_method, extra_metadata = fetch_url(url)
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
        if extra_metadata.get("title"):
             title = extra_metadata["title"]
        elif url:
            title = url.split("/")[-1][:50]
        else:
            title = content[:50].replace("\n", " ")

    # Quality Gate: Check duration
    duration_mins = extra_metadata.get("duration_minutes", 0)
    if duration_mins > 180:
        from rich.prompt import Confirm
        print(f"\n⚠️  [yellow]Warning: Video is {duration_mins} minutes long (very long).[/yellow]")
        print("   Distilliation might take longer and use more tokens.")
        if not Confirm.ask("   Continue processing?"):
            return None # Or handle graceful exit

    slug = slugify(title)

    # Save large content to attachment
    inbox_path = vault_path / "00_Inbox"
    attachments_path = inbox_path / "_attachments"
    attachments_path.mkdir(parents=True, exist_ok=True)

    attachment_file = attachments_path / f"{source_id}.txt"
    attachment_file.write_text(content, encoding="utf-8")
    
    # Format metadata as YAML block if it exists
    metadata_yaml = ""
    if extra_metadata:
        import yaml
        # Dump clean metadata dict to YAML string
        metadata_yaml = yaml.dump(extra_metadata, sort_keys=False, indent=2)
        # Indent it for embedding
        metadata_yaml = "\n".join("  " + line for line in metadata_yaml.splitlines())

    # Create lean source note
    frontmatter = f"""---
id: {source_id}
source_kind: {source_kind}
url: {url or ""}
captured_at: {captured_at}
fetch_method: {fetch_method}
transcript_path: 00_Inbox/_attachments/{source_id}.txt
video_metadata:
{metadata_yaml}
---

# {title}

**Source:** {url or "Manual entry"}
**Captured:** {captured_at}
{f"**Duration:** {duration_mins} min" if duration_mins > 0 else ""}

## Content Preview
{content[:300]}...

---
*Full content in: `{attachment_file.relative_to(vault_path)}`*
"""

    note_file = inbox_path / f"SOURCE__{slug}.md"
    note_file.write_text(frontmatter, encoding="utf-8")

    return note_file
