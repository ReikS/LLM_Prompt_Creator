"""
PROGRAM NAME    : LLM_Prompt_Creator.py
DESCRIPTION     : A Flask web application for generating prompts for LLMs 
                  based on user inputs.

AUTHOR          : ReikS
CREATION DATE   : 2024-04-29
LAST CHANGE     : 2024-04-30

INPUT           : User selections (task type, role, context, etc.) via a web form.
OUTPUT          : Generated prompt displayed on the web page and optionally 
                  saved as a text file. Web server runs on http://127.0.0.1:5000

SUMMARY         : This script creates a web interface using Flask where users 
                  can select context, task types, roles, and other parameters 
                  to generate a customized prompt for an LLM. 
                  Internally, the task dictionary stores detailed descriptions, 
                  while only short capitalized task names (keys) appear in the UI.
                  The output prompt is formatted with line breaks and wrapped 
                  text for readability.
"""


from flask import Flask, render_template_string, request, send_file
from typing import Dict, Any
import datetime
import io

app = Flask(__name__)

def get_task_types() -> Dict[str, str]:
    """
    Return a dictionary of task keys to their detailed descriptions.

    In the UI, only the capitalized key is displayed (e.g., "python_programming"
    becomes "Python Programming"), thus avoiding cluttering the interface with 
    long descriptive text. However, the full descriptive text remains accessible 
    internally for reference or further logic as needed.

    Returns:
        Dict[str, str]: A dictionary where each key is a unique identifier
        (e.g., 'python_programming') and each value is a long, descriptive
        string about the nature and standards of that task.
    """
    return {
        'python_programming': (
            'Python Programming involves writing clean, readable, and efficient code by adhering to PEP 8 style guidelines. '
            'Professional Python programmers utilize meaningful variable and function names, maintain consistent indentation, '
            'and organize code into modular and reusable components. Each script begins with a comprehensive program header that includes '
            'metadata such as the program name, description, author, creation date, and a change tracker. Docstrings are employed for all functions '
            'and classes to provide clear explanations of their purpose, parameters, and return values. Inline comments are used judiciously '
            'to elucidate complex logic or important decisions within the code. Additionally, Python programmers implement robust error handling '
            'and write comprehensive unit and integration tests to ensure code reliability and facilitate maintenance. '
            'Version control systems like Git are utilized for effective code management and collaboration. Adhering to these practices '
            'ensures that Python codebases are maintainable, scalable, and of high quality.'
        ),
        'sas_programming': (
            'SAS Programming entails developing and managing data analysis scripts using SAS software, focusing on data manipulation, '
            'statistical analysis, reporting, and visualization. Professional SAS programmers adhere to coding standards that promote clarity '
            'and efficiency. Each SAS script starts with a detailed program header containing essential information such as the script name, '
            'purpose, author, creation date, and a change tracker for version history. Docstrings are incorporated within macros and data steps '
            'to explain their functionality, input parameters, and expected outcomes. Inline comments are strategically placed to clarify '
            'complex data transformations or analytical procedures. Robust error handling mechanisms are implemented to manage data inconsistencies '
            'and runtime issues gracefully. SAS programmers also develop comprehensive test cases for macros, functions, and data procedures '
            'to validate their correctness and performance. Utilizing version control systems ensures organized code management and facilitates '
            'collaboration among team members. These best practices in SAS programming contribute to the creation of reliable, efficient, '
            'and maintainable data analysis solutions.'
        ),
        'business_email': (
            'Writing a Business Email requires composing clear, concise, and professional messages tailored to the intended audience. '
            'Each email begins with a polite salutation and clearly states the purpose of the communication in the opening lines. '
            'Professional email writers structure their messages logically, using short paragraphs and bullet points where appropriate '
            'to enhance readability. They maintain a formal tone, ensure proper grammar and punctuation, and avoid jargon unless it is '
            'industry-specific and understood by the recipient. Each email concludes with a courteous closing and appropriate sign-off. '
            'Additionally, email writers adhere to organizational guidelines regarding formatting, confidentiality, and compliance with '
            'communication policies. Attention to detail is paramount to ensure that all necessary information is included and that the '
            'email effectively achieves its intended purpose.'
        ),
        'report_review': (
            'Reviewing a Report involves critically evaluating the content, structure, and presentation of a document to ensure accuracy, '
            'clarity, and completeness. Professional report reviewers begin by assessing the overall organization and logical flow of the report, '
            'ensuring that each section transitions smoothly and that the arguments are well-supported by evidence. They verify the accuracy '
            'and relevance of the data and analysis presented, checking for consistency and reliability. Reviewers also evaluate the clarity '
            'of writing, ensuring that technical terms are explained and that the report is accessible to its intended audience. '
            'Attention is paid to formatting, including headings, tables, figures, and citations, to ensure adherence to organizational '
            'or publication standards. Constructive feedback is provided to address areas such as improving argument strength, enhancing data '
            'visualization, and refining language for greater impact. By applying these comprehensive review practices, report reviewers '
            'contribute to the production of high-quality, effective, and professional reports.'
        )
    }

