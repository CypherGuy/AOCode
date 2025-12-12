from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton


class Infobox(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Information")
        self.setGeometry(300, 300, 500, 500)

        main_layout = QVBoxLayout()

        # Keyboard Shortcuts Section
        shortcuts_title = QLabel("Keyboard Shortcuts")
        shortcuts_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(shortcuts_title)

        shortcuts_label = QLabel("""
- Cmd+R: Run your code
- Cmd+Enter: Submit your answer
- Cmd+P: Toggle preferences panel
- Cmd+I: Toggle this info box
- Cmd+1/2/3/4: Switch between Part 1, Part 2, Input, and Utils tabs
        """)
        shortcuts_label.setWordWrap(True)
        main_layout.addWidget(shortcuts_label)

        # Tips Section
        tips_title = QLabel("Tips")
        tips_title.setStyleSheet(
            "font-weight: bold; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(tips_title)

        tips_label = QLabel("""
- There's a hint box for you to view the question in the top left.
- Line numbers are displayed on the left of the code editor.
- Click on 'Utils File' to add your own functions you can call at any time.                            
- Your input data can be called using the variable 'data'.                            
- Click on 'Run' to execute your code and view the output in the console.                    
- You can also click on 'Submit' to submit your solution to the server.                      
- Click on the cog icon to open the preferences panel, where you can customize your theme and font.
        """)
        tips_label.setWordWrap(True)
        main_layout.addWidget(tips_label)

        # Features Section (collapsible)
        self.features_button = QPushButton("Show Features")
        self.features_button.clicked.connect(self.toggle_features)
        main_layout.addWidget(self.features_button)

        self.features_label = QLabel("""
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
        self.features_label.setWordWrap(True)
        self.features_label.hide()
        main_layout.addWidget(self.features_label)

        main_layout.addStretch()
        self.setLayout(main_layout)

    def toggle_features(self):
        if self.features_label.isVisible():
            self.features_label.hide()
            self.features_button.setText("Show Features")
        else:
            self.features_label.show()
            self.features_button.setText("Hide Features")
