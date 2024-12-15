import re
import os
import json
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
import threading
import time
import subprocess

# Set OpenAI API Key globally
import openai
openai.api_key = "your-api-key"  # Replace this with your actual OpenAI API key

# Function to simulate the llama3.1 model (run locally using Ollama)
def llama3_1_api(prompt, max_tokens=300, temperature=0.7):
    """Run llama3.1 model using Ollama locally."""
    try:
        # Prepare the command to call Ollama
        command = [
            "ollama", "run", "llama3.1", 
            "--text", prompt, 
            "--max-tokens", str(max_tokens),
            "--temperature", str(temperature)
        ]
        # Execute the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()  # Return the output from the model
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error running llama3.1 model: {str(e)}"

def format_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def log_with_timestamp(message):
    """Log messages with a timestamp."""
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def summarize_transcript(transcript_text, model):
    """Summarize the transcript using the chosen model."""
    prompt = (
        "The following text is from a Destin, Florida City Council meeting. "
        "Please summarize the text into comprehensive bullet points:\n\n"
        f"{transcript_text}\n\n"
        "Summary in bullet points:"
    )
    try:
        log_with_timestamp(f"Summarizing transcript using model: {model}")
        if model == "gpt-4o-mini":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()
        elif model == "llama3.1":
            return llama3_1_api(prompt, max_tokens=300, temperature=0.7)
    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"

def analyze_content(transcript_text, model):
    """Analyze the transcript for legal and ethical violations using the chosen model."""
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
    try:
        log_with_timestamp(f"Analyzing content for legal/ethical violations using model: {model}")
        if model == "gpt-4o-mini":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()
        elif model == "llama3.1":
            return llama3_1_api(prompt, max_tokens=500, temperature=0.7)
    except Exception as e:
        return f"Error analyzing content: {str(e)}"

def generate_nextdoor_posts(transcript_text, model):
    """Generate Nextdoor posts based on the transcript using the chosen model."""
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
    try:
        log_with_timestamp(f"Generating Nextdoor posts using model: {model}")
        if model == "gpt-4o-mini":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.5,
            )
            return response['choices'][0]['message']['content'].strip()
        elif model == "llama3.1":
            return llama3_1_api(prompt, max_tokens=150, temperature=0.5)
    except Exception as e:
        return f"Error generating Nextdoor posts: {str(e)}"

def split_into_two_chunks(text):
    """Split text into two approximately equal chunks."""
    words = text.split()
    mid_index = len(words) // 2
    chunk1 = ' '.join(words[:mid_index])
    chunk2 = ' '.join(words[mid_index:])
    return chunk1, chunk2

def fetch_youtube_data():
    """Fetch YouTube video data and process transcript with error handling."""
    try:
        log_with_timestamp("Starting the YouTube video data fetch process.")
        # Create a Tkinter pop-up dialog for the YouTube URL
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        video_url = simpledialog.askstring("Input", "Enter the YouTube video URL:")
        if not video_url:
            raise ValueError("No URL provided. Exiting.")
        
        log_with_timestamp(f"YouTube URL entered: {video_url}")

        # Pop-up for model selection using radio buttons with descriptions
        model_selection = tk.Tk()
        model_selection.title("Choose Model")
        model_var = tk.StringVar(value="gpt-4o-mini")  # Default selection

        tk.Label(model_selection, text="Choose the model to use:").pack()
        tk.Radiobutton(
            model_selection, 
            text="OpenAI gpt-4o-mini (Requires API Token)", 
            variable=model_var, 
            value="gpt-4o-mini"
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            model_selection, 
            text="Llama3.1 (Best Offline Model)", 
            variable=model_var, 
            value="llama3.1"
        ).pack(anchor=tk.W)

        def confirm_selection():
            model_selection.quit()  # Close the model selection window

        tk.Button(model_selection, text="Confirm", command=confirm_selection).pack()
        model_selection.mainloop()  # Start the GUI loop

        # Now that model selection is confirmed, log the selected model
        model = model_var.get()
        log_with_timestamp(f"Model selected: {model}")
        
        video_id = re.search(r"(?:v=|\/)([a-zA-Z0-9_-]{11})(?:[&?]|$)", video_url).group(1)
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}")
        soup = BeautifulSoup(response.text, 'html.parser')

        upload_date_meta = soup.find('meta', {'itemprop': 'uploadDate'})
        formatted_date = datetime.fromisoformat(upload_date_meta['content']).strftime("%Y-%m-%d") if upload_date_meta else "Unknown_Date"
        video_title = soup.find('title').text.replace("- YouTube", "").strip() if soup.find('title') else "Unknown Title"

        log_with_timestamp(f"Video title: {video_title}, Upload date: {formatted_date}")

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join(entry['text'] for entry in transcript)
        chunk1, chunk2 = split_into_two_chunks(transcript_text)

        log_with_timestamp("Splitting transcript into two chunks.")

        # Use multithreading to process each chunk in parallel
        def process_chunk(chunk, chunk_num):
            summary = summarize_transcript(chunk, model)
            legal_analysis = analyze_content(chunk, model)
            nextdoor_posts = generate_nextdoor_posts(chunk, model)
            return (chunk_num, summary, legal_analysis, nextdoor_posts)

        threads = []
        results = []

        def thread_callback(result):
            results.append(result)

        for i, chunk in enumerate([chunk1, chunk2], 1):
            thread = threading.Thread(target=lambda: thread_callback(process_chunk(chunk, i)))
            threads.append(thread)
            thread.start()

        log_with_timestamp("Processing chunks in parallel.")
        for thread in threads:
            thread.join()

        # Prepare JSON data
        json_data = {
            "video_title": video_title,
            "upload_date": formatted_date,
            "transcript": transcript_text,
            "summary": {"part_1": results[0][1], "part_2": results[1][1]},
            "Legal_and_ethical_flag": {"part_1": results[0][2], "part_2": results[1][2]},
            "Next_door": {"part_1": results[0][3], "part_2": results[1][3]},
        }

        os.makedirs("processed_transcriptions", exist_ok=True)
        json_filename = os.path.join("processed_transcriptions", f"{formatted_date}_{video_title}.json")
        with open(json_filename, 'w', encoding='utf-8') as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        log_with_timestamp(f"Data processed successfully. JSON saved to {json_filename}.")
        return f"Data processed successfully using {model}. JSON saved to {json_filename}."
    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Run the script
result = fetch_youtube_data()
print(result)