def get_contexts() -> Dict[str, str]:
    """
    Returns a dictionary of contexts with detailed descriptions.

    Each context entry includes:
      - Key responsibilities or focuses
      - Methods or processes typically used
      - Deliverables or usual output to stakeholders
      - Working standards or best practices

    In the user interface, only the capitalized key is displayed (e.g., "credit_risk_modelling"
    → "Credit Risk Modelling"). The lengthy description remains internal for reference or
    further logic.

    Returns:
        Dict[str, str]: A dictionary mapping context keys to comprehensive descriptions.
    """
    return {
        'credit_risk_modelling': (
            'Credit Risk Modelling:\n'
            'Responsibilities: Evaluate the probability of default (PD) and loss given default (LGD) for '
            'loans and credit portfolios. Conduct thorough data gathering, cleaning, and analysis.\n\n'
            'Methods: Utilize statistical models (e.g., logistic regression, decision trees) and advanced '
            'techniques like machine learning for predictive analysis. Employ stress testing and scenario '
            'analysis to assess portfolio resilience under different economic conditions.\n\n'
            'Deliverables: Risk reports with model outputs (PD, EAD, LGD), validation documentation, and '
            'compliance materials aligned with regulations (e.g., Basel III). Summaries for senior '
            'management, detailing key risk indicators and recommended actions.\n\n'
            'Working Standards and Best Practices: Maintain robust data governance, model validation '
            'procedures, and transparent documentation. Collaborate closely with risk committees to ensure '
            'models reflect current regulations and organizational risk appetite. Adhere to strict '
            'version control and testing protocols to maintain model integrity.'
        ),
        'moving_house': (
            'Moving House:\n'
            'Responsibilities: Oversee planning, organization, and execution of relocating belongings '
            'from one residence to another. Coordinate between moving services, utility providers, and '
            'family or housemates.\n\n'
            'Methods: Develop a detailed timeline and budget. Use inventory checklists, packing strategies '
            '(e.g., labeling boxes, categorizing items), and scheduling tools to streamline the move.\n\n'
            'Deliverables: A structured moving plan (including timeline, cost estimates, and contact '
            'details), labeled boxes and furniture for easy unpacking, and a post-move checklist '
            '(address changes, utility transfers, etc.).\n\n'
            'Working Standards and Best Practices: Maintain open communication with all parties involved, '
            'use reliable moving services, secure fragile items properly, and ensure timely updates on '
            'any schedule changes. Conduct a final walkthrough to verify no items are left behind.'
        ),
        'data_analysis': (
            'Data Analysis:\n'
            'Responsibilities: Collect, process, and examine datasets to derive actionable insights '
            'and support data-driven decisions.\n\n'
            'Methods: Employ data cleaning, feature engineering, statistical methods (e.g., hypothesis '
            'testing, regression), and data visualization tools (e.g., matplotlib, seaborn). Develop '
            'reproducible workflows for transparency.\n\n'
            'Deliverables: Analytical reports highlighting key findings, visual dashboards or charts '
            '(e.g., via Tableau or Power BI), and recommendations on trends or anomalies. Documentation '
            'of the analysis process and any code or scripts used.\n\n'
            'Working Standards and Best Practices: Adhere to data privacy regulations (e.g., GDPR), '
            'version-control analysis scripts, and ensure validity through peer review or QA checks. '
            'Explain assumptions and limitations of the analysis to stakeholders.'
        ),
        'software_development': (
            'Software Development:\n'
            'Responsibilities: Design, implement, and maintain software applications, working with '
            'stakeholders to clarify requirements and integrate features.\n\n'
            'Methods: Follow a software development lifecycle (SDLC) model such as Agile or Waterfall. '
            'Use continuous integration/continuous delivery (CI/CD), version control (Git), and code '
            'reviews. Test-driven development (TDD) or behavior-driven development (BDD) is often used '
            'to ensure reliability.\n\n'
            'Deliverables: Functional software modules or applications, technical documentation, unit and '
            'integration test results, and deployment packages or containers (e.g., Docker images).\n\n'
            'Working Standards and Best Practices: Maintain clean architecture, enforce consistent code '
            'style (e.g., PEP 8 for Python), document APIs or libraries thoroughly, and plan regular '
            'refactoring. Employ robust QA processes, including automated testing and peer reviews, to '
            'ensure code quality and maintainability.'
        )
    }


