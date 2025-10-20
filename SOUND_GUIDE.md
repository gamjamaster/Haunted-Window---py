# Sound Guide for Haunted Window

The program now supports sound effects! Follow this guide to add spooky sounds to your haunted experience.

## Setup

### 1. Install pygame

First, install the pygame library (for sound playback):

```bash
pip install pygame
```

Or if using virtual environment:
```bash
venv\Scripts\activate
pip install pygame
```

### 2. Create Sounds Folder

A `sounds` folder will be automatically created in your project directory when you run the program.

Location: `C:\Users\kim\Desktop\Perosnal Project\Haunted Window - py\sounds\`

### 3. Add Sound Files

Add the following MP3 files to the `sounds` folder:

#### Required Sound Files:

1. **`background.mp3`** - Background music that plays during the ghost phase (loops continuously)
2. **`ghost.mp3`** - Sound effect that plays each time a ghost appears
3. **`jumpscare.mp3`** - Sound effect that plays during the jumpscare

## Sound Behavior

### Background Music (`background.mp3`)
- Starts playing when ghosts begin appearing
- Loops continuously throughout the ghost phase
- Stops when ghost phase ends
- **Recommended**: Eerie ambient music, creepy whispers, or haunted house sounds

### Ghost Sound (`ghost.mp3`)
- Plays each time a new ghost appears on screen
- Short sound effect
- **Recommended**: Whisper, moan, ethereal sound, or ghost wail

### Jumpscare Sound (`jumpscare.mp3`)
- Plays when the jumpscare image appears
- Should be loud and startling
- **Recommended**: Scream, loud bang, horror sting

## Supported Formats

- `.mp3` (recommended)
- `.wav` (also supported)
- `.ogg` (also supported)

## File Organization

```
Haunted Window - py/
├── haunted_window.py
├── sounds/
│   ├── background.mp3
│   ├── ghost.mp3
│   └── jumpscare.mp3
├── ghost_images/
│   ├── ghost1.png
│   ├── ghost2.png
│   └── jumpscare.jpg
└── requirements.txt
```

## Optional: Sounds are Optional

If you don't add sound files, the program will still work perfectly - it will just run silently. The program checks if sound files exist before trying to play them.

## Tips for Finding Sounds

- **Free Sound Resources**: 
  - freesound.org
  - zapsplat.com
  - mixkit.co
  - YouTube Audio Library

- **Sound Length Recommendations**:
  - Background: 30-60 seconds (will loop)
  - Ghost: 1-3 seconds
  - Jumpscare: 2-5 seconds

## Troubleshooting

**No sound playing?**
1. Make sure pygame is installed: `pip install pygame`
2. Check that sound files are in the `sounds` folder
3. Verify file names are exactly: `background.mp3`, `ghost.mp3`, `jumpscare.mp3`
4. Try using `.wav` format if `.mp3` doesn't work

**Sound is too loud/quiet?**
You can adjust volume in the code by modifying the `play_sound` method to include volume settings.

Enjoy your haunted experience with sound! 👻🔊
