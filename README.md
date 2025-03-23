# Breakout Game

Classic Breakout implementation in Python using Pygame and Gale libraries.

## Requirements
- **Python**
- **Pygame**
- **Gale**

## Installation
### Windows
1. **Install Python**:
   - Download and install Python from [python.org](https://www.python.org/downloads/).
   - During installation, ensure you check the box **"Add Python to PATH"**.

2. Clone repository:
   ```bash
   git clone https://github.com/Trysdan/03-Breakout.git
   cd 03-Breakout
   ```

3. Create and activate virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Linux
1. **Install Python**:
   - Most Linux distributions come with Python pre-installed. Check your version:
     ```bash
     python3 --version
     ```
   - If Python is not installed, use your package manager:
     - **Debian/Ubuntu**:
       ```bash
       sudo apt update
       sudo apt install python3
       ```
     - **Fedora**:
       ```bash
       sudo dnf install python3
       ```

2. Clone repository:
   ```bash
   git clone https://github.com/Trysdan/03-Breakout.git
   cd 03-Breakout
   ```

3. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game
1. Start the game:
   ```bash
   python main.py
   ```

2. Deactivate virtual environment when done:
   ```bash
   deactivate
   ```

## Controls
- **Start Game / Launch Ball:** Press `Enter` (Return key).
- **Paddle Movement:**
  - Move Left: `Left Arrow` key.
  - Move Right: `Right Arrow` key.
- **Quit Game:** Press `ESC`.


## Power-up
- **TeleportEdges**
  - **Effect:** Balls pass through edges, reappearing on the opposite side.
  - **Duration:** 5 seconds.
  - **Visual:** Edges highlighted in green.

Project created for video game programming practice course.