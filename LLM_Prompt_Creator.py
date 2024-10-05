################################################################
# PROGRAM NAME : LLM_Prompt_Creator.py
# DESCRIPTION : A Flask web application for generating prompts for LLMs based on user inputs.
#
# AUTHOR : ChatGPT Assistant
# CREATION DATE : 2023-10-05
# LAST CHANGE DATE : 2024-04-28
# REVIEWER : N/A
# REVIEW DATE : N/A
#
# INPUT : User selections and inputs from the web interface.
#
# OUTPUT : Generated prompt displayed on the web page and optionally saved as a text file.
#
# SUMMARY : This program creates a web interface using Flask where users can select task types,
# roles, contexts, and other parameters to generate a customized prompt for an LLM.
# It uses hard-coded dictionaries to map user selections to text blocks and concatenates
# them with user-provided inputs to create the final prompt.
#
# USER MANUAL :
# --------------
# **Overview:**
# LLM_Prompt_Creator is a Flask-based web application that allows users to generate customized prompts
# for Large Language Models (LLMs) such as ChatGPT or Copilot. Users can select various parameters
# and input specific details to craft prompts tailored to their needs.
#
# **Setup Instructions:**
# 1. **Prerequisites:**
#    - Ensure you have Python 3.6 or higher installed on your system.
#    - Install the required Python packages using pip:
#      ```
#      pip install flask
#      ```
#
# 2. **Download the Script:**
#    - Save the `LLM_Prompt_Creator.py` script to your desired directory.
#
# 3. **Running the Application:**
#    - Navigate to the directory containing the script using your terminal or command prompt.
#    - Execute the script by running:
#      ```
#      python LLM_Prompt_Creator.py
#      ```
#    - The application will start a local web server, typically accessible at `http://127.0.0.1:5000/`.
#
# **Using the Application:**
# 1. **Access the Web Interface:**
#    - Open a web browser (e.g., Chrome, Firefox, Edge).
#    - Navigate to `http://127.0.0.1:5000/` to access the Prompt Creator interface.
#
# 2. **Generate a Prompt:**
#    - **Select Task Type:** Choose the type of task you want the LLM to perform from the drop-down menu (e.g., Python Programming, Writing a Business Email).
#    - **Select Role:** Choose the role you want the LLM to assume (e.g., Python Code Assistant, Project Manager).
#    - **Select Context:** Choose a predefined context from the drop-down menu or enter a custom context in the provided text field.
#    - **Describe the Task:** Provide a detailed description of the task you want the LLM to perform in the textarea.
#    - **Expected Output:** Specify the expected type, shape, style, and formality of the LLM's response in the textarea.
#    - **Select Language:** Choose the language (English or German) in which you want the LLM's response.
#    - **Create Prompt:** Click the "Create Prompt" button to generate and display the prompt on the webpage.
#
# 3. **Save the Prompt:**
#    - After generating the prompt, you can download it as a `.txt` file by clicking the "Save Prompt" button.
#
# **Troubleshooting:**
# - **Port Conflicts:** If `http://127.0.0.1:5000/` is not accessible, ensure that port `5000` is not being used by another application. You can change the port by modifying the `app.run()` line at the end of the script:
#   ```python
#   app.run(debug=True, port=YOUR_DESIRED_PORT)
#   ```
# - **Missing Dependencies:** Ensure that Flask is installed. If you encounter import errors, reinstall Flask using:
#   ```
#   pip install --upgrade flask
#   ```
#
# **Extending the Application:**
# - **Adding More Options:** You can expand the `get_task_types()`, `get_roles()`, and `get_contexts()` functions to include more options as needed.
# - **Enhancing the UI:** Integrate CSS frameworks like Bootstrap to improve the visual appearance of the web interface.
# - **Database Integration:** Implement database functionality to store generated prompts for future reference.
#
# REVIEW SUMMARY : N/A
#
################################################################
# CHANGE TRACKER
# DATE			AUTHOR				DESCRIPTION
# 2023-10-05	ChatGPT Assistant	Initial creation of the LLM_Prompt_Creator prototype.
# 2024-04-27	ChatGPT Assistant	Updated send_file parameter to 'download_name' to fix TypeError.
# 2024-04-28	ChatGPT Assistant	Refactored roles to be task-specific to ensure relevance.
#
################################################################

