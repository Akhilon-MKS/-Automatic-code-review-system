# Automated Source Code Review and Quality Metrics System

This is a web-based tool for automated code review and quality analysis of Python source code files.

## Features

- **Static Code Analysis**: Uses pylint and radon for comprehensive code quality checks
- **Quality Scoring**: Calculates maintainability and readability scores
- **Command Line Analysis**: Analyzes shell commands for security issues and best practices
- **Multiple Interfaces**:
  - Web interface with visual code display and downloadable reports
  - Command-line interface with colored terminal output and line-by-line suggestions
- **Detailed Feedback**: Line-by-line suggestions and issue highlighting
- **Report Generation**: Downloadable TXT and PDF reports
- Detection of syntax errors, naming convention issues, complexity problems

## Requirements

- Python 3.7+
- Flask
- pylint
- radon
- reportlab

## Installation

1. Clone or download the project files.
2. Navigate to the project directory: `cd code_review_system`
3. Create a virtual environment: `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install flask pylint radon reportlab`

## Usage

### Web Interface

1. Run the application: `python app.py`
2. Open your web browser and go to `http://localhost:5000`
3. Upload one or more Python files using the file selector
4. Click "Analyze Code" to start the review process
5. View the results, including issues found, quality score, and suggestions
6. Download reports in TXT or PDF format

### Command Line Interface

Get detailed analysis directly in your terminal:

```bash
# Full analysis with colored output and line-by-line suggestions
python cli.py path/to/your/file.py

# Show only quality score
python cli.py path/to/your/file.py --score-only
```

The CLI provides:
- Colored terminal output for different issue types
- Line-by-line code display with inline suggestions
- Summary of issues and recommendations

## Sample Files

The project includes sample files for testing:
- `sample_good_code.py`: Demonstrates good coding practices
- `sample_bad_code.py`: Contains various code quality issues for demonstration

## How It Works

The system performs the following analyses:

1. **Syntax and Style Checking**: Uses pylint to detect errors, warnings, and style issues
2. **Complexity Analysis**: Uses radon to measure code complexity and identify overly complex functions
3. **Naming Convention Checks**: Analyzes AST to ensure proper naming conventions (snake_case for functions, PascalCase for classes)
4. **Quality Scoring**: Calculates an overall score based on detected issues
5. **Suggestions**: Provides actionable recommendations for improvement

## Extending to Other Languages

The system is designed to be extensible. To add support for other languages:

1. Replace pylint with language-specific linters (e.g., ESLint for JavaScript, Checkstyle for Java)
2. Update the complexity analysis to use appropriate tools
3. Modify AST parsing for language-specific naming conventions
4. Adjust scoring algorithms as needed

## Security Note

This tool performs static analysis only and does not execute the uploaded code, ensuring security.