def get_roles(task_type: str = None) -> Dict[str, str]:
    """
    Returns a dictionary of roles, with each role key mapped to a descriptive string.
    Each role entry includes:
      - Key responsibilities or focuses
      - Methods or typical approaches
      - Deliverables or usual output
      - Working standards or best practices

    The dictionary returned is specific to a given task_type. In the user interface,
    only the capitalized key (e.g., "python_code_assistant" → "Python Code Assistant")
    is displayed, while the detailed text is retained internally for reference.

    Args:
        task_type (str, optional): The selected task type (e.g., 'python_programming',
                                   'sas_programming', etc.). Defaults to None.

    Returns:
        Dict[str, str]: A dictionary mapping role keys to descriptive text.
    """
    # Python Programming Roles
    python_roles = {
        'python_code_assistant': (
            'Python Code Assistant:\n'
            'Responsibilities: Provide guidance on Python code structure, readability, and '
            'maintainability. Suggest best practices and design patterns.\n\n'
            'Methods: Review code snippets, propose refactorings, and demonstrate sample implementations. '
            'Highlight library or framework choices.\n\n'
            'Deliverables: Annotated code reviews, example scripts demonstrating proposed solutions, '
            'updated code repositories incorporating improvements.\n\n'
            'Working Standards and Best Practices: Follow PEP 8, ensure inline comments explain '
            'non-obvious logic, maintain a robust test suite, and use version control for tracking changes.'
        ),
        'python_debugger': (
            'Python Debugger:\n'
            'Responsibilities: Identify and resolve bugs or unexpected behavior in Python code.\n\n'
            'Methods: Use tools like pdb or IDE-based debuggers, set breakpoints, inspect variables, '
            'and analyze stack traces. Employ systematic isolation to pinpoint root causes.\n\n'
            'Deliverables: Debugged and tested code that resolves the identified issues. '
            'A brief diagnostic report or summary describing the issue and fix.\n\n'
            'Working Standards and Best Practices: Maintain logs of debugging sessions, document '
            'root causes, and update tests to prevent regressions.'
        ),
        'python_code_reviewer': (
            'Python Code Reviewer:\n'
            'Responsibilities: Evaluate Python code for correctness, performance, style compliance, '
            'and overall quality.\n\n'
            'Methods: Conduct line-by-line reviews, examine code structure, and validate adherence '
            'to coding standards (e.g., PEP 8). Check for redundant logic, potential security gaps, '
            'and unclear documentation.\n\n'
            'Deliverables: Structured review feedback, Git pull request comments, suggested revisions, '
            'and acceptance criteria for refactoring.\n\n'
            'Working Standards and Best Practices: Emphasize clarity, maintainability, and proper '
            'testing. Encourage docstrings on all classes/functions and use of continuous integration '
            'for quality checks.'
        ),
        'python_documentation_writer': (
            'Python Documentation Writer:\n'
            'Responsibilities: Craft and maintain technical documentation for Python modules, '
            'classes, and functions.\n\n'
            'Methods: Write docstrings following reStructuredText or Google style, produce user '
            'guides (e.g., Sphinx docs), and consolidate knowledge into wiki or README files.\n\n'
            'Deliverables: Complete docstring coverage, structured user manuals, or knowledge base '
            'articles. Clear guidelines on installation, usage examples, and troubleshooting steps.\n\n'
            'Working Standards and Best Practices: Maintain consistent style and formatting across '
            'all docs, ensure version alignment between code and documentation, and collect user feedback '
            'for continuous improvement.'
        ),
        'python_learning_tutor': (
            'Python Learning Tutor:\n'
            'Responsibilities: Instruct newcomers on Python syntax, data structures, control flow, '
            'and fundamental libraries.\n\n'
            'Methods: Provide hands-on coding examples, exercises, quizzes, and real-world mini-projects '
            'to solidify learning.\n\n'
            'Deliverables: Lesson plans, coding challenge sets, progress reports, and customized feedback '
            'to help learners advance.\n\n'
            'Working Standards and Best Practices: Adapt teaching materials to varied skill levels, '
            'promote best coding practices (PEP 8, docstrings), and encourage active learning through '
            'problem-solving.'
        ),
        'python_data_analyst': (
            'Python Data Analyst:\n'
            'Responsibilities: Manipulate, clean, and analyze data using Python libraries (pandas, '
            'NumPy, matplotlib, etc.). Generate insights and data visualizations.\n\n'
            'Methods: Implement feature engineering, statistical analysis, and exploratory data analysis. '
            'Build notebooks or scripts for reproducible workflows.\n\n'
            'Deliverables: Visual charts, summary reports or dashboards, and recommendations to '
            'business stakeholders.\n\n'
            'Working Standards and Best Practices: Document assumptions, use version control for '
            'analysis scripts, ensure results are reproducible, and respect data governance policies.'
        ),
        'python_web_developer': (
            'Python Web Developer:\n'
            'Responsibilities: Design and implement server-side logic using frameworks like Django '
            'or Flask. Integrate databases, optimize performance, and manage session state.\n\n'
            'Methods: Employ REST or GraphQL APIs, configure deployment (e.g., Docker, AWS), and '
            'use templates or front-end integrations.\n\n'
            'Deliverables: Functional web applications or microservices, database schemas, automated '
            'test suites, and deployment pipelines.\n\n'
            'Working Standards and Best Practices: Enforce code reviews, store secrets securely, '
            'follow security best practices (e.g., XSS/CSRF protection), and maintain scalability.'
        ),
        'python_automation_specialist': (
            'Python Automation Specialist:\n'
            'Responsibilities: Develop scripts and workflows to automate repetitive tasks or '
            'pipeline processes.\n\n'
            'Methods: Create scheduled jobs (e.g., cron, Airflow), integrate APIs, and leverage '
            'Python libraries for file manipulation or data scraping.\n\n'
            'Deliverables: Automated scripts or pipelines, log files documenting process outcomes, '
            'and error-handling procedures.\n\n'
            'Working Standards and Best Practices: Include detailed logs, robust exception handling, '
            'and fallback mechanisms for reliability. Maintain versioned scripts with minimal '
            'hard-coded dependencies.'
        ),
        'python_testing_engineer': (
            'Python Testing Engineer:\n'
            'Responsibilities: Write and maintain unit, integration, and system tests for Python '
            'applications.\n\n'
            'Methods: Use frameworks like pytest or unittest, set up continuous integration, and '
            'analyze coverage reports.\n\n'
            'Deliverables: Comprehensive test suites, documentation on how to run tests, and bug '
            'reports with reproducible steps.\n\n'
            'Working Standards and Best Practices: Ensure tests are deterministic, isolate external '
            'dependencies, use mock libraries when needed, and promote a culture of test-driven '
            'development.'
        ),
        'python_devops_engineer': (
            'Python DevOps Engineer:\n'
            'Responsibilities: Integrate Python-based solutions into CI/CD pipelines, orchestrate '
            'infrastructure (e.g., Kubernetes), and manage deployment.\n\n'
            'Methods: Build Docker images, configure Jenkins/GitLab CI, and monitor services via '
            'tools like Prometheus/Grafana.\n\n'
            'Deliverables: Automated deployment scripts, infrastructure-as-code templates, and '
            'operational runbooks.\n\n'
            'Working Standards and Best Practices: Enforce consistent environment configurations, '
            'lock down secrets (e.g., Vault), track build artifacts, and implement rolling or '
            'blue-green deployments.'
        ),
        'python_ai_ml_engineer': (
            'Python AI/ML Engineer:\n'
            'Responsibilities: Design, implement, and maintain machine learning models using libraries '
            'like scikit-learn, TensorFlow, or PyTorch.\n\n'
            'Methods: Perform data preprocessing, feature engineering, hyperparameter tuning, and '
            'model validation. Deploy models via REST APIs or model-serving frameworks.\n\n'
            'Deliverables: Trained model artifacts, performance metrics (e.g., F1-score, accuracy), '
            'and deployment pipelines.\n\n'
            'Working Standards and Best Practices: Document model assumptions, track experiments '
            '(MLOps), ensure data ethics and privacy, and regularly retrain or validate models '
            'to account for data drift.'
        ),
        'python_security_auditor': (
            'Python Security Auditor:\n'
            'Responsibilities: Inspect Python applications for vulnerabilities, ensure code '
            'complies with security standards, and advise on secure design.\n\n'
            'Methods: Conduct penetration tests, review dependencies (e.g., check CVE databases), '
            'and apply secure coding guidelines.\n\n'
            'Deliverables: Security audit reports, patch recommendations, and updated code to '
            'address discovered issues.\n\n'
            'Working Standards and Best Practices: Maintain confidentiality of sensitive data, '
            'use trusted libraries, enforce SSL/TLS, and keep dependencies up to date.'
        ),
        'python_performance_optimizer': (
            'Python Performance Optimizer:\n'
            'Responsibilities: Identify bottlenecks in Python code and recommend strategies '
            'to reduce latency and resource usage.\n\n'
            'Methods: Profile applications (cProfile, line_profiler), optimize algorithms, use '
            'async or multiprocessing where applicable, and introduce caching.\n\n'
            'Deliverables: Reworked code or functions demonstrating speed gains, performance '
            'metrics (before/after comparisons), and documentation of changes.\n\n'
            'Working Standards and Best Practices: Keep track of baseline measurements, preserve '
            'code readability, and ensure backward compatibility while optimizing.'
        ),
        'python_api_developer': (
            'Python API Developer:\n'
            'Responsibilities: Create RESTful or GraphQL endpoints in Python to facilitate '
            'communication with client applications.\n\n'
            'Methods: Use frameworks like FastAPI, Flask, or Django REST, define data schemas '
            'and error handling, and integrate authentication/authorization.\n\n'
            'Deliverables: API endpoints (with versioning), usage documentation (Swagger/OpenAPI), '
            'and test coverage for endpoints.\n\n'
            'Working Standards and Best Practices: Enforce consistent request/response formats, '
            'log all critical events, handle edge cases gracefully, and monitor API performance.'
        ),
        'python_database_administrator': (
            'Python Database Administrator:\n'
            'Responsibilities: Manage database schemas, queries, and connections within '
            'Python-driven applications.\n\n'
            'Methods: Implement ORMs (SQLAlchemy, Django ORM), index optimization, migrations, '
            'and data recovery plans.\n\n'
            'Deliverables: Properly normalized database schemas, migration scripts, performance '
            'reports (e.g., slow query logs), and backup strategies.\n\n'
            'Working Standards and Best Practices: Maintain consistent naming conventions, '
            'use parameterized queries to prevent SQL injection, regularly test backups, '
            'and keep schema documentation updated.'
        )
    }

    # SAS Programming Roles
    sas_roles = {
        'sas_code_assistant': (
            'SAS Code Assistant:\n'
            'Responsibilities: Guide and refine SAS scripts focused on data manipulation and '
            'analysis. Improve readability, efficiency, and consistency.\n\n'
            'Methods: Suggest macro usage, optimize DATA steps, review PROC setups, and incorporate '
            'performance tips such as indexing.\n\n'
            'Deliverables: Annotated scripts, recommended macro templates, and a short improvement '
            'report describing changes.\n\n'
            'Working Standards and Best Practices: Use version control for SAS programs, maintain '
            'standardized naming conventions for data sets and variables, and create test logs '
            'for reproducibility.'
        ),
        'sas_debugger': (
            'SAS Debugger:\n'
            'Responsibilities: Locate and fix issues or anomalies in SAS logs and outputs. '
            'Identify root causes behind data or procedural errors.\n\n'
            'Methods: Analyze SAS logs for warnings/errors, isolate suspect code blocks, and '
            'test alternative logic or parameter settings.\n\n'
            'Deliverables: Debugged SAS programs, a brief incident report documenting the discovered '
            'issue, and recommended preventive measures.\n\n'
            'Working Standards and Best Practices: Keep track of code changes in version control, '
            'annotate logs, and share debugging insights with team members.'
        ),
        'sas_code_reviewer': (
            'SAS Code Reviewer:\n'
            'Responsibilities: Assess scripts for logical accuracy, performance, and adherence to '
            'organizing principles or coding guidelines.\n\n'
            'Methods: Perform line-by-line reviews, watch for inefficient merges/joins, ensure '
            'documentation (comments, headers) is consistent.\n\n'
            'Deliverables: Structured feedback, annotated pull requests (if applicable), and a '
            'refactoring backlog for potential optimizations.\n\n'
            'Working Standards and Best Practices: Emphasize data integrity, maintain consistent '
            'macro structures, and enforce robust logging of errors.'
        ),
        'sas_documentation_writer': (
            'SAS Documentation Writer:\n'
            'Responsibilities: Create comprehensive documentation for SAS processes, macros, and '
            'data flows.\n\n'
            'Methods: Maintain docstrings or comments within SAS programs, produce user guides in '
            'formats like HTML/PDF, and ensure traceability of macros.\n\n'
            'Deliverables: Updated repository or wiki pages, documented workflows with flowcharts, '
            'and versioned PDF/HTML manuals.\n\n'
            'Working Standards and Best Practices: Keep documentation in sync with code revisions, '
            'use clear naming conventions, and verify accuracy of all code references.'
        ),
        'sas_learning_tutor': (
            'SAS Learning Tutor:\n'
            'Responsibilities: Educate team members or students in SAS fundamentals like DATA steps, '
            'PROCs, macros, and reporting.\n\n'
            'Methods: Conduct interactive sessions, assign hands-on projects, and evaluate '
            'understanding via quizzes or exercises.\n\n'
            'Deliverables: Curriculum outlines, guided exercises, feedback reports, and skill '
            'assessment metrics.\n\n'
            'Working Standards and Best Practices: Encourage best practices (modular macros, '
            'sufficient commenting), show real-world data examples, and stress the importance '
            'of thorough log checks.'
        ),
        'sas_data_analyst': (
            'SAS Data Analyst:\n'
            'Responsibilities: Perform statistical analysis, data exploration, and visualization '
            'using SAS procedures.\n\n'
            'Methods: Use PROCs like PROC SQL, PROC MEANS, PROC FREQ, or PROC REPORT to transform '
            'and summarize data.\n\n'
            'Deliverables: Charts, tables, summary reports, and interpretative commentary '
            'for stakeholders.\n\n'
            'Working Standards and Best Practices: Validate data quality, track transformations, '
            'and thoroughly document each step for reproducibility. Respect data privacy and '
            'compliance regulations.'
        ),
        'sas_web_developer': (
            'SAS Web Developer:\n'
            'Responsibilities: Integrate SAS analytics or reporting into web applications or '
            'interfaces.\n\n'
            'Methods: Develop stored processes, use SAS BI services, and configure secure '
            'connections for real-time data retrieval.\n\n'
            'Deliverables: Deployed web applications or portals, user guides, and testing logs '
            'validating data accuracy.\n\n'
            'Working Standards and Best Practices: Follow security protocols (TLS/SSL), maintain '
            'robust session handling, and keep track of user access privileges.'
        ),
        'sas_automation_specialist': (
            'SAS Automation Specialist:\n'
            'Responsibilities: Design and implement automated workflows for recurring data '
            'analysis or reporting tasks.\n\n'
            'Methods: Schedule jobs using SAS Management Console or scheduling tools (Windows Task '
            'Scheduler, cron), leverage macros for repeatable code.\n\n'
            'Deliverables: Automated job scripts, run logs, and any error-handling routines '
            'to manage failures.\n\n'
            'Working Standards and Best Practices: Ensure consistent logging, handle edge cases '
            'gracefully, and keep a test environment for major macro changes.'
        ),
        'sas_testing_engineer': (
            'SAS Testing Engineer:\n'
            'Responsibilities: Develop and maintain test suites for SAS programs to ensure data '
            'integrity and script reliability.\n\n'
            'Methods: Write test scripts, compare expected vs. actual output, and incorporate '
            'tests in continuous integration if available.\n\n'
            'Deliverables: Documented test cases, test result logs, and bug reports pinpointing '
            'inconsistencies.\n\n'
            'Working Standards and Best Practices: Use standardized test data, separate test and '
            'production environments, and automate regression checks where possible.'
        ),
        'sas_devops_engineer': (
            'SAS DevOps Engineer:\n'
            'Responsibilities: Automate deployment and manage SAS environments, linking them '
            'to CI/CD pipelines.\n\n'
            'Methods: Employ infrastructure-as-code (e.g., Ansible, Terraform) to provision SAS '
            'servers, define deployment scripts, and monitor performance.\n\n'
            'Deliverables: Automated build/deploy pipelines, environment configuration docs, '
            'and performance dashboards.\n\n'
            'Working Standards and Best Practices: Keep environment configurations versioned, '
            'apply security patches promptly, and test all changes in staging before production.'
        ),
        'sas_ai_ml_engineer': (
            'SAS AI/ML Engineer:\n'
            'Responsibilities: Build and deploy machine learning models within SAS environments, '
            'handling data preparation, training, and validation.\n\n'
            'Methods: Use PROCs (e.g., PROC HPFOREST, PROC LOGISTIC), experiment tracking, and '
            'model management within SAS. Compare model performance metrics.\n\n'
            'Deliverables: Production-ready models, scoring code or APIs, and performance reports '
            'documenting false positives, precision, or recall, etc.\n\n'
            'Working Standards and Best Practices: Ensure compliance with data governance, '
            'properly document model parameters, and establish retraining strategies for model drift.'
        ),
        'sas_security_auditor': (
            'SAS Security Auditor:\n'
            'Responsibilities: Verify that SAS programs, servers, and data handling practices '
            'meet organizational or regulatory security requirements.\n\n'
            'Methods: Run security scans, review logs for unauthorized access attempts, and confirm '
            'proper encryption for sensitive data.\n\n'
            'Deliverables: Security audit reports, remedial action lists, and updated configuration '
            'files or scripts.\n\n'
            'Working Standards and Best Practices: Conduct regular audits, maintain minimal '
            'privilege controls, and track user permissions closely.'
        ),
        'sas_performance_optimizer': (
            'SAS Performance Optimizer:\n'
            'Responsibilities: Identify inefficiencies in SAS scripts and propose or implement '
            'enhancements.\n\n'
            'Methods: Profile or benchmark code, optimize merges/joins, and ensure correct indexing '
            'or partitioning of datasets.\n\n'
            'Deliverables: Revised SAS programs with improved run times, performance metrics logs, '
            'and a summary of changes.\n\n'
            'Working Standards and Best Practices: Maintain backward compatibility where possible, '
            'document all changes, and monitor performance post-deployment.'
        ),
        'sas_api_developer': (
            'SAS API Developer:\n'
            'Responsibilities: Create or integrate SAS-generated data or analytics into web APIs, '
            'making them accessible to client applications.\n\n'
            'Methods: Define endpoint structures, set up authentication, and ensure consistent '
            'request/response formats. Might involve SAS Stored Processes or SAS Integration '
            'Technologies.\n\n'
            'Deliverables: Working APIs with versioning, usage documentation, and test logs '
            'verifying data accuracy.\n\n'
            'Working Standards and Best Practices: Log requests/responses, enforce SSL/TLS, and '
            'thoroughly document edge cases or error codes.'
        ),
        'sas_database_administrator': (
            'SAS Database Administrator:\n'
            'Responsibilities: Manage database connections, schemas, and query optimization '
            'within SAS environments.\n\n'
            'Methods: Use pass-through SQL, index creation, or partitioning strategies. Implement '
            'backup/recovery plans and failover mechanisms.\n\n'
            'Deliverables: Optimized queries or macros, performance tuning logs, and established '
            'best practices for query usage.\n\n'
            'Working Standards and Best Practices: Enforce secure connections (e.g., SAS/ACCESS), '
            'regularly test backups, maintain consistent naming conventions, and keep an audit '
            'trail for database changes.'
        )
    }

    # Business Email Roles
    business_email_roles = {
        'email_writer': (
            'Email Writer:\n'
            'Responsibilities: Compose concise, effective business emails, ensuring clarity of '
            'purpose and a professional tone.\n\n'
            'Methods: Employ structured outlines, clearly defined subject lines, and short paragraphs '
            'or bullet points for easier scanning.\n\n'
            'Deliverables: Drafted and approved emails reflecting brand voice and etiquette, '
            'templates for recurring communication needs.\n\n'
            'Working Standards and Best Practices: Maintain consistent formatting, proofread for '
            'grammar/spelling, ensure compliance with organizational guidelines, and seek '
            'feedback from recipients.'
        ),
        'communication_coordinator': (
            'Communication Coordinator:\n'
            'Responsibilities: Manage email correspondence schedules, maintain alignment with '
            'organizational messaging, and distribute or escalate messages as needed.\n\n'
            'Methods: Implement tracking systems (e.g., project management tools) to schedule '
            'emails, coordinate approvals, and oversee mass mailings.\n\n'
            'Deliverables: Organized email calendars, status updates to relevant teams, and '
            'archived communication logs.\n\n'
            'Working Standards and Best Practices: Adhere to data privacy policies (e.g., '
            'avoiding mass CC for sensitive data), maintain versioned email templates, '
            'and swiftly update recipients on any changes.'
        ),
        'project_manager': (
            'Project Manager (Business Email Context):\n'
            'Responsibilities: Oversee project-related emails covering timelines, deliverables, '
            'and stakeholder communications.\n\n'
            'Methods: Use collaboration platforms (e.g., Teams, Slack) in conjunction with email '
            'to track tasks and dependencies.\n\n'
            'Deliverables: Detailed email updates on milestones, risk logs if issues arise, and '
            'final recap emails upon project completion.\n\n'
            'Working Standards and Best Practices: Keep a structured email format with clear '
            'action items, deadlines, and ownership. Respect confidentiality when sharing project '
            'details externally.'
        ),
        'client_relations_specialist': (
            'Client Relations Specialist:\n'
            'Responsibilities: Address client inquiries, maintain positive relationships, '
            'and resolve concerns promptly via email.\n\n'
            'Methods: Craft empathetic yet business-focused responses, use client data '
            '(e.g., CRM tools) to personalize communication, and escalate issues when necessary.\n\n'
            'Deliverables: Resolution confirmation emails, follow-up messages tracking client '
            'satisfaction, and summarized communications for management.\n\n'
            'Working Standards and Best Practices: Maintain a friendly yet professional tone, '
            'record all client interactions in a shared database or CRM, and respond within '
            'agreed service-level agreements (SLAs).'
        )
    }

    # Report Review Roles
    report_review_roles = {
        'report_reviewer': (
            'Report Reviewer:\n'
            'Responsibilities: Evaluate the thoroughness, structure, and factual accuracy '
            'of reports to ensure clarity and completeness.\n\n'
            'Methods: Use checklists for factual verification, assess logical flow, '
            'and confirm adherence to formatting or citation standards.\n\n'
            'Deliverables: Marked-up versions of the report with inline comments, '
            'a summarized feedback document addressing high-level improvements.\n\n'
            'Working Standards and Best Practices: Reference guidelines for structuring '
            'professional documents, maintain a consistent feedback process, and confirm '
            'necessary revisions are completed prior to final publication.'
        ),
        'quality_assurance_specialist': (
            'Quality Assurance Specialist (Report Review Context):\n'
            'Responsibilities: Verify that all data, references, and analyses within the '
            'report meet predefined quality standards and regulatory or organizational '
            'requirements.\n\n'
            'Methods: Cross-check data sources, confirm alignment with internal QA rules, '
            'and utilize standardized checklists for evaluating completeness.\n\n'
            'Deliverables: QA certificates or sign-off documents, error logs for any '
            'mismatched data, and final quality assessment summaries.\n\n'
            'Working Standards and Best Practices: Keep thorough documentation of all review '
            'activities, ensure a clear chain of approval, and track versions to pinpoint '
            'where changes occurred.'
        ),
        'content_editor': (
            'Content Editor (Report Review Context):\n'
            'Responsibilities: Refine the language, grammar, and style of a report to ensure '
            'professional tone and readability.\n\n'
            'Methods: Review text for clarity and conciseness, reorganize sections if needed, '
            'and coordinate with authors on suggested changes.\n\n'
            'Deliverables: A polished, reader-friendly version of the report, plus a style '
            'guide or reference document if applicable.\n\n'
            'Working Standards and Best Practices: Adhere to brand or editorial style guides, '
            'use consistent formatting, and document major edits in track-changes or an '
            'equivalent review system.'
        ),
        'compliance_officer': (
            'Compliance Officer (Report Review Context):\n'
            'Responsibilities: Check the report for compliance with legal, regulatory, or '
            'organizational policies. Identify any violations or omissions.\n\n'
            'Methods: Compare content against policy checklists, verify disclaimers, confirm '
            'intellectual property usage, and ensure disclaimers are in place.\n\n'
            'Deliverables: A compliance checklist or matrix indicating pass/fail criteria, '
            'and mandated updates if the report fails certain benchmarks.\n\n'
            'Working Standards and Best Practices: Keep a record of all compliance checks, '
            'notify relevant authorities if critical issues arise, and maintain versioned '
            'proof of compliance sign-off.'
        )
    }

    # Map task types to their extended role dictionaries
    roles_mapping = {
        'python_programming': python_roles,
        'sas_programming': sas_roles,
        'business_email': business_email_roles,
        'report_review': report_review_roles
    }

    return roles_mapping.get(task_type, {})

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

    # Build the prompt with paragraphs and extra line breaks for readability
    prompt_parts = []

    # Paragraph 1: Role and Task Type
    first_paragraph = (
        f"You are a {role_description} specializing in "
        f"{task_types.get(data.get('task_type'), 'the specified task')}."
    )
    prompt_parts.append(first_paragraph)

    # Paragraph 2: Context (if any)
    context = data.get('context_custom') or contexts.get(data.get('context'), '')
    if context:
        prompt_parts.append(f"Context: {context}")

    # General requirements
    prompt_parts.append("""
    Your task is not restricted to giving advice only. 
    You will make a serious attempt to carry out the task given by the user. 
    In addition to the result, you will assess how far you were able to accomplish 
    the task and point out any missing parts or limitations. 
    After that, you may ask follow-up questions to the user that might help you 
    to provide an even more useful response.""")
    
    # Paragraph 3: Task Description
    task_description = data.get('task_description', 'Provide details about the task.')
    prompt_parts.append(f"Task: {task_description}")

    # Paragraph 4: Expected Output
    expected_output = data.get('expected_output', 'Provide details about the expected output.')
    prompt_parts.append(f"Expected Output: {expected_output}")

    # Paragraph 5: Language
    language = data.get('language', 'English')
    prompt_parts.append(f"Please provide the response in {language}.")

    # Join the paragraphs with a blank line in between
    prompt = "\n\n".join(prompt_parts)
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
    <script>
        function enableRoleDropdown() {
            var taskType = document.getElementById('task_type').value;
            var roleDropdown = document.getElementById('role');
            if (taskType) {
                roleDropdown.disabled = false;
            } else {
                roleDropdown.disabled = true;
            }
        }
        window.onload = function() {
            enableRoleDropdown();
        };
    </script>