from flask import Flask, render_template_string, request, send_file
from typing import Dict, Any
import datetime
import io

app = Flask(__name__)

def get_task_types() -> Dict[str, str]:
    """
    Returns a dictionary of task types.

    Returns:
        Dict[str, str]: A dictionary mapping task keys to task descriptions.
    """
    return {
        'python_programming': 'Python Programming',
        'sas_programming': 'SAS Programming',
        'business_email': 'Writing a Business Email',
        'report_review': 'Reviewing a Report'
    }

def get_roles(task_type: str = None) -> Dict[str, str]:
    """
    Returns a dictionary of roles based on the task type.

    Args:
        task_type (str, optional): The selected task type. Defaults to None.

    Returns:
        Dict[str, str]: A dictionary mapping role keys to role descriptions.
    """
    roles_mapping = {
        'python_programming': {
            'python_code_assistant': 'Python Code Assistant',
            'python_debugger': 'Python Debugger',
            'python_code_reviewer': 'Python Code Reviewer',
            'python_documentation_writer': 'Python Documentation Writer',
            'python_learning_tutor': 'Python Learning Tutor',
            'python_data_analyst': 'Python Data Analyst',
            'python_web_developer': 'Python Web Developer',
            'python_automation_specialist': 'Python Automation Specialist',
            'python_testing_engineer': 'Python Testing Engineer',
            'python_devops_engineer': 'Python DevOps Engineer',
            'python_ai_ml_engineer': 'Python AI/ML Engineer',
            'python_security_auditor': 'Python Security Auditor',
            'python_performance_optimizer': 'Python Performance Optimizer',
            'python_api_developer': 'Python API Developer',
            'python_database_administrator': 'Python Database Administrator'
        },
        'sas_programming': {
            'sas_code_assistant': 'SAS Code Assistant',
            'sas_debugger': 'SAS Debugger',
            'sas_code_reviewer': 'SAS Code Reviewer',
            'sas_documentation_writer': 'SAS Documentation Writer',
            'sas_learning_tutor': 'SAS Learning Tutor',
            'sas_data_analyst': 'SAS Data Analyst',
            'sas_web_developer': 'SAS Web Developer',
            'sas_automation_specialist': 'SAS Automation Specialist',
            'sas_testing_engineer': 'SAS Testing Engineer',
            'sas_devops_engineer': 'SAS DevOps Engineer',
            'sas_ai_ml_engineer': 'SAS AI/ML Engineer',
            'sas_security_auditor': 'SAS Security Auditor',
            'sas_performance_optimizer': 'SAS Performance Optimizer',
            'sas_api_developer': 'SAS API Developer',
            'sas_database_administrator': 'SAS Database Administrator'
        },
        'business_email': {
            'email_writer': 'Email Writer',
            'communication_coordinator': 'Communication Coordinator',
            'project_manager': 'Project Manager',
            'client_relations_specialist': 'Client Relations Specialist'
        },
        'report_review': {
            'report_reviewer': 'Report Reviewer',
            'quality_assurance_specialist': 'Quality Assurance Specialist',
            'content_editor': 'Content Editor',
            'compliance_officer': 'Compliance Officer'
        }
    }

    return roles_mapping.get(task_type, {})

def get_contexts() -> Dict[str, str]:
    """
    Returns a dictionary of contexts.

    Returns:
        Dict[str, str]: A dictionary mapping context keys to context descriptions.
    """
    return {
        'credit_risk_modelling': 'Credit Risk Modelling',
        'moving_house': 'Moving the House',
        'data_analysis': 'Data Analysis',
        'software_development': 'Software Development'
    }

