# AI Watchdog

This program is designed to identify potential ethical violations in city council meetings uploaded to YouTube. It works by fetching the video transcript, analyzing the content using OpenAI's GPT model, and generating a report on possible legal or ethical issues. The script prompts users for a YouTube video URL, processes the transcript, and produces a summary along with an analysis of any concerning content. This automated approach helps citizens and watchdogs efficiently review council meetings for transparency and accountability. The program's output includes detailed descriptions of potential violations, specific laws or ethical standards that may have been breached, and any content that raises legal or ethical concerns15. By automating this process, the tool aims to make it easier for the public to monitor local government activities and ensure compliance with ethical standards6.


## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setup Instructions

1. Clone this repository or download the script to your local machine.

2. Install the required Python packages:

3. Obtain an OpenAI API key:
- Sign up for an account at [OpenAI](https://openai.com/)
- Navigate to the API section and create a new API key
- Copy the API key

4. Open the script in a text editor and replace the placeholder in this line with your actual OpenAI API key:

5. (Optional) If you want to use a different OpenAI model, modify the `model` parameter in the `openai.ChatCompletion.create()` calls.

## Usage

1. Run the script:

2. When prompted, enter the URL of the YouTube video you want to analyze.

3. The script will process the video and generate a JSON file in the `processed_transcriptions` folder. The filename will include the upload date and video title.

## Output

The script generates a JSON file containing:
- Video title and upload date
- Full transcript text
- Summary of the transcript (in two parts)
- Analysis of potential legal and ethical issues (in two parts)
- Generated Nextdoor-style posts (in two parts)

## Customization

You can modify the prompts in the `summarize_transcript()`, `analyze_content()`, and `generate_nextdoor_posts()` functions to adapt the script for different types of videos or analyses.

## Troubleshooting

- If you encounter a "Transcripts are disabled for this video" error, the video owner has not made transcripts available.
- For other errors, check your API key and internet connection, and ensure you have the latest versions of the required packages.

## Disclaimer

This script is for educational and informational purposes only. Always respect YouTube's terms of service and content creators' rights when using this tool.
