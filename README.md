# ZENITHAPPLYAI---A JOB APPLIER AI AGENT
*Elevate Your Job Hunt with an AI JOB APPLIER AGENT*



ZENITHAPPLYAI is a powerful automation engine designed to streamline and enhance your job search process. By leveraging advanced AI and web automation, ZENITHAPPLYAI helps you discover relevant job opportunities and apply to them efficiently, primarily focusing on platforms like LinkedIn. It intelligently processes job descriptions, tailors application materials, and navigates application forms, allowing you to focus on what matters most: landing your next role.

## Key Features
*   **Automated Application Submission**: Intelligently navigates and fills "Easy Apply" forms on supported job platforms (e.g., LinkedIn).
*   **AI-Powered Resume & Cover Letter Customization**: Dynamically tailors your resume summary and generates cover letters to align with specific job requirements, powered by LLMs.
*   **Intelligent Form Filling**: Uses AI to understand and accurately respond to common questions found in job application forms.
*   **Advanced Job Filtering**: Employs user-defined criteria, including company/title blacklists and job attributes, to target the most suitable job openings.
*   **Versatile LLM Integration**: Supports a range of Large Language Models (LLMs) including OpenAI, Anthropic Claude, Google Gemini, local Ollama models, and Hugging Face endpoints, allowing you to choose the best AI for your needs.
*   **Customizable Search Configurations**: Define precise job search parameters such as keywords, locations, experience levels, and job types.
*   **Automated Resume Management**: Works with your provided HTML resume as a base for generating tailored application documents.
*   **Cross-Platform Compatibility**: Designed to run on various operating systems, with setup assistance for Linux/WSL environments.

## Technology Stack
*   **Core Language:** Python
*   **Web Automation:** Selenium
*   **AI/LLM Framework:** Langchain (for interfacing with various LLMs)
*   **LLM Support:** OpenAI, Anthropic Claude, Google Gemini, Ollama, Hugging Face
*   **Configuration:** YAML, .env files
*   **Data Handling:** Beautiful Soup (for HTML parsing during extraction), PDFMiner.six (for document processing if needed by LLM)

## Getting Started

### Prerequisites
*   Python 3.9+
*   pip (Python Package Installer)
*   Google Chrome browser installed
*   (For Linux/WSL) `build-essential`, `libssl-dev`, `libffi-dev`, and potentially other development tools (see `install_auto_linux.sh` for a comprehensive list).

### Installation
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Ifham58741/ZENITHAPPLY-AI
    cd ZENITHAPPLYAI
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    # .venv\Scripts\activate    # On Windows
    ```

3.  **Install Dependencies:**
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
    *(Note: `requirements.txt` at the root of the project contains dependencies for the core automation engine.)*

4.  **Setup ChromeDriver:**
    The application uses `webdriver-manager` which should automatically download and manage the correct ChromeDriver version compatible with your installed Google Chrome. If you encounter issues, ensure Google Chrome is up-to-date.

5.  **Configure ZENITHAPPLYAI:**

    *   **Environment Variables (`.env` file):**
        *   Copy the `.env.example` file (located in the project root) to a new file named `.env`:
            ```bash
            cp .env.example .env
            ```
        *   Edit the `.env` file and provide your API keys for the LLM providers you intend to use (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
        *   You can also configure logging levels and browser behavior (e.g., `HEADLESS` mode) in this file.

    *   **Bot Configuration (`data_folder/config.yaml`):**
        *   Customize this file to define your job search preferences:
            *   `remote`, `experienceLevel`, `jobTypes`, `date` filters.
            *   `searches`: List of locations and job positions to search for.
            *   `distance`: Search radius.
            *   `company_blacklist`, `title_blacklist`, `description_blacklist`: Terms to exclude jobs.
            *   `llm_model_type` & `llm_model`: Specify your chosen LLM provider and model.

    *   **Base Resume (`resumes/resume.html`):**
        *   Place your primary resume in HTML format at `resumes/resume.html`. This file is crucial as the AI uses its content to generate tailored application materials.

    *   **(Optional) Private Context (`data_folder/private_context.yaml`):**
        *   You can provide additional personal details or preferences in this YAML file (following the schema in `assets/resume_schema.yaml`) to further enhance LLM personalization. This file is typically gitignored.

6.  **(For Linux/WSL Users) Automated Setup:**
    You can use the provided shell script to help automate the installation of Python, Chrome, and other dependencies on Ubuntu-based systems (including WSL):
    ```bash
    chmod +x install_auto_linux.sh
    ./install_auto_linux.sh
    ```
    Review the script before running it to understand the changes it will make to your system.

## Usage

1.  **Ensure Configuration:** Double-check your `.env` file for API keys and `data_folder/config.yaml` for your search preferences and LLM choices. Verify your `resumes/resume.html` is up-to-date.
2.  **Activate Virtual Environment:**
    ```bash
    source .venv/bin/activate
    ```
3.  **Run the Automation Engine:**
    Execute the main script from the project's root directory:
    ```bash
    python main.py
    ```
    You can also pass optional arguments:
    ```bash
    python main.py --data-dir path/to/your/data_folder --env-file path/to/your/.env
    ```
    The engine will launch a Chrome browser instance (potentially headless if configured) and begin the job searching and application process according to your `config.yaml`. You may be prompted to log in to LinkedIn manually in the browser window during the first run or if your session expires.

4.  **Monitoring:**
    Check the console output and log files in the `logs/` directory for progress and any potential issues.

5.  **Automated Runs (Optional):**
    The `run_auto_jobs.sh` script provides an example of how to set up automated, periodic runs (e.g., via cron). Remember to make it executable (`chmod +x run_auto_jobs.sh`) and configure paths within the script if necessary.

## Configuration Details

### `.env` File (Root Directory)
Stores sensitive information and operational toggles:
*   `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `HUGGINGFACEHUB_API_TOKEN`: API keys for your chosen LLMs.
*   `CONSOLE_LOG_LEVEL`, `FILE_LOG_LEVEL`: Controls verbosity of logging.
*   `HEADLESS`: Set to `true` to run the browser in headless mode (no visible UI).
*   `CHROME_PROFILE_PATH`: Path to a Chrome user profile directory to persist sessions/cookies.
*   `SKIP_APPLY`: Set to `True` to test job searching and filtering without actual application submission.
*   `DISABLE_DESCRIPTION_FILTER`: Set to `True` to ignore the `description_blacklist` in `config.yaml`.

### `data_folder/config.yaml`
The primary configuration for the bot's behavior:
*   **Search Preferences:** `remote`, `experienceLevel`, `jobTypes`, `date`, `searches` (locations and positions), `distance`.
*   **Blacklists:** `company_blacklist`, `title_blacklist`, `description_blacklist` to filter out unwanted jobs.
*   **LLM Choice:** `llm_model_type` (e.g., `openai`, `ollama`) and `llm_model` (e.g., `gpt-4o-mini`, `llama3`).
*   **Other Settings:** `apply_once_at_company`, `job_applicants_threshold`.

### `resumes/resume.html`
Your base resume in HTML format. The content of this file is used by the AI to tailor applications.

### (Optional) `data_folder/private_context.yaml`
A YAML file (schema in `assets/resume_schema.yaml`) for providing additional structured personal information to the LLM for more personalized outputs. This can include details about your work preferences, availability, salary expectations, etc.

## Future Development
While the core automation engine is powerful, future enhancements may include a dedicated web interface for easier management, enhanced analytics, and broader platform support.


---
*Optimize your job search with ZENITHAPPLYAI!*