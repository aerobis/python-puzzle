import cv2
import tkinter as tk
import customtkinter as ctk

from tkinter import filedialog
from tkinter import messagebox
from image_processor import ImageProcessor
from puzzle import Puzzle
from gameplay import GameplayManager
from scoreboard import Scoreboard

class PuzzleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Puzzle Game")
        self.root.geometry("1100x760")
        self.root.minsize(950, 700)
        # Shared display size for the original and puzzle images.
# Keeping this in one place also keeps mouse coordinates,
# hints and grid lines aligned with the displayed puzzle.
        self.canvas_size = 480



        self.current_image = None
        self.current_tiles = []
        self.hints_used = 0
        self.hinted_tiles = set()

        self.image_processor = None
        self.puzzle = None
        self.gameplay = None

        self.scoreboard = Scoreboard()
        self.score_saved = False

        # Background Colour
        self.root.config(bg = "#10072B")
        # Scrollable main area
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color="#10072B"
        )

        self.main_frame.pack(
            fill="both",
            expand=True
        )

        # Game Heading
        self.heading = tk.Label(
            self.main_frame, 
            text = "IMAGE PUZZLE GAME",
            font = ("Arial", 38, "bold"),
            fg = "#ffffff",
            bg = "#10072B"
        )
        self.heading.pack(pady = (25, 5))

        # Game Subtitle
        self.subtitle = tk.Label(
        self.main_frame,
        text="Swap, Rotate & Flip Your Way to Victory!",
        font=("Didot", 14, "italic"),
        fg="#DCC8F5",
        bg="#10072B"
    )
        self.subtitle.pack(pady=(0, 25))
        self.setup_layout()
        
