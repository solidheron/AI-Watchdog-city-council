## AI Watchdog for City Council Meetings

This program uses AI to analyze city council meeting videos on YouTube, identifying potential ethical violations and legal issues.

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/solidheron/AI-Watchdog-city-council.git
   cd AI-Watchdog-city-council
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install required libraries:
   ```bash
   pip install youtube-transcript-api pytube requests beautifulsoup4 openai
   ```

4. Obtain an OpenAI API key from [OpenAI](https://openai.com/) and set it as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

### Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Enter the YouTube URL of the city council meeting when prompted.

3. The analysis will be saved as a JSON file in the `processed_transcriptions` folder.

### License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

This license allows users to use, modify, and distribute the software, including for commercial purposes, as long as they include the original copyright and license notice
