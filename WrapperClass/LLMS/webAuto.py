# web_automator.py
import time
import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import subprocess
import sys

class WebDevAutomator:
    def __init__(self):
        """Initialize WebDevAutomator with OpenAI and project settings."""
        load_dotenv()
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key)
        self.base_dir = r'C:\Users\shiva\Desktop\DEVIN\output' # use your own base directory where you want to store your output file
        self.project_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize OpenAI assistant
        self.assistant = self.client.beta.assistants.create(
            name="Developer",
            instructions='''You're an expert in web development, proficient in HTML, CSS, JavaScript, and React.
            Your skills extend beyond conventional methods, allowing you to seamlessly integrate all three languages into a single HTML file.
            Your CSS prowess shines through as you craft stylesheets with elegance and efficiency.''',
            model="gpt-4-0125-preview",
        )
        self.thread = self.client.beta.threads.create()

    def run_assistant(self, user_instructions):
        """Run OpenAI assistant with given instructions."""
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions=user_instructions,
        )

        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id, 
                run_id=run.id
            )
            if run.status == "completed":
                print("Successfully generated code, preparing to deploy!")
                break
            print("Working on it...")
            time.sleep(5)

        return self.get_assistant_response()

    def get_assistant_response(self):
        """Get the response from the assistant."""
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        message_store = []
        
        for message in messages:
            if message.assistant_id == self.assistant.id:
                message_store.append(message.content[0].text.value)
        
        return "".join(reversed(message_store))

    def format_html_input(self, input_text: str) -> str:
        """Format HTML input by extracting HTML block."""
        input_lines = input_text.split('\n')
        html_lines = []
        in_html_block = False

        for line in input_lines:
            if line.strip().startswith('<!DOCTYPE html>'):
                in_html_block = True
            if in_html_block:
                html_lines.append(line)
            if line.strip().endswith('</html>'):
                in_html_block = False

        return '\n'.join(html_lines)

    def separate_sections(self, code, jsx_path, css_path):
        """Separate JSX and CSS code from the response."""
        lines = code.split('\n')
        jsx_content = []
        css_content = []
        section = None

        for line in lines:
            if '```jsx' in line:
                section = 'jsx'
                continue
            elif '```css' in line:
                section = 'css'
                continue
            elif '```' in line:
                section = None
                continue

            if section == 'jsx':
                jsx_content.append(line + '\n')
            elif section == 'css':
                css_content.append(line + '\n')

        with open(jsx_path, 'w') as jsx_file:
            jsx_file.writelines(jsx_content)

        with open(css_path, 'w') as css_file:
            css_file.writelines(css_content)

        print("Files separated successfully.")

    def create_html_project(self, instructions):
        """Create and deploy HTML/CSS/JS project."""
        folder_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_path = os.path.join(self.base_dir, folder_name)
        os.makedirs(project_path, exist_ok=True)

        # Generate code
        response = self.run_assistant(instructions + " Make sure it has all HTML, CSS, and JavaScript code embedded within the file itself.")
        html_content = self.format_html_input(response)
        
        # Save and deploy
        file_path = os.path.join(project_path, 'index.html')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        print(f"Created project at: {project_path}")
        os.chdir(project_path)
        subprocess.run("npx vercel", shell=True, check=True)

    def create_react_project(self, instructions):
        """Create and deploy React project."""
        project_path = os.path.join(self.base_dir, self.project_name)
        os.makedirs(project_path, exist_ok=True)
        os.chdir(project_path)

        # Initialize React project
        subprocess.run("npm init vite@latest my-react-app -- --template react", shell=True, check=True)
        os.chdir("my-react-app")
        subprocess.run("npm install", shell=True, check=True)
        subprocess.run("npm install react-router-dom", shell=True, check=True)

        # Generate code
        enhanced_instructions = (
            f"{instructions} Make sure it follows React + Vite format. "
            f"Complete within App.jsx and App.css only. "
            f"Project name: {self.project_name}. "
            "Make desktop view with 100vh and 100vw."
        )
        response = self.run_assistant(enhanced_instructions)
        
        # Save files
        self.separate_sections(
            response,
            os.path.join('src', 'App.jsx'),
            os.path.join('src', 'App.css')
        )
        
        # Deploy
        subprocess.run("npx vercel", shell=True, check=True)

