# Haunted Window Program

A Python program that creates a terrifying haunted experience with screen effects, automated notepad typing, and jumpscares!

## Features

1. **Black Screen Blinking**: The entire screen is covered in black and blinks 8 times with suspenseful timing
2. **Haunted Notepad**: Notepad automatically opens and types random text from `random.txt`, then slowly types "DO NOT LOOK BACK"
3. **Keyboard Sound Effects**: Each keystroke in notepad is accompanied by a typing sound for realism
4. **Jumpscare**: A full-screen jumpscare image appears with sound effects
5. **Background Music**: Atmospheric background music plays throughout the experience
6. **ESC Key Support**: Press ESC at any time to safely exit the program

## Requirements

Install the required packages:

```bash
pip install pillow pygame pyautogui
```

## Setup

### Required Files

1. **random.txt**: Create a file named `random.txt` in the project root containing the text you want the notepad to type

### Optional: Add Sound Files

Create a folder named `sounds` in the same directory as the script and add the following MP3 files:
- `background.mp3` - Background music (loops continuously)
- `keyboard.mp3` - Keyboard typing sound effect
- `jumpscare.mp3` - Jumpscare sound effect
- `ghost.mp3` - Ghost sound effect (optional)

### Optional: Add Jumpscare Image

Create a folder named `ghost_images` and add:
- `jumpscare.jpg` - The image shown during the jumpscare

If you don't add a jumpscare image, the program will show a red "BOO!!!" screen as a fallback.

## Usage

Run the program:

```bash
python haunted_window.py
```

**Exit Options**:
- Option 1: Press `ESC` key (works best if you don't click away)
- Option 2: Close the terminal window
- Option 3: Press `Ctrl+C` in the terminal

## Program Flow

1. **Wait**: Program waits 3 seconds after execution
2. **Black Screen Blink**: Screen blinks black 8 times (1 second per blink), then stays black for 3 seconds
3. **Haunted Notepad Sequence**:
   - All existing notepad windows are closed
   - A fresh notepad window opens
   - Font size is set to 18pt via registry
   - Types contents of `random.txt` character by character (slow start, then fast)
   - Pauses for 3 seconds
   - Types "DO NOT LOOK BACK" slowly on a new line
   - Notepad closes automatically
   - Black screen appears for 3 seconds
4. **Jumpscare**: Full-screen jumpscare image/effect with sound
5. **Thank You**: Message box appears thanking you for executing
6. **Exit**: Program closes

## Technical Details

- **Transparent Window**: Uses tkinter with transparency and click-through capabilities
- **Fullscreen Effect**: Window covers entire screen and stays on top
- **Sound System**: pygame mixer for audio playback with sound synchronization
- **Keyboard Automation**: pyautogui for typing simulation in notepad
- **Registry Editing**: Modifies Windows registry to set notepad font size
- **Process Management**: Uses subprocess and taskkill to manage notepad windows

## Customization

You can modify the following in the code:

- Blink count and speed in `show_black_screen_with_blink()`
- Typing speed in `show_haunted_notepad()` (currently: 0.3s for first 10 chars, 0.01s for rest)
- Message text (currently: "DO NOT LOOK BACK")
- Font size via the `font_height` variable (currently: -18)
- Wait durations between sequences

Enjoy your haunted experience! 👻🎃

## License
- Music by <a href="https://pixabay.com/users/pulsebox-52068281/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=420687">PulseBox</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=420687">Pixabay</a>

<a href="https://www.vecteezy.com/free-photos/inanimate">Inanimate Stock photos by Vecteezy</a>