# Function To Select An Image
    def load_image(self):
    
        file_path = filedialog.askopenfilename(
            title = "Select an Image",
            filetypes = [
                ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
            ]
            )
        if file_path:
            print("Selected Image:", file_path)
            print("Selected Grid Size:", self.grid_size.get())

            # Load and resize the image using OpenCV
            size = int(self.grid_size.get()[0])

            try:
                self.image_processor = ImageProcessor(file_path, size)
                self.current_image = self.image_processor.get_original_image()

            except Exception:
                messagebox.showerror(
            "Image Error",
            "The selected file could not be loaded as an image."
                )
                return
            self.current_image = self.image_processor.get_original_image()

            tiles = self.image_processor.get_tile_images()
            print("Number of Tiles:", len(tiles))

            self.puzzle = Puzzle(tiles, size)
            self.current_tiles = self.puzzle.tiles

            self.gameplay = GameplayManager(self.difficulty.get(), size)
            self.gameplay.configure_puzzle(self.puzzle)
            self.score_saved = False
            if self.difficulty.get() == "Medium":
                self.update_timer()

            if self.difficulty.get() == "Hard":
                self.set_moves_left(str(self.gameplay.get_moves_left()))

            self.tiles_left_var.set(str(self.puzzle.incorrect_count()))
            self.moves_var.set("0")

            self.hints_used = 0
            self.hinted_tiles.clear()
            self.hints_var.set("3")
            print("Tiles Shuffled Successfully!")

            self.display_tiles(self.current_tiles)

            # Covert The Image for Tkinter
            photo = tk.PhotoImage(
                data = self.image_processor.to_png_bytes(self.current_image)
            )

            # Display The Original image
            self.original_hint_canvas.delete("all")
            self.original_hint_canvas.create_image(
                0, 0,
                anchor = "nw",
                image = photo
            )
            self.original_hint_canvas.image = photo

            # Enable The Hint Button
            self.hint_button.configure(state = "normal", text = "Hint (0/3)")

            # Enable The Solve Button
            self.solve_button.configure(state = "normal")

    # Display Shuffled Tiles On The Puzzle Canvas
    def display_tiles(self, tiles):
        size = int(self.grid_size.get()[0])

        self.puzzle_canvas.delete("all")
        self.puzzle_canvas.tiles = []

        index = 0

        for row in range(size):
            for col in range(size):

                # Calculate Each Tile's Position
                x = round(col * self.canvas_size / size)
                y = round(row * self.canvas_size / size)

                # Convert The Tile For Tkinter
                tile = tiles[index]
                tile_photo = tk.PhotoImage(
                    data = self.image_processor.to_png_bytes(tile.image)
                )

                # Keep The Image In Memory
                self.puzzle_canvas.tiles.append(tile_photo)

                # Display The Tile
                self.puzzle_canvas.create_image(
                    x, y,
                    anchor = "nw",
                    image = tile_photo,
                )

                index +=1

        self.draw_grid()
        self.show_correct_tiles()


    # Update The Puzzle When The Grid Size Changes
    def change_grid(self):
        if self.image_processor is not None:
            size = int(self.grid_size.get()[0])
            self.image_processor.grid_size = size

            tiles = self.image_processor.get_tile_images()
            self.puzzle = Puzzle(tiles, size)
            self.current_tiles = self.puzzle.tiles

            self.gameplay = GameplayManager(self.difficulty.get(), size)
            self.gameplay.configure_puzzle(self.puzzle)
            self.score_saved = False

            if self.difficulty.get() == "Medium":
                self.update_timer()

            if self.difficulty.get() == "Hard":
                self.set_moves_left(str(self.gameplay.get_moves_left()))

            self.tiles_left_var.set(str(self.puzzle.incorrect_count()))
            self.moves_var.set("0")

            self.hints_used = 0
            self.hinted_tiles.clear()
            self.hints_var.set("3")

            self.display_tiles(self.current_tiles)

            self.original_hint_canvas.delete("hint")
            self.hint_button.configure(
                state = "normal", 
                text = "Hint (0/3)"
            )

            # Enable The Solve Button
            self.solve_button.configure(state = "normal")
        else:
            self.draw_grid()

    # Show A Hint An Inccorrect Tile
    def show_hint(self):
        if self.hints_used >= 3 or not self.current_tiles:
            return

        size = int(self.grid_size.get()[0])

        # Find A Tile In The Wrong Position
        target = self.gameplay.get_hint(self.puzzle)
        if target is None:
            return

        index, tile_id = target
        self.hinted_tiles.add(tile_id)

        # Remove Previous Hint Circles
        self.puzzle_canvas.delete("hint")
        self.original_hint_canvas.delete("hint")

        # Cicle On The Shuffled Tile
        col = index % size
        row = index // size

        x = (col + 0.5) * self.canvas_size / size
        y = (row + 0.5) * self.canvas_size / size

        radius = 15

        self.puzzle_canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            outline = "#2196F3",
            width = 3,
            tags = "hint"
        )

        # Circle On The Tile's Correct Position
        home_col = tile_id % size
        home_row = tile_id // size

        home_x = (home_col + 0.5) * self.canvas_size / size
        home_y = (home_row + 0.5) * self.canvas_size / size

        self.original_hint_canvas.create_oval(
            home_x - radius, home_y - radius,
            home_x + radius, home_y + radius,
            outline = "#2196F3",
            width = 3,
            tags = "hint"
        )

        self.hints_used = 3 - self.gameplay.get_hints_left()
        self.hints_var.set(str(self.gameplay.get_hints_left()))

        self.hint_button.configure(text = f"Hint ({self.hints_used}/3)")

        if self.hints_used >= 3:
            self.hint_button.configure(state = "disabled")


    # HELPER FUNCTIONS
    def _tile_from_event(self, event):
        # If the registered click is beyond the scope of the canvas
        if not(0 <= event.x < self.canvas_size and 0 <= event.y <= self.canvas_size):
            return None
        size = int(self.grid_size.get()[0])
        col = int(event.x * size / self.canvas_size)
        row = int (event.y * size / self.canvas_size)
        return row * size + col
    
    def _after_move(self):
        self.gameplay.selected_tile = None
        self.puzzle_canvas.delete("selection")
        self.current_tiles = self.puzzle.tiles
        self.display_tiles(self.current_tiles)
        self.clear_hints()
        self.set_moves(self.gameplay.get_moves())
        self.set_tiles_left(self.gameplay.get_tiles_left(self.puzzle))
        if self.difficulty.get() == "Hard":
            self.set_moves_left(str(self.gameplay.get_moves_left()))
        if self.puzzle.is_solved():
            self.gameplay.game_finished = True
            self.save_game_result()
            self.hint_button.configure(state="disabled")
            self.solve_button.configure(state="disabled")
            self.root.after(100, lambda: messagebox.showinfo(
                "Puzzle Completed!",
                "Congratulations! You solved the puzzle!"))
            return
        self.check_hard_game_over()
    
    def _draw_selection(self):
        self.puzzle_canvas.delete("selection")
        selected = self.gameplay.get_selected_tile()
        if selected is None:
            return
        size = int(self.grid_size.get()[0])
        tile_size = self.canvas_size / size
        row, col = divmod(selected, size)
        x1 = col * tile_size
        y1 = row * tile_size
        self.puzzle_canvas.create_rectangle(
            x1, y1, x1 + tile_size, y1 + tile_size,
            outline = "#DC0FE3", width = "4", tags = "selection"
        )

    # Flip A Puzzle Tile
    def on_tile_flip(self, event):
        if self.puzzle is None or self.gameplay is None:
            return
        tile_index = self._tile_from_event(event)
        if tile_index is None:
            return
        if self.gameplay.handle_flip(self.puzzle, tile_index):
            self._after_move()

    # Rotates A Puzzle Tile
    def on_tile_rotate(self, event):
        if self.puzzle is None or self.gameplay is None:
            return
        tile_index = self._tile_from_event(event)
        if tile_index is None:
            return
        if self.gameplay.handle_rotate(self.puzzle, tile_index):
            self._after_move()

    # Detect Which Puzzle Tile Is Clicked
    def on_tile_click(self, event):
        if self.puzzle is None or self.gameplay is None:
            return
        if not self.gameplay.can_make_move():
            return
        tile_index = self._tile_from_event(event)
        if tile_index is None:
            return

        selected = self.gameplay.get_selected_tile()
        if selected is None or selected == tile_index:
            self.gameplay.select_tile(tile_index)   # select, or deselect on second click
        elif self.gameplay.handle_swap(self.puzzle, selected, tile_index):
            self._after_move()
            return
        self._draw_selection()

    # Show Green Ticks On Correct Tiles
    def show_correct_tiles(self):
        if self.puzzle is None:
            return

        self.puzzle_canvas.delete("correct")

        size = int(self.grid_size.get()[0])
        tile_size = self.canvas_size / size

        for index in range(size * size):
            if self.puzzle.is_correct(index):
                row = index // size
                col = index % size

                x = (col + 0.85) * tile_size
                y = (row + 0.15) * tile_size

                self.puzzle_canvas.create_text(
                    x, y,
                    text = "✓",
                    fill = "#01FF7C",
                    font = ("Arial", 22, "bold"),
                    tag = "correct"
                )

    # Remove Hint Circles after a move
    def clear_hints(self):
        self.puzzle_canvas.delete("hint")
        self.original_hint_canvas.delete("hint")
           # Save The Result When The Player Solves The Puzzle
    def save_game_result(self):
        if self.gameplay is None or self.score_saved:
            return

        difficulty = self.difficulty.get()
        grid_size = self.grid_size.get()

        if difficulty == "Easy":
            result = {
                "moves": self.gameplay.get_moves()
            }

        elif difficulty == "Medium":
            time_left = self.gameplay.get_time_left()

            if time_left is None:
                return

            result = {
                "time_left": int(time_left),
                "moves": self.gameplay.get_moves()
            }

        elif difficulty == "Hard":
            result = {
                "moves_left": self.gameplay.get_moves_left(),
                "moves_used": self.gameplay.get_moves()
            }

        else:
            return

        self.scoreboard.save_score(
            difficulty,
            grid_size,
            result
        )

        self.score_saved = True
        # Check If Hard Mode Has Run Out Of Moves
    def check_hard_game_over(self):
        if self.gameplay is None or self.puzzle is None:
            return False

        if self.gameplay.difficulty != "Hard":
            return False

        if (
            self.gameplay.get_moves_left() == 0
            and not self.puzzle.is_solved()
        ):
            self.gameplay.game_finished = True

            self.hint_button.configure(state="disabled")
            self.solve_button.configure(state="disabled")

            self.root.after(
                100,
                lambda: messagebox.showinfo(
                    "Game Over",
                    "You have run out of moves! Try again."
                )
            )

            return True

        return False


    # Solve The Puzzle
    def solve_puzzle(self):
        if self.puzzle is None:
            return
    
        # Restore All Tiles To Their Original Position
        self.gameplay.solve_puzzle(self.puzzle)

        self.gameplay.moves = 0
        self.moves_var.set("0")

        self.current_tiles = self.puzzle.tiles
        self.tiles_left_var.set("0")

        # Display the completed puzzle
        self.display_tiles(self.current_tiles)

        # Remove The Circles
        self.original_hint_canvas.delete("hint")
        self.puzzle_canvas.delete("hint")

        # Disable The Buttons After Solving
        self.hint_button.configure(
            text = "Hint (0/3)",
            state = "disabled"
        )
        self.solve_button.configure(state = "disabled")
    # Open The Scoreboard Window
        # Open The Scoreboard Window - Himanshu Part
    def show_scoreboard(self):
        scores = self.scoreboard.load_scores()

        window = tk.Toplevel(self.root)
        window.title("Scoreboard")
        window.geometry("650x500")
        window.configure(bg="#10072B")

        title = tk.Label(
            window,
            text="SCOREBOARD",
            font=("Arial", 26, "bold"),
            fg="#FFFFFF",
            bg="#10072B"
        )
        title.pack(pady=(20, 10))

        # Difficulty buttons
        difficulty_frame = tk.Frame(
            window,
            bg="#10072B"
        )
        difficulty_frame.pack(pady=5)

        # Area where scores are displayed
        score_frame = tk.Frame(
            window,
            bg="#10072B"
        )
        score_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        # Display scores for selected difficulty
        def display_scores(difficulty):

            # Clear previous scores
            for widget in score_frame.winfo_children():
                widget.destroy()

            filtered = [
                score for score in scores
                if score["difficulty"] == difficulty
            ]

            # Easy - lower moves are better
            if difficulty == "Easy":
                filtered.sort(
                    key=lambda score:
                    score["result"].get("moves", 999999)
                )

            # Medium - more remaining time is better
            elif difficulty == "Medium":
                filtered.sort(
                    key=lambda score:
                    score["result"].get("time_left", 0),
                    reverse=True
                )

            # Hard - more remaining moves are better
            elif difficulty == "Hard":
                filtered.sort(
                    key=lambda score:
                    score["result"].get("moves_left", 0),
                    reverse=True
                )

            heading = tk.Label(
                score_frame,
                text=f"{difficulty} Scores",
                font=("Arial", 18, "bold"),
                fg="#DC0FE3",
                bg="#10072B"
            )
            heading.pack(pady=(5, 10))

            # No saved scores yet
            if not filtered:
                no_scores = tk.Label(
                    score_frame,
                    text="No scores yet.",
                    font=("Arial", 14),
                    fg="#DCC8F5",
                    bg="#10072B"
                )
                no_scores.pack()
                return

            # Display up to 10 results
            for position, score in enumerate(
                filtered[:10],
                start=1
            ):
                grid = score["grid_size"]
                result = score["result"]

                if difficulty == "Easy":
                    result_text = (
                        f'{result.get("moves", 0)} moves'
                    )

                elif difficulty == "Medium":
                    seconds = result.get("time_left", 0)
                    minutes, seconds = divmod(
                        int(seconds),
                        60
                    )

                    result_text = (
                        f"{minutes:02d}:{seconds:02d} remaining"
                    )

                else:
                    result_text = (
                        f'{result.get("moves_left", 0)} '
                        f'moves left'
                    )

                row_text = (
                    f"{position}.  "
                    f"{grid}  |  "
                    f"{result_text}"
                )

                score_label = tk.Label(
                    score_frame,
                    text=row_text,
                    font=("Arial", 14),
                    fg="#FFFFFF",
                    bg="#10072B"
                )
                score_label.pack(pady=4)

        # Difficulty selection buttons
        for difficulty in ("Easy", "Medium", "Hard"):
            button = ctk.CTkButton(
                difficulty_frame,
                text=difficulty,
                width=120,
                command=lambda d=difficulty: display_scores(d)
            )
            button.pack(
                side="left",
                padx=5
            )

        # Easy scoreboard is shown first
        display_scores("Easy")

    def setup_layout(self):
        # Top Left Row
        self.top_frame = tk.Frame(
            self.main_frame,
            bg = "#10072B")
        self.top_frame.pack(pady = 10)

        # Frame for Difficulty and Grid Size Slectors
        self.selector_frame = tk.Frame(self.top_frame, 
                                bg ="#10072B")
        self.selector_frame.pack(side = "left")

        # Difficulty Box
        self.difficulty_box = ctk.CTkFrame(
            self.selector_frame,
            fg_color = "#DCC8F5",
            bg_color = "#10072B",
            border_color = "#8A2BE2",
            border_width = 2.5,
            corner_radius = 15,
            width = 233,
            height = 85,
   )
        self.difficulty_box.pack(side = "left", padx = (10, 10))
        self.difficulty_box.pack_propagate(False)

        # Grid Size Box
        self.grid_box = ctk.CTkFrame(
            self.selector_frame,
            fg_color = "#DCC8F5",
            bg_color = "#10072B",
            border_color = "#8A2BE2",
            border_width = 2.5,
            corner_radius = 15,
            width = 233,
            height = 85,
        )
        self.grid_box.pack(side = "left", padx = (10, 0))
        self.grid_box.pack_propagate(False)

        # Difficulty Selection
        self.difficulty = tk.StringVar(value = "Easy")

        difficulty_label = tk.Label(
            self.difficulty_box,
            text = "Select Difficulty:",
            font = ("Didot", 16, "bold"),
            fg = "#DC0FE3",
            bg = "#DCC8F5"
        )
        difficulty_label.pack(pady = (12, 5))

        difficulty_menu = tk.OptionMenu(
            self.difficulty_box,
            self.difficulty,
            "Easy", "Medium","Hard"
        )

        difficulty_menu.config(
            font = ("Didot", 14),
            fg = "#10072B",
            bg ="#DCC8F5",
            width = 6
        )
        difficulty_menu.pack(pady = 0)

        difficulty_menu["menu"].config(
            font = ("Didot", 14),
            fg = "#10072B",
        )

        # Grid Size Selection
        self.grid_size = tk.StringVar(value="3x3")

        grid_label = tk.Label(
            self.grid_box,
            text = "Select Grid Size:",
            font = ("Didot", 16, "bold"),
            fg = "#DC0FE3",
            bg = "#DCC8F5"
        )
        grid_label.pack(pady = (12, 5))

        grid_menu = tk.OptionMenu(
            self.grid_box, 
            self.grid_size, 
            "3x3", "4x4", "5x5",
            command = lambda _: self.change_grid()
        )

        grid_menu.config(
            font = ("Didot", 14,),
            fg = "#10072B",
            bg = "#DCC8F5",
            width = 3,
            relief = "flat",
            highlightthickness = 0
        )

        grid_menu["menu"].config(
            font = ("Didot", 14),
            fg = "#10072B",
        )
        grid_menu.pack(pady = 0)

        # Progress Display
        self.progress_frame = ctk.CTkFrame(
            self.top_frame,
            fg_color = "#DCC8F5",
            bg_color = "#10072B",
            border_color = "#8A2BE2",
            border_width = 2.5,
            corner_radius = 15,
            width = 486,
            height = 85,
        )
        self.progress_frame.pack(side = "left", padx = (30, 0))
        self.progress_frame.grid_propagate(False)
        for col in (0, 2, 4, 6):
            self.progress_frame.grid_columnconfigure(col, weight = 1)
        self.progress.frame.grid_rowconfigure(0, weight = 1)

        # Top Right Row
        # Progress Value
        self.moves_var = tk.StringVar(value = "0")
        self.tiles_left_var = tk.StringVar(value = "0")
        self.hints_var = tk.StringVar(value = "3")
        self.time_left_var = tk.StringVar(value = "--:--")
        self.moves_left_var = tk.StringVar(value = "--")

        # Function to Create Progress Labels 
        def add_progress_label(parent, title, variable, column):
            section = ctk.CTkFrame(
                parent, 
                fg_color = "#DCC8F5",
            )

            section.grid(row = 0, column = column, padx = 10, pady = 8)

            ctk.CTkLabel(
                section,
                text = title,
                font = ("Didot", 16, "bold"),
                text_color = "#DC0FE3",
                bg_color = "#DCC8F5"
            ).pack()

            ctk.CTkLabel(
                section,
                textvariable = variable,
                font = ("Didot", 20, "bold"),
                text_color = "#10072B",
                bg_color = "#DCC8F5"
            ).pack()

            return section

        # Function to Create Dividers
        def add_divider(parent, column):
            divider = ctk.CTkFrame(
                parent,
                fg_color = "#8A2BE2",
                width = 1,
                height = 45,
            )
            divider.grid(row = 0, column = column, padx = 0, pady = 15)
            return divider

        self.moves_section = add_progress_label(
            self.progress_frame, "Moves", self.moves_var, 0)

        self.tiles_section = add_progress_label(
            self.progress_frame, "Tiles Left", self.tiles_left_var, 2)

        self.hints_section = add_progress_label(
            self.progress_frame, "Hints", self.hints_var, 4)

        self.time_section = add_progress_label(
            self.progress_frame, "Time Left", self.time_left_var, 6)

        self.moves_left_section = add_progress_label(
            self.progress_frame, "Moves Left", self.moves_left_var, 6)

        add_divider(self.progress_frame, 1)
        add_divider(self.progress_frame, 3)
        self.last_divider = add_divider(self.progress_frame, 5)

        # Update Progress Display Based on Difficulty
        def update_progress_display(*args):
            self.time_section.grid_remove()
            self.moves_left_section.grid_remove()

            if self.difficulty.get() == "Medium":
                self.time_section.grid()
            elif self.difficulty.get() == "Hard":
                self.moves_left_section.grid()

        self.difficulty.trace_add("write", update_progress_display)
        self.difficulty.trace_add("write", lambda *args: self.change_grid())
        update_progress_display()

        # Frame To Hold Both Images
        self.image_frame = tk.Frame(self.main_frame)
        self.image_frame.pack(pady = 0)
        self.image_frame.config(
            bg = "#10072B"
        )

        # Original Image On The Left
        self.left_frame = tk.Frame(self.image_frame)
        self.left_frame.pack(side = "left", padx = 15, anchor = "n" )
        self.left_frame.config(
            bg = "#10072B"
        )

        # Original Image Heading
        original_heading = tk.Label(
            self.left_frame, text = "Original Image",
            font = ("Didot", 24, "bold"),
            fg = "#ffffff",
            bg = "#10072B",
        )
        original_heading.pack(anchor = "w", padx = 0, pady = 15)

        # Original Image Container
        self.original_container = tk.Frame(
            self.left_frame, 
            width = 490, 
            height = 490, 
            bg = "#F4E8FF",
            highlightbackground = "#8A2BE2",
            highlightthickness = 5,
            highlightcolor = "#8A2BE2"
        )
        self.original_container.pack()
        self.original_container.pack_propagate(False)

        # Original Image Display
        self.original_hint_canvas = tk.Canvas(
            self.original_container,
            width = 486,
            height = 486,
            bg = "#F4E8FF",
            highlightthickness = 0,
            borderwidth = 0,
        )
        self.original_hint_canvas.pack()

        # Upoad Image button
        self.load_button = ctk.CTkButton(
            self.left_frame,
            text = "Upload Image (JPG, PNG, BMP)",
            command = self.load_image,
            font = ("Arial", 16, "bold"),
            text_color = "#8A2BE2",
            fg_color = "#F4E8FF",
            border_width = 2,
            border_color = "#F4E8FF",
            hover_color = "#DC0FE3",
            width = self.canvas_size,
            height = 50 
        )
        self.load_button.pack(pady = (25, 0))

        # Puzzle Image Frame On The Right
        self.right_frame = tk.Frame(self.image_frame)
        self.right_frame.pack(side = "right", 
                        padx = 15, 
                        anchor = "n")
        self.right_frame.config(
            bg = "#10072B"
        )

        # Puzzle Image Heading
        self.puzzle_heading = tk.Label(
            self.right_frame, text = "Puzzle Image",
            font = ("Didot", 24, "bold"),
            fg = "#ffffff",
            bg = "#10072B",
        )
        self.puzzle_heading.pack(anchor = "w", padx = 0, pady = 15)

        # Puzzle Canvas
        self.puzzle_canvas = tk.Canvas(
            self.right_frame,
            width = self.canvas_size, 
            height = self.canvas_size,
            bg = "#F4E8FF",
            highlightbackground = "#8A2BE2",
            highlightthickness = 5,
            highlightcolor = "#8A2BE2",
        )
        self.puzzle_canvas.pack()

        self.puzzle_canvas.bind("<Button-1>", self.on_tile_click)
        self.puzzle_canvas.bind("<Button-3>", self.on_tile_rotate)
        self.puzzle_canvas.bind("<Button-2>", self.on_tile_rotate);
        self.puzzle_canvas.bind("<Control-Button-1>", self.on_tile_rotate)
        self.puzzle_canvas.bind("<Shift-Button-1>", self.on_tile_flip)

        self.draw_grid()

        # Hint and Solve Buttons
        self.button_frame = tk.Frame(
            self.right_frame,
            bg = "#10072B"
        )
        self.button_frame.pack(pady=(25, 0))

        self.hint_button = ctk.CTkButton(
            self.button_frame,
            text = "Hint (0/3)",
            command = self.show_hint,
            state = "disabled",
            font = ("Arial", 16, "bold"),
            text_color = "#8A2BE2",
            fg_color = "#F4E8FF",
            border_width = 2,
            border_color = "#F4E8FF",
            hover_color = "#DC0FE3",
            width = 233,
            height = 50
        )
        self.hint_button.pack(side = "left", padx = 10)

        self.solve_button = ctk.CTkButton(
            self.button_frame,
            text = "Solve",
            command = self.solve_puzzle,
            state = "disabled",
            font = ("Arial", 16, "bold"),
            text_color = "#DCC8F5",
            fg_color = "#8A2BE2",
            hover_color = "#DC0FE3",
            width = 233,
            height = 50
        )
        self.solve_button.pack(side = "right", padx = 10)


        # Scoreboard Button - Himanshu Part
        self.scoreboard_button = ctk.CTkButton(
            self.right_frame,
            text = "Scoreboard",
            command = self.show_scoreboard,
            font = ("Arial", 16, "bold"),
            text_color = "#DCC8F5",
            fg_color = "#8A2BE2",
            hover_color = "#DC0FE3",
            width = 233,
            height = 50
        )

        self.scoreboard_button.pack(pady = (15, 0))

        # How to Play Instructions
        self.instructions_label = tk.Label(
        self.main_frame,
            text="Left-click: Swap  |  Right-click: Rotate  |  Shift + click: Flip  |  Mac: Control + click to rotate",
            font=("Arial", 11),
            fg="#DCC8F5",
            bg="#10072B"
        )
        self.instructions_label.pack(pady=(15, 0))

