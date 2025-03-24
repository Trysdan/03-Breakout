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
   Note on Virtual Environment Activation in PowerShell

   If you encounter an error when trying to activate the virtual environment using the `venv\Scripts\activate` command in PowerShell, it may be due to the script execution policy on your system. To resolve this, run the following command in PowerShell before activating the virtual environment:

   ```bash
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
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

### Controls
- **Start Game / Launch Ball**: Press `Enter` (Return key).
- **Paddle Movement**:
  - Move Left: `Left Arrow` key.
  - Move Right: `Right Arrow` key.
- **Pause Game**: Press `Spacebar`.
- **Quit Game**: Press `ESC`.
- **Launch Sticky Balls**: Press `R`.
- **Shoot Cannon Bullets**: Press `F`.

### Power-ups
1. **Two More Balls**:
   - **Effect**: Adds 2 extra balls to the game.
   - **Duration**: Instant (balls remain until lost).
   - **Visual**: Blue icon.

2. **Sticky Paddle**:
   - **Effect**: Balls stick to the paddle on contact. Press `R` to launch them again.
   - **Duration**: Until all stuck balls are launched.
   - **Visual**: Yellow icon.

3. **Teleport Edges**:
   - **Effect**: For 5 seconds, balls pass through edges and reappear on the opposite side.
   - **Duration**: 5 seconds.
   - **Visual**: Edges highlighted in green.

4. **Cannons**:
   - **Effect**: Adds two cannons to the sides of the paddle. Press `F` to shoot bullets that destroy bricks.
   - **Duration**: Up to 5 shots.
   - **Visual**: Red icon and visible cannons on the paddle.

Project created for video game programming practice course.