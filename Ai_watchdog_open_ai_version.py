import re
import os
import json
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from datetime import datetime
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import threading
import time
import subprocess

# Set OpenAI API Key globally
import openai = "Your_Token_here"  # Replace this with your actual OpenAI API key

def generate_response(prompt, selected_model, max_tokens=300, temperature=0.7):
    if selected_model == "llama3.1":
        return llama3_1_api(prompt, max_tokens, temperature)
    elif selected_model == "gpt-4o-mini":
        return openai_api(prompt, max_tokens, temperature)
    else:
        return "Error: Invalid model selected"

def llama3_1_api(prompt, max_tokens=300, temperature=0.7):
    try:
        log_with_timestamp("Calling llama3.1 model on local Ollama server.")
        payload = {
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        if response.status_code == 200:
            return response.json()["response"]
        else:
            log_with_timestamp(f"Ollama server error: {response.text}")
            return f"Error: {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama server: {str(e)}"
    except Exception as e:
        return f"Error running llama3.1 model: {str(e)}"

def format_time(seconds):
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def log_with_timestamp(message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def summarize_transcript(transcript_text, model):
    prompt = (
        "The following text is from a Destin, Florida City Council meeting. "
        "Please summarize the text into comprehensive bullet points:\n\n"
        f"{transcript_text}\n\n"
        "Summary in bullet points:"
    )
    try:
        log_with_timestamp(f"Summarizing transcript using model: {model}")
        if model == "llama3.1":
            return llama3_1_api(prompt, max_tokens=300, temperature=0.7)
        elif model == "gpt-4o-mini":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()
        else:
            return f"Error summarizing transcript: Unsupported model {model}."
    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"

def analyze_content(transcript_text, model):
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
        if model == "llama3.1":
            return llama3_1_api(prompt, max_tokens=500, temperature=0.7)
        elif model == "gpt-4o-mini":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()
        else:
            return f"Error analyzing content: Unsupported model {model}."
    except Exception as e:
        return f"Error analyzing content: {str(e)}"

def generate_nextdoor_posts(transcript_text, model):
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
        if model == "llama3.1":
            return llama3_1_api(prompt, max_tokens=150, temperature=0.5)
        elif model == "gpt-4o-mini":
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.5,
            )
            return response['choices'][0]['message']['content'].strip()
        else:
            return f"Error generating Nextdoor posts: Unsupported model {model}."
    except Exception as e:
        return f"Error generating Nextdoor posts: {str(e)}"

def split_into_two_chunks(text):
    words = text.split()
    mid_index = len(words) // 2
    chunk1 = ' '.join(words[:mid_index])
    chunk2 = ' '.join(words[mid_index:])
    return chunk1, chunk2

def view_json_file(json_filename):
    try:
        with open(json_filename, 'r', encoding='utf-8') as file:
            json_content = file.read()
        viewer = tk.Tk()
        viewer.title(f"Viewing: {os.path.basename(json_filename)}")
        text_widget = tk.Text(viewer, wrap=tk.WORD)
        text_widget.insert(tk.END, json_content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=1, fill=tk.BOTH)
        scrollbar = tk.Scrollbar(viewer, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        viewer.geometry("800x600")
        viewer.mainloop()
    except Exception as e:
        log_with_timestamp(f"Error displaying JSON file: {str(e)}")

class YouTubeTranscriptGUI:
    def __init__(self, master):
        self.master = master
        master.title("YouTube Transcript Processor")
        master.geometry("400x300")

        self.label = tk.Label(master, text="Enter YouTube URL:")
        self.label.pack(pady=10)

        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack(pady=5)

        self.model_label = tk.Label(master, text="Select AI Model:")
        self.model_label.pack(pady=10)

        self.model_buttons_frame = tk.Frame(master)
        self.model_buttons_frame.pack(pady=5)

        self.models = ["llama3.1", "gpt-4o-mini"]
        self.selected_model = tk.StringVar()

        for model in self.models:
            button = ttk.Button(self.model_buttons_frame, text=model, command=lambda m=model: self.select_model(m))
            button.pack(side=tk.LEFT, padx=5)

        self.process_button = ttk.Button(master, text="Process Transcript", command=self.process_transcript)
        self.process_button.pack(pady=20)

    def select_model(self, model):
        self.selected_model.set(model)
        messagebox.showinfo("Model Selected", f"You selected {model}")

    def process_transcript(self):
        url = self.url_entry.get()
        model = self.selected_model.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        if not model:
            messagebox.showerror("Error", "Please select an AI model")
            return
        result = fetch_youtube_data(url, model)
        messagebox.showinfo("Processing Complete", result)

def fetch_youtube_data(video_url, model):
    try:
        log_with_timestamp("Starting the YouTube video data fetch process.")
        log_with_timestamp(f"YouTube URL entered: {video_url}")
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
        view_json_file(json_filename)
        return f"Data processed successfully using {model}. JSON saved to {json_filename}."

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except ValueError as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    root = tk.Tk()
    gui = YouTubeTranscriptGUI(root)
    root.mainloop()
