
from youtube_transcript_api import YouTubeTranscriptApi
import inspect

print("Inspecting YouTubeTranscriptApi...")
try:
    if hasattr(YouTubeTranscriptApi, 'list_transcripts'):
        print("has 'list_transcripts'")
    else:
        print("MISSING 'list_transcripts'")

    if hasattr(YouTubeTranscriptApi, 'list'):
        print("has 'list'")
        # Check if it is a bound method or function
        m = getattr(YouTubeTranscriptApi, 'list')
        print(f"Type: {type(m)}")
        print(f"Dir: {dir(m)}")
    else:
        print("MISSING 'list'")

except Exception as e:
    print(f"Error inspecting: {e}")

print("Attempting to call...")
video_id = "J8DXKKJZTtU"

try:
    # Try static/class method list_transcripts
    print("Trying static list_transcripts...")
    YouTubeTranscriptApi.list_transcripts(video_id)
    print("SUCCESS: static list_transcripts")
except Exception as e:
    print(f"FAIL static list_transcripts: {e}")

try:
    # Try static list
    print("Trying static list...")
    YouTubeTranscriptApi.list(video_id)
    print("SUCCESS: static list")
except Exception as e:
    print(f"FAIL static list: {e}")

try:
    # Try instance list
    print("Trying instance list...")
    YouTubeTranscriptApi().list(video_id)
    print("SUCCESS: instance list")
except Exception as e:
    print(f"FAIL instance list: {e}")
