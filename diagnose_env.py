
import sys
import os

print(f"Python Executable: {sys.executable}")
print(f"Python Version: {sys.version}")
print(f"CWD: {os.getcwd()}")
print(f"Path: {sys.path}")

try:
    import youtube_transcript_api
    from youtube_transcript_api import YouTubeTranscriptApi
    
    print(f"\n[YouTubeTranscriptApi]")
    print(f"  Version: {getattr(youtube_transcript_api, '__version__', 'unknown')}")
    print(f"  File: {youtube_transcript_api.__file__}")
    print(f"  Has list_transcripts? {'list_transcripts' in dir(YouTubeTranscriptApi)}")
    
    # Try a dry run or just checking the method exists
    try:
        # We don't actually fetch to avoid network/api key usage in diagnosis, just check the attribute
        f = YouTubeTranscriptApi.list_transcripts
        print("  SUCCESS: YouTubeTranscriptApi.list_transcripts exists and is callable.")
    except AttributeError:
         print("  FAILURE: YouTubeTranscriptApi.list_transcripts DOES NOT EXIST.")

except ImportError:
    print("\n[ERROR] youtube_transcript_api NOT INSTALLED.")

