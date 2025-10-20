# Haunted Window Program

A Python program that creates a spooky haunted window experience!

## Features

1. **Opening Screen**: Displays "HAUNTED!!!" in large red text for 3 seconds
2. **Ghost Animation**: Random ghost images appear on screen for 3 minutes
3. **Jumpscare**: A full-screen jumpscare appears for 3 seconds
4. **Thank You Message**: A message box thanking you for executing the program

## Requirements

Install the required packages:

```bash
pip install pillow
```

## Setup

### Optional: Add Custom Images

1. **Ghost Images**: Create a folder named `ghost_images` in the same directory as the script and add your ghost images (PNG, JPG, or GIF format)
2. **Jumpscare Image**: Add a file named `jumpscare.png` in the same directory for the jumpscare effect

If you don't add images, the program will use emoji ghosts (👻) and a red "BOO!!!" screen as fallbacks.

## Usage

Run the program:

```bash
python haunted_window.py
```

**Note**: Press `ESC` at any time to exit the program safely.

## Program Flow

1. Fullscreen window opens
2. "HAUNTED!!!" appears in red (3 seconds)
3. Random ghost images appear and disappear (3 minutes)
4. Jumpscare fills the screen (3 seconds)
5. Thank you message box appears
6. Program exits

## Customization

You can modify the following in the code:

- Duration of ghost animation (default: 180 seconds/3 minutes)
- Ghost spawn rate (adjust the probability in `show_random_ghosts`)
- Ghost size and appearance time
- Text and colors for the opening and jumpscare screens

Enjoy your haunted experience! 👻

## License
- Music by <a href="https://pixabay.com/users/pulsebox-52068281/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=420687">PulseBox</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=420687">Pixabay</a>

- <a href="https://www.vecteezy.com/free-photos/pornographic">Pornographic Stock photos by Vecteezy</a>s

- <a href="https://kr.freepik.com/free-ai-image/view-mysterious-entity-dark-foggy-room_69809215.htm#fromView=search&page=1&position=45&uuid=f176187e-746d-4e52-bb7d-2f09b7eff34d&query=%EA%B3%B5%ED%8F%AC">by freepik</a>
