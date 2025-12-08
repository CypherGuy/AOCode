from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout


class Infobox(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(300, 300, 500, 400)

        main_layout = QVBoxLayout()

        # How to Use Section
        howto_title = QLabel("Tips and hints")
        howto_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(howto_title)

        howto_label = QLabel("""
- There's a hint box for you to view the question in the top left.                            
- Click on 'Utils File' to add your own functions you can call at any time.                            
- Your input data can be called using the variable 'data'.                            
- Click on 'Run' to execute your code and view the output in the console.                    
- You can also click on 'Submit' to submit your solution to the server.                      
- Click on the cog icon to open the preferences panel, where you can customize your theme and font.
        """)
        howto_label.setWordWrap(True)
        main_layout.addWidget(howto_label)

        # Features Section
        features_title = QLabel("Features")
        features_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(features_title)

        features_label = QLabel("""
Built-By-Scratch Syntax Highlighter
Built-in Code Execution
One-Click Solution Submission
User Preferences Panel with persistent theme and font customization
Secure Session Management
Resizable Panels
Auto-Unlock Part 2
Tabbed Interface for parts, input, and helper functions
Hint Box displaying the actual question so no need to scroll
        """)
        features_label.setWordWrap(True)
        main_layout.addWidget(features_label)

        self.setLayout(main_layout)
        self.show()
