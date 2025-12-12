# AoCode - Advent of Code IDE

AoCode is a lightweight Python-based Integrated Development Environment (IDE) designed for Advent of Code, built to solve challenges as efficiently and quickly as possible.
It provides an efficient interface for writing, running, and submitting solutions with built-in syntax highlighting, automated input fetching, and custom preferences.

## Why AoCode?

As someone who participates in Advent of Code, I want a way to streamline my code with a fast yet efficient way to submit answers and have quick access to any helper functions
I've created. AoCode solves this by keeping everything you need — the question, code editor, and utilities — just one click away. There's no need to even open the
Advent of Code website, as the IDE fetches the problem statement and input for you. I also built this project to challenge my way of thinking and experiment with new libraries
I haven't used before.

## Features

- **Built-By-Scratch Syntax Highlighter**: No-library Syntax Highlighter highlights Python keywords, functions, comments, etc.
- **Smart Code Editor**: Line numbers, auto-indentation, block indent/dedent with Tab/Shift+Tab, and smooth tab navigation.
- **Built-in Code Execution**: Runs Python code directly within the IDE.
- **Automatic Input Loading**: Your puzzle input is automatically available as the `data` variable. No need to read files.
- **Quick Submission**: Submit solutions to Advent of Code in one click.
- **Color-Coded Feedback**: Terminal displays green for correct answers, red for incorrect ones.
- **User Preferences Panel**: Customize themes and fonts for both the editor and console. Preferences persist upon restart.
- **Custom Theme Creator**: Use the built-in color picker to create your own custom color themes.
- **Session Management**: Securely stores and reuses session tokens via system keyring.
- **Auto-Save Utils**: Your custom utility functions save automatically as you type.
- **Resizable Panels**: Adjust terminal, question panels, and code editor as needed.
- **Auto-Unlock Part 2**: Automatically loads Part 2 once Part 1 is completed.
- **Tabbed Interface**: Quickly switch between each part, input, and helper functions.
- **Persistent Hint Box**: The last part of the question remains visible at all times, reducing unnecessary scrolling.
- **Keyboard Shortcuts**: Lightning-fast workflow with comprehensive keyboard shortcuts (see below).

## Keyboard Shortcuts

Make your workflow lightning-fast with these shortcuts:

- **Cmd+R**: Run your code
- **Cmd+Enter**: Submit your answer to Advent of Code
- **Cmd+P**: Toggle preferences panel
- **Cmd+I**: Open info/help dialog
- **Cmd+1/2/3/4**: Switch between Part 1, Part 2, Input, and Utils tabs
- **Tab**: Indent current line or selection (4 spaces)
- **Shift+Tab**: Dedent current line or selection

## Installation

1. Clone the repository:

```
git clone git@github.com:CypherGuy/AOCode.git
cd AOCode
```

2. Install dependencies:

```
pip install -r Code/requirements.txt
```

**Current Dependencies:**

```
PySide6>=6.8.1
requests>=2.32
beautifulsoup4>=4.10
keyring>=25.7.0
```

**Development Dependencies (for testing):**

```
pytest>=9.0.2
pytest-qt>=4.5.0
pytest-mock>=3.15.1
pytest-cov>=7.0.0
```

_(Note: These versions are flexible to allow updates as the project evolves.)_

3. Run the application:

```
python Code/main.py
```

And you're done!

## Usage

### Starting the IDE

Upon running `main.py`, you will be prompted to enter your Advent of Code session token. This token is required to fetch problems and submit solutions.

### Writing and Running Code

- The left panel contains problem descriptions and input.
- The right panel includes the editor and terminal.
- Write your code in the editor and press the **Run** button to execute it, or the **Submit** button to submit it to Advent of Code and get a response.

### Submitting Answers

- Click the **Submit** button to send your solution.
- The response from Advent of Code will appear in the terminal, indicating whether the answer is correct.

### Customizing Preferences

- Click the **Settings** button to open the preferences panel.
- Customize the font and theme for both the editor and console.
- Press **Save** to apply changes.

## File Structure

```
AOCode/
├── Code/
│   ├── main.py                    # Entry point of the application
│   ├── requirements.txt           # Project dependencies
│   │
│   ├── config/
│   │   ├── config.py              # Global configuration and theme definitions
│   │   └── preferences.py         # Preferences panel for customizing the IDE
│   │
│   ├── core/
│   │   ├── aoc_fetcher.py         # Fetches problem descriptions and inputs from AoC
│   │   ├── runner.py              # Handles code execution and solution submission
│   │   └── utils.py               # User utilities manager and template
│   │
│   ├── ui/
│   │   ├── code_editor.py         # Code editor with line numbers
│   │   ├── highlighter.py         # Custom Python syntax highlighter
│   │   └── infobox.py             # Information and help dialog
│   │
│   ├── tests/                     # Test suite
│   │   ├── conftest.py            # Pytest configuration
│   │   └── test_*.py              # Various test files
│   │
│   └── images/                    # UI assets (icons)
│
├── user_files/                    # User-specific data (gitignored)
│   └── [hashed_token]/            # Per-user directory (SHA256 of session token)
│       ├── preferences.json       # Saved user preferences
│       └── utils.py               # User's custom utility functions
│
├── requirements-dev.txt           # Development dependencies
└── README.md                      # This file
```

The `user_files` folder stores user preferences and utility files, with each user identified by their session token hashed via SHA256.
You can define custom functions in your `utils.py` file and call them directly in your solutions without any imports needed.

## Technologies Used

- **GUI**: PySide6 (Qt for Python)
- **Web Scraping**: requests, BeautifulSoup4
- **Secure Storage**: keyring (for session token management)
- **Syntax Highlighting**: Custom built-from-scratch Python highlighter
- **Testing**: pytest with Qt support
- **Data Storage**: JSON for user preferences

## Plans for the Future

- Allow for theme colours and styles of your choice via hexcode
- Support for additional programming languages beyond Python
- Introducing debugging tools (breakpoints, variable inspection, etc.)
- Expanding functionality for competitive programming beyond Advent of Code
- Integration with LLM's
- Shift from JSON files to Databases

## Contributions & Community

Contributions are welcome! If you have ideas for improvements or want to contribute, feel free to open an issue or submit a pull request.

## Author

Created by CypherGuy. Feel free to contribute or reach out!

## Screenshots

<img width="1000" alt="AOCode IDE interface displaying problem statement, code editor, and output panel for Advent of Code." src="https://i.imgur.com/9XSQsxk.png" />
*AOCode IDE interface displaying problem statement, code editor, and output panel for Advent of Code.*

<img width="1000" alt="Getting the wrong answer on the IDE" src="https://github.com/user-attachments/assets/e3826c07-1613-4bcd-b391-d72219a7292a" />
*Getting the wrong answer on the IDE*

<img width="1000" alt="Preferences dialog to change how the IDE looks" src="https://github.com/user-attachments/assets/69928fc2-127b-42a7-a179-44459b9eb162" />
*Preferences dialog to change how the IDE looks*

<img width="1000" alt="An example theme" src="https://github.com/user-attachments/assets/e4d9859e-3b11-4e9a-97bc-a26454cdeafb" />
*An example theme*