#Draw Faint Grid Lines
    def draw_grid(self):
        self.puzzle_canvas.delete("grid")
        size = int(self.grid_size.get()[0])
        tile_size = self.canvas_size / size

        for i in range(1, size):
            position = i * tile_size

            self.puzzle_canvas.create_line(position, 0, position, self.canvas_size, 
                                            fill="#C9B8E8", width=1, tags="grid")

            self.puzzle_canvas.create_line(0, position, self.canvas_size, position,
                                                fill="#C9B8E8", width=1, tags="grid")

    def set_moves(self, value):
        self.moves_var.set(str(value))

    def set_tiles_left(self, value):
        self.tiles_left_var.set(str(value))

    def set_hints(self, value):
        self.hints_var.set(str(value))

    # Update The Countdown Timer
    def update_timer(self, game=None):
        if game is None:
            game = self.gameplay

        if game is None or game is not self.gameplay:
            return

        if game.difficulty != "Medium":
            return

        if game.game_finished:
            return

        seconds = game.get_time_left()

        if seconds is None:
            return

        minutes, remaining_seconds = divmod(max(0, int(seconds)), 60)
        self.set_time_left(f"{minutes:02d}:{remaining_seconds:02d}")

        if seconds > 0:
            self.root.after(1000, lambda: self.update_timer(game))
        else:
            game.game_finished = True
            self.hint_button.configure(state="disabled")
            self.solve_button.configure(state="disabled")
            messagebox.showinfo("Time's Up", "You ran out of time!")

    def set_time_left(self, value):
        self.time_left_var.set(value)

    def set_moves_left(self, value):
        self.moves_left_var.set(value)

    def run(self):
        self.root.mainloop()
        
if __name__ == "__main__":
    app = PuzzleGUI()
    app.run()