def generate_prompt(data: Dict[str, Any]) -> str:
    """
    Generates the final prompt by concatenating text blocks and user inputs.

    Args:
        data (Dict[str, Any]): A dictionary containing user selections and inputs.

    Returns:
        str: The generated prompt.
    """
    task_types = get_task_types()
    roles = get_roles(data.get('task_type'))
    contexts = get_contexts()

    role_description = roles.get(data.get('role'), 'Role')

    prompt = f"You are a {role_description} specializing in {task_types.get(data.get('task_type'), 'the specified task')}.\n"
    context = data.get('context_custom') or contexts.get(data.get('context'), '')
    if context:
        prompt += f"Context: {context}\n"
    task_description = data.get('task_description', 'Provide details about the task.')
    prompt += f"Task: {task_description}\n"
    expected_output = data.get('expected_output', 'Provide details about the expected output.')
    prompt += f"Expected Output: {expected_output}\n"
    language = data.get('language', 'English')
    prompt += f"Please provide the response in {language}."
    return prompt

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Renders the main page and handles form submissions.

    Returns:
        str: Rendered HTML template or file download response.
    """
    task_types = get_task_types()
    contexts = get_contexts()
    prompt = ''
    roles = {}

    if request.method == 'POST':
        data = request.form.to_dict()
        selected_task_type = data.get('task_type')
        roles = get_roles(selected_task_type)

        if 'create_prompt' in request.form:
            # Ensure that a role is selected before generating the prompt
            if 'role' in data and data['role']:
                prompt = generate_prompt(data)
            else:
                prompt = "Please select a valid role to generate the prompt."
        elif 'save_prompt' in request.form:
            # Retrieve the prompt from the hidden field
            prompt = data.get('prompt', '')
            if prompt and not prompt.startswith("Please select a valid role"):
                return generate_prompt_file(prompt)
            else:
                prompt = "No prompt available to save. Please generate a prompt first."

    return render_template_string(TEMPLATE, task_types=task_types, roles=roles,
                                  contexts=contexts, prompt=prompt)

def generate_prompt_file(prompt: str):
    """
    Generates a text file from the prompt for the user to download.

    Args:
        prompt (str): The generated prompt.

    Returns:
        Response: Flask response to send the file.
    """
    buffer = io.BytesIO()
    buffer.write(prompt.encode('utf-8'))
    buffer.seek(0)
    filename = f"prompt_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='text/plain')

# HTML Template as a multi-line string
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Prompt Creator</title>
</head>
<body>
    <h1>Prompt Creator</h1>
    <form method="post">
        <label for="task_type">Select Task Type:</label>
        <select name="task_type" id="task_type" onchange="this.form.submit()">
            <option value="">--Select Task Type--</option>
            {% for key, value in task_types.items() %}
            <option value="{{ key }}" {% if request.form.get('task_type') == key %}selected{% endif %}>{{ value }}</option>
            {% endfor %}
        </select><br><br>

        {% if roles %}
        <label for="role">Select Role:</label>
        <select name="role" id="role">
            <option value="">--Select Role--</option>
            {% for key, value in roles.items() %}
            <option value="{{ key }}">{{ value }}</option>
            {% endfor %}
        </select><br><br>
        {% endif %}

        <label for="context">Select Context:</label>
        <select name="context" id="context">
            <option value="">--None--</option>
            {% for key, value in contexts.items() %}
            <option value="{{ key }}">{{ value }}</option>
            {% endfor %}
        </select><br><br>

        <label for="context_custom">Or Enter Custom Context:</label>
        <input type="text" id="context_custom" name="context_custom"><br><br>

        <label for="task_description">Describe the Task:</label><br>
        <textarea id="task_description" name="task_description" rows="4" cols="50"></textarea><br><br>

        <label for="expected_output">Expected Output:</label><br>
        <textarea id="expected_output" name="expected_output" rows="4" cols="50"></textarea><br><br>

        <label for="language">Select Language:</label>
        <select name="language" id="language">
            <option value="English">English</option>
            <option value="German">German</option>
        </select><br><br>

        {% if roles %}
        <!-- Hidden field to store the generated prompt -->
        {% if prompt and not prompt.startswith("Please select a valid role") %}
        <input type="hidden" name="prompt" value="{{ prompt | e }}">
        {% endif %}

        <button type="submit" name="create_prompt">Create Prompt</button>
        <button type="submit" name="save_prompt">Save Prompt</button>
        {% endif %}
    </form>

    {% if prompt %}
    <h2>Generated Prompt:</h2>
    <pre>{{ prompt }}</pre>
    {% endif %}
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
