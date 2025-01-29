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
- **Built-in Code Execution**: Runs Python code directly within the IDE.
- **Quick Submission**: Submit solutions to Advent of Code in one click.
- **User Preferences Panel**: Customize themes and fonts for both the editor and console. Preferences persist upon restart.
- **Session Management**: Securely stores and reuses session tokens for problem fetching.
- **Resizable Panels**: Adjust terminal, question panels, and code editor as needed.
- **Auto-Unlock Part 2**: Automatically loads Part 2 once Part 1 is completed.
- **Tabbed Interface**: Quickly switch between each part, input, and helper functions.
- **Persistent Hint Box**: The last part of the question remains visible at all times, reducing unnecessary scrolling.

## Installation

1. Clone the repository:

```
git clone git@github.com:CypherGuy/AOCode.git
cd AOCode
```
2. Install dependencies:
   
```
pip install -r requirements.txt
```

**Current Development Dependencies:**
```
PySide6>=6.8.1
requests>=2.32
beautifulsoup4>=4.1
```
*(Note: These versions are flexible to allow updates as the project evolves.)*

3. Run the application:

```
python main.py
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
│-- AoCFetcher.py # Fetches problem descriptions and inputs
│-- config.py # Stores session tokens and configuration variables
│-- exec.py # Handles code execution and solution submission
│-- Highlighter.py # Implements syntax highlighting
│-- main.py # Entry point of the application
│-- Preferences.py # Preferences panel for customizing the IDE
│-- requirements.txt # Dependencies for the project
│-- utils.py # Utility functions for problem solving
```
There is also a folder called user_files. What this is will be explained later, but essentially it's a file structure to store user preferences and their utility files, 
identified by their token which is hashed via SHA256 and stored as the folder name. The one you see is a mimic to show what it would look like.

## Technologies Used

- **GUI**: PySide6 (Qt for Python)
- **Web Scraping**: requests, BeautifulSoup4
- **Syntax Highlighting**: Just pure Python!
- **JSON Storage**: For storing user preferences. I plan to shift this over to a NoSQL Database in the future

## Why This Project Matters

AOCode is a demonstration of my skills in GUI development, API integration, real-world problem-solving and most importantly, a demonstration of I work with new technologies. AoCode 
showcases my ability to develop simplistic yet feature-heavy user interfaces and efficiently interact with external data sources based on what users of Advent of Code want.

## Key Technical Challenges & Solutions

### Syntax Highlighting

Over the course of development, the hardest thing for me was getting the string highlighting correct, for example text between a triple quote and a single quote not being 
highlighted when it should be green, or in the case of nested, unclosed quotes highlighting in blue (for classes). With a lot of edge cases to consider, I had to put two 
weeks towards highlighting alone. 

I ended up solving the majority of edge cases by implementing a custom state-based syntax highlighter that tracks whether the editor is 
currently inside a string and what type of string it is. This approach ensures that highlighting remains accurate even as the user types dynamically, making the 
experience much smoother and more intuitive.

### User Utility Functions

Another issue I struggled with was how I could have a custom file for utility functions specific to each user. Initially, I considered storing each user's utility functions 
in a dictionary, but this approach quickly ran into problems with memory consumption and complexity. Every user's functions would exist in RAM simultaneously, making it 
inefficient and unscalable. 

To resolve this, I designed a filesystem-based solution structured like this:

```
user_files/
├── <hashed_user_token_1>/
  ├── utils.py
├── <hashed_user_token_2>/
  ├── utils.py
```


This setup ensures that each user has their own isolated `utils.py` file, allowing them to maintain custom helper functions without interfering with others. When executing code, the system automatically loads the corresponding `utils.py`, making user-defined utilities instantly available without the need for manual imports. This method also streamlines error detection and debugging, significantly enhancing the user experience.

## Plans for the Future

- Allow for theme colours and styles of your choice via hexcode
- Support for additional programming languages beyond Python
- Introducing debugging tools (breakpoints, variable inspection, etc.)
- Expanding functionality for competitive programming beyond Advent of Code
- Integration with LLM's (with restrictions on the first 60 minute after puzzle release or after part 2 is completed to prevent cheating and getting a flase leaderboard position)
- Shift from JSON files to Databases

## Contributions & Community

Contributions are welcome! If you have ideas for improvements or want to contribute, feel free to open an issue or submit a pull request.

## Author

Created by CypherGuy. Feel free to contribute or reach out!

## Screenshots

<img width="1000" alt="AOCode IDE interface displaying problem statement, code editor, and output panel for Advent of Code." src="https://github.com/user-attachments/assets/350a1c26-ea43-41e3-aa4c-17c750937f40" />
*AOCode IDE interface displaying problem statement, code editor, and output panel for Advent of Code.*

<img width="1000" alt="Getting the wrong answer on the IDE" src="https://github.com/user-attachments/assets/e3826c07-1613-4bcd-b391-d72219a7292a" />
*Getting the wrong answer on the IDE*

<img width="1000" alt="Preferences dialog to change how the IDE looks" src="https://github.com/user-attachments/assets/69928fc2-127b-42a7-a179-44459b9eb162" />
*Preferences dialog to change how the IDE looks*

<img width="1000" alt="An example theme" src="https://github.com/user-attachments/assets/e4d9859e-3b11-4e9a-97bc-a26454cdeafb" />
*An example theme*




