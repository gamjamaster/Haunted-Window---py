import tkinter as tk
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk
import os
import pygame  # For sound effects
import subprocess

class HauntedWindow:
    def __init__(self):
        # Initialize pygame for sound and keyboard
        pygame.init()
        
        self.root = tk.Tk()
        self.root.title("Haunted Window")
        
        # Get screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Make window fullscreen
        self.root.attributes('-fullscreen', True)
        
        # Make window transparent and click-through
        self.root.attributes('-transparentcolor', 'black')
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        
        # Keep window focused
        self.root.focus_force()
        
        # Flag for exit
        self.should_exit = False
        
        # Allow escape key to exit (for safety)
        self.root.bind('<Escape>', lambda e: self.exit_program())
        
        # Start with window disabled (click-through)
        self.root.wm_attributes('-disabled', True)
        
        # Canvas for displaying content
        self.canvas = tk.Canvas(self.root, width=self.screen_width, 
                                height=self.screen_height, bg='black', 
                                highlightthickness=0)
        self.canvas.pack()
        
        # Store image references to prevent garbage collection
        self.images = []
        self.jumpscare_image = None
        
        # Load sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load sound files from sounds folder"""
        sounds_folder = os.path.join(os.path.dirname(__file__), 'sounds')
        
        # Create folder if it doesn't exist
        if not os.path.exists(sounds_folder):
            os.makedirs(sounds_folder)
            print(f"Please add sound files to: {sounds_folder}")
        
        # Load sound files
        self.background_sound = None
        self.ghost_sound = None
        self.jumpscare_sound = None
        self.keyboard_sound = None
        
        # Try to load background music (for ghost phase)
        bg_path = os.path.join(sounds_folder, 'background.mp3')
        if os.path.exists(bg_path):
            try:
                self.background_sound = bg_path
                print("Loaded background.mp3")
            except Exception as e:
                print(f"Error loading background sound: {e}")
        
        # Try to load ghost appearance sound
        ghost_path = os.path.join(sounds_folder, 'ghost.mp3')
        if os.path.exists(ghost_path):
            try:
                self.ghost_sound = pygame.mixer.Sound(ghost_path)
                print("Loaded ghost.mp3")
            except Exception as e:
                print(f"Error loading ghost sound: {e}")
        
        # Try to load jumpscare sound
        jumpscare_path = os.path.join(sounds_folder, 'jumpscare.mp3')
        if os.path.exists(jumpscare_path):
            try:
                self.jumpscare_sound = pygame.mixer.Sound(jumpscare_path)
                print("Loaded jumpscare.mp3")
            except Exception as e:
                print(f"Error loading jumpscare sound: {e}")
        
        # Try to load keyboard sound
        keyboard_path = os.path.join(sounds_folder, 'keyboard.mp3')
        if os.path.exists(keyboard_path):
            try:
                self.keyboard_sound = pygame.mixer.Sound(keyboard_path)
                print("Loaded keyboard.mp3")
            except Exception as e:
                print(f"Error loading keyboard sound: {e}")
    
    def play_sound(self, sound_type):
        """Play a specific sound"""
        try:
            if sound_type == 'background' and self.background_sound:
                pygame.mixer.music.load(self.background_sound)
                pygame.mixer.music.play(-1)  # Loop indefinitely
            elif sound_type == 'ghost' and self.ghost_sound:
                self.ghost_sound.play()
            elif sound_type == 'jumpscare' and self.jumpscare_sound:
                self.jumpscare_sound.play()
            elif sound_type == 'keyboard' and self.keyboard_sound:
                self.keyboard_sound.play()
        except Exception as e:
            print(f"Error playing sound: {e}")
    
    def stop_sound(self):
        """Stop all sounds"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Error stopping sound: {e}")
    
    def exit_program(self):
        """Safely exit the program"""
        if self.should_exit:
            return  # Already exiting
        self.should_exit = True
        self.stop_sound()
        try:
            pygame.quit()
        except:
            pass
        self.root.quit()
    
    def check_for_escape(self):
        """Check if escape key is pressed using pygame"""
        if self.should_exit:
            return True
        
        # Periodically reclaim focus to ensure ESC works
        try:
            if not self.root.focus_get():
                self.root.focus_force()
        except:
            pass
        
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.exit_program()
                    return True
        except:
            pass
        return False
        
    def load_jumpscare_image(self):
        """Load jumpscare image from ghost_images folder"""
        # Look for jumpscare.jpg in the ghost_images folder
        jumpscare_path = os.path.join(os.path.dirname(__file__), 'ghost_images', 'jumpscare.jpg')
        
        if os.path.exists(jumpscare_path):
            try:
                img = Image.open(jumpscare_path)
                img = img.resize((self.screen_width, self.screen_height), 
                               Image.Resampling.LANCZOS)
                self.jumpscare_image = ImageTk.PhotoImage(img)
                return True
            except Exception as e:
                print(f"Error loading jumpscare image: {e}")
                return False
        return False
    
    def show_jumpscare(self):
        """Display jumpscare image and wait for sound to finish"""
        # Temporarily disable click-through for jumpscare
        self.root.wm_attributes('-disabled', False)
        
        # Play jumpscare sound
        self.play_sound('jumpscare')
        
        self.canvas.delete('all')
        
        # Try to load and show actual jumpscare image
        if self.load_jumpscare_image() and self.jumpscare_image:
            self.canvas.configure(bg='black')
            self.canvas.create_image(
                self.screen_width // 2,
                self.screen_height // 2,
                image=self.jumpscare_image
            )
        else:
            # Fallback: Create a scary red screen with text
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
            # Keep checking if sound is still playing
            while pygame.mixer.get_busy():
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
        
        self.canvas.delete('all')
    
    def show_black_screen_with_blink(self):
        """Show black screen that blinks continuously, then stays for 3 seconds"""
        self.root.wm_attributes('-disabled', False)
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        self.root.update()
        
        # Blink continuously (no time limit)
        is_black = True  # Start with black display
        blink_count = 0
        max_blinks = 8  # Number of blinks before stopping
        
        while blink_count < max_blinks:
            if self.check_for_escape() or self.should_exit:
                return
            
            # Toggle between two nearly-black shades to avoid white flashes
            if is_black:
                self.canvas.configure(bg='black')
            else:
                self.canvas.configure(bg='#050505')
            
            is_black = not is_black
            self.root.update()
            time.sleep(1.0)  # Slower blink speed (1 second per change)
            blink_count += 1
        
        # Stay black for 3 seconds
        self.canvas.configure(bg='black')
        self.root.update()
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
            self.root.update()
    
    def show_haunted_notepad(self):
        """Show notepad appearing with random letters, then typing a message"""
        import subprocess
        import pyautogui
        
        # Open notepad
        notepad = subprocess.Popen(['notepad.exe'])
        time.sleep(1)  # Wait for notepad to open

        font_height = -18
        subprocess.run([
            "reg", "add", "HKCU\\Software\\Microsoft\\Notepad",
            "/v", "lfHeight",
            "/t", "REG_DWORD",
            "/d", str(font_height),
            "/f"
        ])
        
        # Phase 1: Type extremely long random letters (slow to fast)
        # Load text from random.txt file
        random_txt_path = os.path.join(os.path.dirname(__file__), 'random.txt')
        
        try:
            with open(random_txt_path, 'r', encoding='utf-8') as f:
                random_text = f.read()
            print(f"Loaded random.txt with {len(random_text)} characters")
        except FileNotFoundError:
            print("random.txt not found, using fallback random text")
            random_text = 'abcdefghijklmnopqrstuvwxyz' * 50  # Fallback
        
        # Keep line breaks from the file for proper line formatting
        # Type each character from random.txt with speed based on position
        total_chars = len(random_text)
        
        for i, char in enumerate(random_text):
            if self.check_for_escape() or self.should_exit:
                notepad.terminate()
                return
            
            # Type character from random.txt (including line breaks)
            if char == '\n':
                pyautogui.press('enter')
            else:
                pyautogui.write(char, interval=0)
            self.play_sound('keyboard')  # Play keyboard sound
            
            # Slow for first 10 characters, then fast
            if i < 10:
                delay = 0.3  # Slow for first 10 characters
            else:
                delay = 0.01  # Fast for the rest
            time.sleep(delay)
        
        # Phase 2: Wait 3 seconds
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                notepad.terminate()
                return
            time.sleep(0.1)
        
        # Phase 3: Go to new line and type the message in bold
        pyautogui.press('enter')  # New line
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'b')  # Bold (if supported, may not work in Notepad)
        time.sleep(0.2)
        
        message = "DO NOT LOOK BACK"
        for char in message:
            if self.check_for_escape() or self.should_exit:
                notepad.terminate()
                return
            pyautogui.write(char, interval=0)
            self.play_sound('keyboard')  # Play keyboard sound
            time.sleep(0.3)  # Slow typing
        
        # Close notepad without saving
        notepad.terminate()
        time.sleep(0.5)
        
        # Phase 4: Show black screen for 3 seconds after closing notepad
        self.root.wm_attributes('-disabled', False)  # Make window visible
        self.root.attributes('-alpha', 1.0)  # Make fully opaque
        self.canvas.delete('all')
        self.canvas.configure(bg='#050505')  # Near-black so transparentcolor doesn't hide it
        self.root.update()
        
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
            self.root.update()
    
    def show_thank_you(self):
        """Display thank you message box"""
        self.root.withdraw()  # Hide main window
        messagebox.showinfo("Thank You", "Thank you for executing!")
        self.root.quit()
    
    def run(self):
        """Main program flow"""
        # Start background music at the beginning
        self.play_sound('background')
        
        # Step 1: Wait 5 seconds
        print("Waiting 5 seconds...")
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
        
        # Step 2: Black screen blinks for 5 seconds, then stays for 3 seconds
        print("Black screen sequence...")
        self.show_black_screen_with_blink()
        if self.should_exit:
            return
        
        # Step 3: Notepad appears with random letters and message
        print("Notepad sequence...")
        self.show_haunted_notepad()
        if self.should_exit:
            return
        
        # Step 4: Show jumpscare
        print("Jumpscare!")
        self.show_jumpscare()
        if self.should_exit:
            return
        
        # Step 5: Stop all music, clear screen, and show thank you message
        self.stop_sound()
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        self.show_thank_you()

if __name__ == "__main__":
    print("=" * 60)
    print("HAUNTED WINDOW PROGRAM")
    print("=" * 60)
    print("\n⚠️  TO EXIT THE PROGRAM:")
    print("   Option 1: Press ESC key (works best if you don't click away)")
    print("   Option 2: Close this terminal window")
    print("   Option 3: Press Ctrl+C in this terminal")
    print("\n🎃 Starting haunted experience...\n")
    print("=" * 60)
    
    app = HauntedWindow()
    app.run()
