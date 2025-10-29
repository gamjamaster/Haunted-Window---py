# Import required libraries
import tkinter as tk  # For creating GUI window
from tkinter import messagebox  # For showing message boxes
import random  # For random effects
import time  # For delays and timing
from PIL import Image, ImageTk  # For image handling
import os  # For file path operations
import pygame  # For sound effects and keyboard events
import subprocess  # For launching notepad and system commands

class HauntedWindow:
    def __init__(self):
        """Initialize the haunted window program with all necessary components"""
        # Initialize pygame for sound and keyboard event handling
        pygame.init()
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Haunted Window")
        
        # Get screen dimensions for fullscreen mode
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Make window fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Set transparency - black pixels become transparent
        self.root.attributes('-transparentcolor', 'black')
        self.root.attributes('-topmost', True)  # Keep window on top
        self.root.configure(bg='black')
        
        # Force window to have focus
        self.root.focus_force()
        
        # Flag to track if program should exit
        self.should_exit = False
        
        # Bind ESC key to exit
        self.root.bind('<Escape>', lambda e: self.exit_program())
        
        # Make window click-through initially (transparent to mouse)
        self.root.wm_attributes('-disabled', True)
        
        # Create canvas for drawing effects
        self.canvas = tk.Canvas(self.root, width=self.screen_width, 
                                height=self.screen_height, bg='black', 
                                highlightthickness=0)
        self.canvas.pack()
        
        # Initialize image storage
        self.images = []
        self.jumpscare_image = None
        
        # Load all sound files
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound files from the sounds folder"""
        # Create sounds folder if it doesn't exist
        sounds_folder = os.path.join(os.path.dirname(__file__), 'sounds')
        
        if not os.path.exists(sounds_folder):
            os.makedirs(sounds_folder)
            print(f"Please add sound files to: {sounds_folder}")
        
        # Initialize sound variables
        self.background_sound = None
        self.ghost_sound = None
        self.jumpscare_sound = None
        self.keyboard_sound = None
        
        # Load background music (looping)
        bg_path = os.path.join(sounds_folder, 'background.mp3')
        if os.path.exists(bg_path):
            self.background_sound = bg_path
            print("Loaded background.mp3")
        
        # Load ghost sound effect
        ghost_path = os.path.join(sounds_folder, 'ghost.mp3')
        if os.path.exists(ghost_path):
            self.ghost_sound = pygame.mixer.Sound(ghost_path)
            print("Loaded ghost.mp3")
        
        # Load jumpscare sound effect
        jumpscare_path = os.path.join(sounds_folder, 'jumpscare.mp3')
        if os.path.exists(jumpscare_path):
            self.jumpscare_sound = pygame.mixer.Sound(jumpscare_path)
            print("Loaded jumpscare.mp3")
        
        # Load keyboard typing sound effect
        keyboard_path = os.path.join(sounds_folder, 'keyboard.mp3')
        if os.path.exists(keyboard_path):
            self.keyboard_sound = pygame.mixer.Sound(keyboard_path)
            print("Loaded keyboard.mp3")
    
    def play_sound(self, sound_type):
        """Play a specific sound by type"""
        if sound_type == 'background' and self.background_sound:
            pygame.mixer.music.load(self.background_sound)
            pygame.mixer.music.play(-1)  # Loop indefinitely
        elif sound_type == 'ghost' and self.ghost_sound:
            self.ghost_sound.play()
        elif sound_type == 'jumpscare' and self.jumpscare_sound:
            self.jumpscare_sound.play()
        elif sound_type == 'keyboard' and self.keyboard_sound:
            self.keyboard_sound.play()
    
    def stop_sound(self):
        """Stop all currently playing sounds"""
        pygame.mixer.music.stop()
    
    def exit_program(self):
        """Safely exit the program"""
        if self.should_exit:
            return  # Already exiting
        self.should_exit = True
        self.stop_sound()
        pygame.quit()
        self.root.quit()
    
    def check_for_escape(self):
        """Check if ESC key was pressed using pygame events"""
        if self.should_exit:
            return True
        
        # Periodically reclaim focus to ensure ESC key works
        if not self.root.focus_get():
            self.root.focus_force()
        
        # Check for ESC key in pygame event queue
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit_program()
                return True
        return False
        
    def load_jumpscare_image(self):
        """Load and resize the jumpscare image"""
        # Look for jumpscare.jpg in the ghost_images folder
        jumpscare_path = os.path.join(os.path.dirname(__file__), 'ghost_images', 'jumpscare.jpg')
        
        if os.path.exists(jumpscare_path):
            # Open and resize image to fit screen
            img = Image.open(jumpscare_path)
            img = img.resize((self.screen_width, self.screen_height), 
                           Image.Resampling.LANCZOS)
            self.jumpscare_image = ImageTk.PhotoImage(img)
            return True
        return False
    
    def show_jumpscare(self):
        """Display jumpscare image with sound and wait for sound to finish"""
        # Temporarily disable click-through so jumpscare is visible
        self.root.wm_attributes('-disabled', False)
        
        # Play jumpscare sound
        self.play_sound('jumpscare')
        
        # Clear canvas
        self.canvas.delete('all')
        
        # Try to load and show the jumpscare image
        if self.load_jumpscare_image() and self.jumpscare_image:
            self.canvas.configure(bg='black')
            self.canvas.create_image(
                self.screen_width // 2,
                self.screen_height // 2,
                image=self.jumpscare_image
            )
        else:
            # Fallback: Show red screen with "BOO!!!" text
            self.canvas.configure(bg='red')
            self.canvas.create_text(
                self.screen_width // 2,
                self.screen_height // 2,
                text="BOO!!!",
                font=("Arial", 200, "bold"),
                fill="black"
            )
        
        self.root.update()
        
        # Wait for jumpscare sound to finish playing
        if self.jumpscare_sound:
            while pygame.mixer.get_busy():  # Check if sound is still playing
                if self.check_for_escape() or self.should_exit:
                    return
                time.sleep(0.1)
                self.root.update()
        else:
            # If no sound file, wait 3 seconds as fallback
            start_time = time.time()
            while time.time() - start_time < 3:
                if self.check_for_escape() or self.should_exit:
                    return
                time.sleep(0.1)
                self.root.update()
        
        # Clear the jumpscare
        self.canvas.delete('all')
    
    def show_black_screen_with_blink(self):
        """Show black screen that blinks 8 times, then stays black for 3 seconds"""
        # Make window visible (disable click-through)
        self.root.wm_attributes('-disabled', False)
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        self.root.update()
        
        # Blink the screen 8 times by toggling colors
        is_black = True  # Start with black
        blink_count = 0
        max_blinks = 8  # Total number of blinks
        
        while blink_count < max_blinks:
            if self.check_for_escape() or self.should_exit:
                return
            
            # Alternate between black and near-black (#050505)
            # We use #050505 instead of white to avoid harsh flashing
            if is_black:
                self.canvas.configure(bg='black')
            else:
                self.canvas.configure(bg='#050505')  # Near-black to avoid transparency issues
            
            is_black = not is_black
            self.root.update()
            time.sleep(1.0)  # 1 second per color change
            blink_count += 1
        
        # After blinking, stay black for 3 seconds
        self.canvas.configure(bg='black')
        self.root.update()
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
            self.root.update()
    
    def show_haunted_notepad(self):
        """Open notepad and type random text, then show a haunted message"""
        import subprocess
        import pyautogui
        
        # Close any existing notepad windows to start fresh
        subprocess.run(['taskkill', '/F', '/IM', 'notepad.exe'], 
                      capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        time.sleep(0.3)
        
        # Open a new notepad window
        notepad = subprocess.Popen(['notepad.exe'])
        time.sleep(1)  # Wait for notepad to open

        # Set notepad font size via registry (larger font for horror effect)
        font_height = -18
        subprocess.run([
            "reg", "add", "HKCU\\Software\\Microsoft\\Notepad",
            "/v", "lfHeight",
            "/t", "REG_DWORD",
            "/d", str(font_height),
            "/f"
        ])
        
        # Load text from random.txt file
        random_txt_path = os.path.join(os.path.dirname(__file__), 'random.txt')
        
        if os.path.exists(random_txt_path):
            with open(random_txt_path, 'r', encoding='utf-8') as f:
                random_text = f.read()
            print(f"Loaded random.txt with {len(random_text)} characters")
        else:
            print("random.txt not found, using fallback random text")
            random_text = 'abcdefghijklmnopqrstuvwxyz' * 50  # Fallback text
        
        total_chars = len(random_text)
        
        # Phase 1: Type each character from random.txt with keyboard sound
        for i, char in enumerate(random_text):
            if self.check_for_escape() or self.should_exit:
                notepad.terminate()
                return
            
            # Play keyboard sound before typing for better sync
            if self.keyboard_sound:
                self.keyboard_sound.play(maxtime=300)  # Limit sound duration
            else:
                self.play_sound('keyboard')

            # Type the character (handle line breaks separately)
            if char == '\n':
                pyautogui.press('enter')
            else:
                pyautogui.write(char, interval=0)

            # Slow typing for first 10 characters, then fast
            if i < 10:
                delay = 0.3  # Slow for dramatic effect
            else:
                delay = 0.01  # Fast for the rest
            time.sleep(delay)
        
        # Phase 2: Pause for 3 seconds
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                notepad.terminate()
                return
            time.sleep(0.1)
        
        # Phase 3: Type the haunted message slowly
        pyautogui.press('enter')  # Go to new line
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'b')  # Attempt to bold (may not work in Notepad)
        time.sleep(0.2)
        
        message = "DO NOT LOOK BACK"
        for i, char in enumerate(message):
            if self.check_for_escape() or self.should_exit:
                notepad.terminate()
                return
            # Play keyboard sound before each character
            if self.keyboard_sound:
                self.keyboard_sound.play(maxtime=300)
            else:
                self.play_sound('keyboard')

            pyautogui.write(char, interval=0)
            time.sleep(0.3)  # Slow typing for suspense
        
        # Close notepad without saving
        notepad.terminate()
        time.sleep(0.5)
        
        # Phase 4: Show black screen for 3 seconds after closing notepad
        self.root.wm_attributes('-disabled', False)  # Make window visible
        self.root.attributes('-alpha', 1.0)  # Make fully opaque
        self.canvas.delete('all')
        self.canvas.configure(bg='#050505')  # Near-black (avoids transparency issues)
        self.root.update()
        
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
            self.root.update()
    
    def show_thank_you(self):
        """Display thank you message and close the program"""
        self.root.withdraw()  # Hide main window
        messagebox.showinfo("Thank You", "Thank you for executing!")
        self.root.quit()
    
    def run(self):
        """Main program flow - orchestrates all haunted effects in sequence"""
        # Start background music at the beginning
        self.play_sound('background')
        
        # Step 1: Wait 3 seconds before starting
        print("Waiting 5 seconds...")
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
        
        # Step 2: Black screen blinks 8 times, then stays for 3 seconds
        print("Black screen sequence...")
        self.show_black_screen_with_blink()
        if self.should_exit:
            return
        
        # Step 3: Notepad appears and types random text + haunted message
        print("Notepad sequence...")
        self.show_haunted_notepad()
        if self.should_exit:
            return
        
        # Step 4: Show jumpscare with image and sound
        print("Jumpscare!")
        self.show_jumpscare()
        if self.should_exit:
            return
        
        # Step 5: Clean up and show thank you message
        self.stop_sound()
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        self.show_thank_you()

# Program entry point
if __name__ == "__main__":
    # Display program information and instructions
    print("=" * 60)
    print("HAUNTED WINDOW PROGRAM")
    print("=" * 60)
    print("\n⚠️  TO EXIT THE PROGRAM:")
    print("   Option 1: Press ESC key (works best if you don't click away)")
    print("   Option 2: Close this terminal window")
    print("   Option 3: Press Ctrl+C in this terminal")
    print("\n🎃 Starting haunted experience...\n")
    print("=" * 60)
    
    # Create and run the haunted window application
    app = HauntedWindow()
    app.run()