</head>
<body>
    <h1>Prompt Creator</h1>

    <!-- How to Use -->
    <section style="max-width: 800px; margin-bottom: 30px;">
        <h3>How to Use</h3>
        <p>
            This tool helps you generate structured prompts for large language models (LLMs) like Copilot or Le Chat.
            The mechanic is very simple, the prompt is assembled from the users input and pre-defined textblocks.
            The focus is mainly on coding for the development of statistical models. 
            To get the best result, follow these steps:
        </p>
        <ol>
            <li><strong>Select Task Type:</strong> Choose the nature of the task to be performed (e.g., Python Programming, Business Email).</li>
            <li><strong>Select Context:</strong> Pick a general setting for the task or describe your own context below.</li>
            <li><strong>Select Role:</strong> Choose the role the LLM should take on. This becomes available after you choose a task type.</li>
            <li><strong>Enter Custom Context (optional):</strong> You may provide a specific setting relevant to your use case.</li>
            <li><strong>Describe the Task:</strong> The LLM's reply will strongly depend on the structure, clarity and level of detail of the task description.</li>
            <li><strong>Expected Output:</strong> Explain the format or content you expect in the LLM's reply. Provide a template or example when at hand.</li>
            <li><strong>Select Language:</strong> Choose the language for the final reply of the LLM.</li>
            <li>Click <strong>Create Prompt</strong> to preview or <strong>Save Prompt</strong> to download it as a file.</li>
        </ol>
    </section>

    <form method="post">

        <!-- Select Task Type -->
        <label for="task_type"><strong>Select Task Type:</strong></label><br>
        <small>Select the kind of task the LLM should perform. This determines available roles and styles.</small><br>
        <select name="task_type" id="task_type" onchange="this.form.submit(); enableRoleDropdown();">
            <option value="">--Select Task Type--</option>
            {% for key, value in task_types.items() %}
            <option value="{{ key }}" {% if request.form.get('task_type') == key %}selected{% endif %}>
                {{ key.replace('_', ' ').title() }}
            </option>
            {% endfor %}
        </select><br><br>

        <!-- Select Context -->
        <label for="context"><strong>Select Context:</strong></label><br>
        <small>Select a general work environment or setting where the task should take place.</small><br>
        <select name="context" id="context">
            <option value="">--None--</option>
            {% for key, value in contexts.items() %}
            <option value="{{ key }}">{{ key.replace('_', ' ').title() }}</option>
            {% endfor %}
        </select><br><br>

        <!-- Select Role -->
        <label for="role"><strong>Select Role:</strong></label><br>
        <small>Choose a professional role the model should adopt. Only available after selecting a task type.</small><br>
        <select name="role" id="role" {% if not roles %}disabled{% endif %}>
            <option value="">--Select Role--</option>
            {% for key, value in roles.items() %}
            <option value="{{ key }}">{{ key.replace('_', ' ').title() }}</option>
            {% endfor %}
        </select><br><br>

        <!-- Custom Context -->
        <label for="context_custom"><strong>Or Enter Custom Context:</strong></label><br>
        <small>Optionally describe your own custom environment or scenario for the task.</small><br>
        <input type="text" id="context_custom" name="context_custom" size="80"><br><br>

        <!-- Task Description -->
        <label for="task_description"><strong>Describe the Task:</strong></label><br>
        <small>Write clearly what you want the LLM to do. Include key actions or questions it should address.</small><br>
        <textarea id="task_description" name="task_description" rows="4" cols="80"></textarea><br><br>

        <!-- Expected Output -->
        <label for="expected_output"><strong>Expected Output:</strong></label><br>
        <small>Describe what kind of response you expect — a summary, a script, a recommendation, etc.</small><br>
        <textarea id="expected_output" name="expected_output" rows="4" cols="80"></textarea><br><br>

        <!-- Select Language -->
        <label for="language"><strong>Select Language:</strong></label><br>
        <small>Select the language in which the LLM should respond.</small><br>
        <select name="language" id="language">
            <option value="English">English</option>
            <option value="German">German</option>
        </select><br><br>

        {% if roles %}
        {% if prompt and not prompt.startswith("Please select a valid role") %}
        <input type="hidden" name="prompt" value="{{ prompt | e }}">
        {% endif %}
        <button type="submit" name="create_prompt">Create Prompt</button>
        <button type="submit" name="save_prompt">Save Prompt</button>
        {% endif %}
    </form>

    {% if prompt %}
    <h2>Generated Prompt:</h2>
    <pre style="white-space: pre-wrap;">{{ prompt }}</pre>
    {% endif %}
</body>
</html>

"""

if __name__ == '__main__':
    app.run(debug=True)
