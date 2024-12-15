import re
import os
import json
import requests
import openai
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog

# Set your OpenAI API key directly (for testing purposes only)
openai.api_key = "Put API token here"

def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def summarize_transcript(transcript_text):
    """Use OpenAI API to summarize the given transcript text."""
    prompt = (
        "The following text is from a Destin, Florida City Council meeting. "
        "Please summarize the text into comprehensive bullet points:\n\n"
        f"{transcript_text}\n\n"
        "Summary in bullet points:"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def analyze_content(transcript_text):
    """Use OpenAI API to analyze the given transcript text for legal and ethical violations."""
    prompt = (
        "The following text is from a Destin, Florida City Council meeting. "
        "Please analyze the text and identify any legal or ethical violations. "
        "Report only the following:\n"
        "- Specific laws, regulations, or ethical standards violated.\n"
        "- Detailed descriptions of the violations.\n"
        "- Any content that raises potential legal or ethical concerns.\n\n"
        f"Here is the text to analyze:\n\n{transcript_text}\n\n"
        "Provide a concise report listing all identified violations or concerns."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7,
    )
    return response['choices'][0]['message']['content'].strip()

def generate_nextdoor_posts(transcript_text):
    """
    Generate two concise and straightforward posts for Nextdoor
    based on the provided transcript text.
    """
    prompt = (
        "The following text is from a Destin, Florida City Council meeting. "
        "Based on this content, create simple, dry, short posts for Nextdoor:\n\n"
        f"{transcript_text}\n\n"
        "Each post should:\n"
        "- Be direct and concise.\n"
        "- Use friendly and relatable language.\n"
        "- Reaffirm that the information is sourced from city council meetings.\n"
        "- Be easy to understand for everyone in the community.\n"
        "- Avoid overly formal or technical language.\n"
        "- Omit any enthusiastic or promotional phrases.\n"
        "- No questions.\n"
        "- No emojis or symbols.\n"
        "- Be within 70 words.\n\n"
        "Write the posts as plain text paragraphs without numbering."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.5,
    )
    return response['choices'][0]['message']['content'].strip()

def split_into_two_chunks(text):
    """Split text into two approximately equal chunks."""
    words = text.split()
    mid_index = len(words) // 2  # Find the midpoint for splitting
    # Create two chunks
    chunk1 = ' '.join(words[:mid_index])  # First half
    chunk2 = ' '.join(words[mid_index:])  # Second half
    return chunk1, chunk2

def fetch_youtube_data():
    # Create a Tkinter pop-up dialog for the YouTube URL
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    video_url = simpledialog.askstring("Input", "Enter the YouTube video URL:")

    if not video_url:
        return "No URL provided. Exiting."

    try:
        video_id = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})(?:[&?]|$)", video_url).group(1)
        
        # Fetch video page response
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract upload date from meta tag
        upload_date_meta = soup.find('meta', {'itemprop': 'uploadDate'})
        if upload_date_meta:
            upload_date_str = upload_date_meta['content']
            formatted_date = datetime.fromisoformat(upload_date_str).strftime("%Y-%m-%d")
        else:
            formatted_date = "Unknown_Date"

        # Extract video title
        video_title_tag = soup.find('title')
        video_title = video_title_tag.text.replace("- YouTube", "").strip() if video_title_tag else "Unknown Title"

        print(f"Upload Date: {formatted_date}, Title: {video_title}")

        # Fetch transcript
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Format transcript in SRT format and create plain text for JSON
            plain_transcript_lines = [entry['text'] for entry in transcript]
            transcript_text = " ".join(plain_transcript_lines)

            # Split the transcript text into two chunks
            chunk1, chunk2 = split_into_two_chunks(transcript_text)

            # Summarize and analyze each chunk
            summary1 = summarize_transcript(chunk1)
            summary2 = summarize_transcript(chunk2)
            legal_analysis1 = analyze_content(chunk1)
            legal_analysis2 = analyze_content(chunk2)
            nextdoor_posts_part_1 = generate_nextdoor_posts(chunk1)
            nextdoor_posts_part_2 = generate_nextdoor_posts(chunk2)

            # Create JSON output
            json_data = {
                "video_title": video_title,  # Include video title here
                "upload_date": formatted_date,
                "transcript": transcript_text,
                "summary": {"part_1": summary1, "part_2": summary2},
                "Legal_and_ethical_flag": {"part_1": legal_analysis1, "part_2": legal_analysis2},
                "Next_door": {"part_1": nextdoor_posts_part_1, "part_2": nextdoor_posts_part_2},
            }

            os.makedirs("processed_transcriptions", exist_ok=True)
            json_filename = os.path.join("processed_transcriptions", f"{formatted_date}_{video_title}_open_ai.json")
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            return f"Data processed successfully. JSON saved to {json_filename}."

        except TranscriptsDisabled:
            return "Transcripts are disabled for this video."
        
        except Exception as e:
            return f"Error fetching transcript: {str(e)}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Run the script
result = fetch_youtube_data()
print(result)
