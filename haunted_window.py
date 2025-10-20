import tkinter as tk
from tkinter import messagebox
import random
import time
from PIL import Image, ImageTk
import os
import pygame  # For sound effects

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
        self.ghost_images = []
        self.ghost_images_original = []  # Store original PIL images for fading
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
        self.should_exit = True
        self.stop_sound()
        pygame.quit()
        self.root.quit()
    
    def check_for_escape(self):
        """Check if escape key is pressed using pygame"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit_program()
                return True
        return False
        
    def show_haunted_text(self):
        """Display 'HAUNTED!!!' in red for 3 seconds"""
        # Temporarily disable click-through for this screen
        self.root.wm_attributes('-disabled', False)
        
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        
        # Create large red text
        self.canvas.create_text(
            self.screen_width // 2,
            self.screen_height // 2,
            text="HAUNTED!!!",
            font=("Arial", 120, "bold"),
            fill="red",
            tags="haunted_text"
        )
        
        self.root.update()
        
        # Wait 3 seconds while checking for escape
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
            self.root.update()
        
        self.canvas.delete('all')
        
        # Re-enable click-through for ghost phase
        self.root.wm_attributes('-disabled', True)
    
    def load_ghost_images(self):
        """Load ghost images from the images folder"""
        images_folder = os.path.join(os.path.dirname(__file__), 'ghost_images')
        
        # Create folder if it doesn't exist
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
            print(f"Please add ghost images to: {images_folder}")
            # Create placeholder images if no images exist
            self.create_placeholder_ghosts()
            return
        
        # Load all image files from the folder
        for filename in os.listdir(images_folder):
            # Skip jumpscare.jpg - it's reserved for the jumpscare only
            if filename.lower() == 'jumpscare.jpg':
                continue
                
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                try:
                    img_path = os.path.join(images_folder, filename)
                    img = Image.open(img_path)
                    # Resize to reasonable size
                    img = img.resize((200, 200), Image.Resampling.LANCZOS)
                    
                    # Convert to RGBA if not already
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    
                    # Store original image for fading
                    self.ghost_images_original.append(img.copy())
                    
                    # Create default translucent version
                    alpha = img.split()[3]
                    alpha = alpha.point(lambda p: int(p * 0.6))
                    img.putalpha(alpha)
                    
                    photo = ImageTk.PhotoImage(img)
                    self.ghost_images.append(photo)
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
        
        # If no images loaded, create placeholders
        if not self.ghost_images:
            self.create_placeholder_ghosts()
    
    def create_ghost_at_opacity(self, image_index, opacity):
        """Create a ghost image at a specific opacity level (0.0 to 1.0)"""
        if image_index >= len(self.ghost_images_original):
            return None
        
        img = self.ghost_images_original[image_index].copy()
        alpha = img.split()[3]
        alpha = alpha.point(lambda p: int(p * opacity))
        img.putalpha(alpha)
        return ImageTk.PhotoImage(img)
    
    def create_placeholder_ghosts(self):
        """Create simple ghost shapes as placeholders"""
        # We'll use text-based ghosts as simple placeholders
        for i in range(5):
            # Create a small canvas for each ghost
            ghost_canvas = tk.Canvas(self.root, width=100, height=100, 
                                    bg='black', highlightthickness=0)
            
            # Draw a simple ghost shape
            ghost_canvas.create_oval(20, 20, 80, 80, fill='white', outline='')
            ghost_canvas.create_text(50, 50, text="👻", font=("Arial", 40))
            
            # Convert to PhotoImage
            ghost_canvas.update()
            self.ghost_images.append("👻")
    
    def show_random_ghosts(self, duration=3):
        """Display random ghost images for specified duration with fade in/out effects"""
        self.canvas.delete('all')
        self.canvas.configure(bg='black')
        
        # Play background music
        self.play_sound('background')
        
        start_time = time.time()
        active_ghosts = []  # Store: (img_id, spawn_time, x, y, image_index, photo_ref)
        fade_duration = 1.0  # Seconds for fade in/out
        
        while time.time() - start_time < duration:
            # Check for escape key
            if self.check_for_escape() or self.should_exit:
                break
                
            current_time = time.time()
            
            # Spawn new ghost randomly
            if random.random() < 0.03:  # 3% chance each iteration (very slow appearance rate)
                x = random.randint(50, self.screen_width - 50)
                y = random.randint(50, self.screen_height - 50)
                
                # Play ghost sound effect
                self.play_sound('ghost')
                
                if self.ghost_images_original:
                    # Use actual image with fade-in
                    image_index = random.randint(0, len(self.ghost_images_original) - 1)
                    # Start with very low opacity
                    photo = self.create_ghost_at_opacity(image_index, 0.01)
                    if photo:
                        img_id = self.canvas.create_image(x, y, image=photo)
                        active_ghosts.append((img_id, current_time, x, y, image_index, photo))
                elif self.ghost_images and isinstance(self.ghost_images[0], str):
                    # Use emoji ghost (no fade for emoji)
                    img_id = self.canvas.create_text(
                        x, y,
                        text=random.choice(self.ghost_images),
                        font=("Arial", random.randint(40, 80)),
                        fill="white"
                    )
                    active_ghosts.append((img_id, current_time, x, y, -1, None))
            
            # Update opacity of all active ghosts
            ghosts_to_remove = []
            for i, (img_id, spawn_time, x, y, image_index, photo_ref) in enumerate(active_ghosts):
                ghost_age = current_time - spawn_time
                ghost_lifetime = random.uniform(3, 5)  # Total lifetime
                
                if ghost_age >= ghost_lifetime:
                    # Ghost is too old, mark for removal
                    ghosts_to_remove.append(i)
                    self.canvas.delete(img_id)
                elif image_index >= 0:  # Only fade real images, not emoji
                    # Calculate opacity based on age
                    if ghost_age < fade_duration:
                        # Fade in
                        opacity = (ghost_age / fade_duration) * 0.6  # Max opacity 0.6
                    elif ghost_age > ghost_lifetime - fade_duration:
                        # Fade out
                        remaining = ghost_lifetime - ghost_age
                        opacity = (remaining / fade_duration) * 0.6
                    else:
                        # Full opacity
                        opacity = 0.6
                    
                    # Update the image with new opacity
                    new_photo = self.create_ghost_at_opacity(image_index, opacity)
                    if new_photo:
                        self.canvas.delete(img_id)
                        new_img_id = self.canvas.create_image(x, y, image=new_photo)
                        active_ghosts[i] = (new_img_id, spawn_time, x, y, image_index, new_photo)
            
            # Remove old ghosts
            for i in reversed(ghosts_to_remove):
                active_ghosts.pop(i)
            
            self.root.update()
            time.sleep(0.05)  # Smooth animation update rate
        
        # Stop background music
        self.stop_sound()
        self.canvas.delete('all')
    
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
        """Display jumpscare image for 3 seconds"""
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
        
        # Wait 3 seconds while checking for escape
        start_time = time.time()
        while time.time() - start_time < 3:
            if self.check_for_escape() or self.should_exit:
                return
            time.sleep(0.1)
            self.root.update()
        
        self.canvas.delete('all')
    
    def show_thank_you(self):
        """Display thank you message box"""
        self.root.withdraw()  # Hide main window
        messagebox.showinfo("Thank You", "Thank you for executing!")
        self.root.quit()
    
    def run(self):
        """Main program flow"""
        # Step 1: Show "HAUNTED!!!" for 3 seconds
        self.show_haunted_text()
        if self.should_exit:
            return
        
        # Step 2: Load and show random ghost images for 3 seconds
        self.load_ghost_images()
        self.show_random_ghosts(duration=30)  # 30 seconds
        if self.should_exit:
            return
        
        # Step 3: Show jumpscare for 3 seconds
        self.show_jumpscare()
        if self.should_exit:
            return
        
        # Step 4: Show thank you message
        self.show_thank_you()

if __name__ == "__main__":
    app = HauntedWindow()
    app.run()
