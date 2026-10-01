import tkinter as tk
import random 
import customtkinter as ctk

from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import ImageOps

root = tk.Tk()
root.title("Image Puzzle Game")
root.geometry("1200x800")
current_image = None 
current_tiles = []
hints_used = 0
hinted_tiles = set()

#Background Colour
root.config(bg = "#10072B")
    
heading = tk.Label(root, 
                   text = "IMAGE PUZZLE GAME",
                   font = ("Arial", 38, "bold"),
                   fg = "#ffffff",
                   bg = "#10072B"
)
heading.pack(pady = (45, 15))

# Function To Select An Image
def load_image():
    global current_image, current_tiles, hints_used
    
    file_path = filedialog.askopenfilename(
        title = "Select an Image",
        filetypes = [
            ("Image Files", "*.jpg *.jpeg *.png *.bmp"),
        ]
    )
    if file_path:
        print("Selected Image:", file_path)
        print("Selected Grid Size:", grid_size.get())

        # Open And Resize The Image
        image = Image.open(file_path)
        image = ImageOps.fit(image, (400, 400))
        current_image = image

        tiles = create_tiles(image)
        print("Number of Tiles:", len(tiles))

        shuffled_tiles = shuffle_tiles(tiles)
        current_tiles = shuffled_tiles
        hints_used = 0
        hinted_tiles.clear()
        print("Tiles Shuffled Successfully!")

        display_tiles(shuffled_tiles)

        # Covert The Image for Tkinter
        photo = ImageTk.PhotoImage(image)

        # Display The Original image
        original_hint_canvas.delete("all")
        original_hint_canvas.create_image(
            0, 0,
            anchor = "nw",
            image = photo
        )
        original_hint_canvas.image = photo

        # Hide The Load Image Button
        load_button.place_forget()

        # Enable The Hint Button
        hint_button.configure(state = "normal", text = "Hint (0/3)")

        # Enable The Solve Button
        solve_button.configure(state = "normal")

# Divide The Image Into Puzzle Tiles
def create_tiles(image):
    size = int(grid_size.get()[0])
    tiles = []

    for row in range(size):
        for col in range(size):
            left = round(col * 400 / size)
            upper = round(row * 400 / size)
            right = round((col + 1) * 400 / size)
            lower = round((row + 1) * 400 / size)

            tile = image.crop((left, upper, right, lower))
            tiles.append(tile)
    return tiles

# Shuffle The Tiles
def shuffle_tiles(tiles):
    shuffled = list(enumerate(tiles))
    random.shuffle(shuffled)
    return shuffled

# Display Shuffled Tiles On The Puzzle Canvas
def display_tiles(tiles):
    size = int(grid_size.get()[0])

    puzzle_canvas.delete("all")
    puzzle_canvas.tiles = []

    index = 0

    for row in range(size):
        for col in range(size):

            # Calculate Each Tile's Position
            x = round(col * 400 / size)
            y = round(row * 400 / size)

            # Convert The Tile For Tkinter
            tile_id, tile_image = tiles[index]
            tile_photo = ImageTk.PhotoImage(tile_image)

            # Keep The Image In Memeory
            puzzle_canvas.tiles.append(tile_photo)

            # Display The Tile
            puzzle_canvas.create_image(
                x, y,
                anchor = "nw",
                image = tile_photo,
            )

            index +=1

    draw_grid()

# Update The Puzzle When The Grid Size Chnages
def change_grid():
    global current_tiles, hints_used

    if current_image:
        tiles = create_tiles(current_image)
        shuffled_tiles = shuffle_tiles(tiles)

        current_tiles = shuffled_tiles
        hints_used = 0
        hinted_tiles.clear()

        display_tiles(shuffled_tiles)

        original_hint_canvas.delete("hint")
        hint_button.configure(state = "normal", 
                           text = "Hint (0/3)"
        )

        # Enable The Solve Button
        solve_button.configure(state = "normal")
    else:
        draw_grid()

# Show A Hint An Inccorrect Tile
def show_hint():
    global hints_used, hinted_tiles

    if hints_used >= 3 or not current_tiles:
        return

    size = int(grid_size.get()[0])

    # Find A Tile In The Wrong Position
    incorrect_tiles = [
        index
        for index, (tile_id, title_image)
        in enumerate(current_tiles)
        if tile_id != index and tile_id not in hinted_tiles
    ]

    if not incorrect_tiles:
        return

    # Choose One Incorrect Tile
    index = random.choice(incorrect_tiles)
    tile_id, tile_image = current_tiles[index]
    hinted_tiles.add(tile_id)

    # Remove Previous Hint Circles
    puzzle_canvas.delete("hint")
    original_hint_canvas.delete("hint")

    # Cicle On The Shuffled Tile
    col = index % size
    row = index // size

    x = (col + 0.5) * 400 / size
    y = (row + 0.5) * 400 / size

    radius = 15

    puzzle_canvas.create_oval(
        x - radius, y - radius,
        x + radius, y + radius,
        outline = "#DC0FE3",
        width = 3,
        tags = "hint"
    )

    # Circle On The Tile's Correct Position
    home_col = tile_id % size
    home_row = tile_id // size

    home_x = (home_col + 0.5) * 400 / size
    home_y = (home_row + 0.5) * 400 / size

    original_hint_canvas.create_oval(
        home_x - radius, home_y - radius,
        home_x + radius, home_y + radius,
        outline = "#DC0FE3",
        width = 3,
        tags = "hint"
    )

    hints_used += 1 
    hint_button.configure(text = f"Hint ({hints_used}/3)")

    if hints_used >= 3:
        hint_button.configure(state = "disabled")

# Solve The Puzzle
def solve_puzzle():
    global current_tiles, hints_used

    if current_image is None:
        return

    # Restore All Tiles To Their Original Position
    tiles = create_tiles(current_image)
    current_tiles = list(enumerate(tiles))

    # Display the completed puzzle
    display_tiles(current_tiles)

    # Remove The Circles
    original_hint_canvas.delete("hint")
    puzzle_canvas.delete("hint")

    # Disable The Buttons After Solving
    hint_button.configure(
        text = "Hint (0/3)",
        state = "disabled"
    )
    solve_button.configure(state = "disabled")

# Top Left Row
top_frame = tk.Frame(root,
                     bg = "#10072B")
top_frame.pack(anchor = "w", padx = 140, pady = 10)

# Frame for Difficulty and Grid Size Slectors
selector_frame = tk.Frame(top_frame, 
                          bg ="#10072B")
selector_frame.pack(side = "left")

# Difficulty Box
difficulty_box = ctk.CTkFrame(
    selector_frame,
    fg_color = "#F4E8FF",
    bg_color = "#10072B",
    border_color = "#8A2BE2",
    border_width = 2,
    corner_radius = 10,
    width = 193,
    height = 85,
)
difficulty_box.pack(side = "left", padx = (10, 10))
difficulty_box.pack_propagate(False)

# Grid Size Box
grid_box = ctk.CTkFrame(
    selector_frame,
    fg_color = "#F4E8FF",
    bg_color = "#10072B",
    border_color = "#8A2BE2",
    border_width = 2,
    corner_radius = 10,
    width = 193,
    height = 85,
)
grid_box.pack(side = "left", padx = (10, 0))
grid_box.pack_propagate(False)

# Difficulty Selection
difficulty = tk.StringVar(value = "Easy")

difficulty_label = tk.Label(
    difficulty_box,
    text = "Select Diffficulty:",
    font = ("Didot", 16, "bold"),
    fg = "#DC0FE3",
    bg = "#F4E8FF"
)
difficulty_label.pack(pady = (12, 5))

difficulty_menu = tk.OptionMenu(
    difficulty_box,
    difficulty,
    "Easy", "Medium","Hard"
)

difficulty_menu.config(
    font = ("Didot", 14),
    fg = "#10072B",
    bg = "#F4E8FF",
    width = 6
)
difficulty_menu.pack(pady = 0)

difficulty_menu["menu"].config(
    font = ("Didot", 14),
    fg = "#10072B",
)

# Grid Size Selection
grid_size = tk.StringVar(value="3x3")

grid_label = tk.Label(
    grid_box,
    text = "Select Grid Size:",
    font = ("Didot", 16, "bold"),
    fg = "#DC0FE3",
    bg = "#F4E8FF"
)
grid_label.pack(pady = (12, 5))

grid_menu = tk.OptionMenu(
    grid_box, 
    grid_size, 
    "3x3", "4x4", "5x5",
    command = lambda _: change_grid()
)

grid_menu.config(
    font = ("Didot", 14,),
    fg = "#10072B",
    bg = "#F4E8FF",
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
progress_frame = ctk.CTkFrame(
    top_frame,
    fg_color = "#F4E8FF",
    bg_color = "#10072B",
    border_color = "#8A2BE2",
    border_width = 2,
    corner_radius = 10,
    width = 406,
    height = 85,
)
progress_frame.pack(side = "left", padx = (85, 0))
progress_frame.grid_propagate(False)

# Top Right Row
# Progress Value
moves_var = tk.StringVar(value = "0")
tiles_left_var = tk.StringVar(value = "0")
hints_var = tk.StringVar(value = "3")
time_left_var = tk.StringVar(value = "--:--")
moves_left_var = tk.StringVar(value = "--")

# Function to Create Progress Labels 
def add_progress_label(parent, title, variable, column):
    section = ctk.CTkFrame(
        parent, 
        fg_color = "#F4E8FF",
    )

    section.grid(row = 0, column = column, padx = 23, pady = 12)

    ctk.CTkLabel(
        section,
        text = title,
        font = ("Didot", 16, "bold"),
        text_color = "#DC0FE3",
        bg_color = "#F4E8FF"
    ).pack()

    ctk.CTkLabel(
        section,
        textvariable = variable,
        font = ("Didot", 20, "bold"),
        text_color = "#10072B",
        bg_color = "#F4E8FF"
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

moves_section = add_progress_label(
    progress_frame, "Moves", moves_var, 0)

tiles_section = add_progress_label(
    progress_frame, "Tiles Left", tiles_left_var, 2)

hints_section = add_progress_label(
    progress_frame, "Hints", hints_var, 4)

time_section = add_progress_label(
    progress_frame, "Time Left", time_left_var, 6)

moves_left_section = add_progress_label(
    progress_frame, "Moves Left", moves_left_var, 6)

add_divider(progress_frame, 1)
add_divider(progress_frame, 3)
add_divider(progress_frame, 5)

# Update Progress Display Based on Difficulty
def update_progress_display(*args):
    time_section.grid_remove()
    moves_left_section.grid_remove()

    if difficulty.get() == "Medium":
        time_section.grid()
    elif difficulty.get() == "Hard":
        moves_left_section.grid()

difficulty.trace_add("write", update_progress_display)
update_progress_display()

# Frame To Hold Both Images
image_frame = tk.Frame(root)
image_frame.pack(pady = 0)
image_frame.config(
    bg = "#10072B"
)

# Original Image On The Left
left_frame = tk.Frame(image_frame)
left_frame.pack(side = "left", padx = 40, anchor = "n" )
left_frame.config(
    bg = "#10072B"
)

# Original Image Heading
original_heading = tk.Label(
    left_frame, text = "Original Image",
    font = ("Didot", 24, "bold"),
    fg = "#F4E8FF",
    bg = "#10072B",
)
original_heading.pack(anchor = "w", padx = 0, pady = 15)

# Original Image Container
original_container = tk.Frame(
    left_frame, 
    width = 406, 
    height = 406, 
    bg = "#F4E8FF",
    highlightbackground = "#8A2BE2",
    highlightthickness = 3,
    highlightcolor = "#8A2BE2"
)
original_container.pack()
original_container.pack_propagate(False)

# Original Image Display
original_hint_canvas = tk.Canvas(
    original_container,
    width = 400,
    height = 400,
    bg = "#F4E8FF",
    highlightthickness = 0,
    borderwidth = 0,
)
original_hint_canvas.pack()

# Upoad Image button
load_button = tk.Button(
    original_container,
    text = "Upload Image (JPG, PNG, BMP)",
    command = load_image,
    font = ("Didot", 14),
    fg = "#10072B",
    bg = "#F4E8FF",
    highlightbackground = "#F4E8FF"
)
load_button.place(relx = 0.5, rely = 0.5, anchor = "center"
)

# Puzzle Image Frame On The Right
right_frame = tk.Frame(image_frame)
right_frame.pack(side = "right", 
                 padx = 35, 
                 anchor = "n")
right_frame.config(
    bg = "#10072B"
)

# Puzzle Image Heading
puzzle_heading = tk.Label(
    right_frame, text = "Puzzle Image",
    font = ("Didot", 24, "bold"),
    fg = "#F4E8FF",
    bg = "#10072B",
)
puzzle_heading.pack(anchor = "w", padx = 0, pady = 15)

# Puzzle Canvas
puzzle_canvas = tk.Canvas(right_frame,
    width = 400, 
    height = 400,
    bg = "#F4E8FF",
    highlightbackground = "#8A2BE2",
    highlightthickness = 3,
    highlightcolor = "#8A2BE2",
)
puzzle_canvas.pack()

#Draw Faint Grid Lines
def draw_grid():
    puzzle_canvas.delete("grid")
    size = int(grid_size.get()[0])
    tile_size = 400 / size

    for i in range(1, size):
        position = i * tile_size

        puzzle_canvas.create_line(position, 0, position, 400, 
                                  fill="#8A2BE2", tags="grid")

        puzzle_canvas.create_line(0, position, 400, position,
                                    fill="#8A2BE2", tags="grid")

draw_grid()

#Hint and Solve Buttons
button_frame = tk.Frame(
    right_frame,
    bg = "#10072B"
)
button_frame.pack(pady=(25, 0))

hint_button = ctk.CTkButton(
    button_frame,
    text = "Hint (0/3)",
    command = show_hint,
    state = "disabled",
    font = ("Arial", 18, "bold"),
    text_color = "#8A2BE2",
    fg_color = "#F4E8FF",
    border_width = 2,
    border_color = "#F4E8FF",
    hover_color = "#DC0FE3",
    width = 193,
    height = 50
)
hint_button.pack(side = "left", padx = 10)

solve_button = ctk.CTkButton(
    button_frame,
    text = "Solve",
    command = solve_puzzle,
    state = "disabled",
    font = ("Arial", 18, "bold"),
    text_color = "#F4E8FF",
    fg_color = "#8A2BE2",
    hover_color = "#DC0FE3",
    width = 193,
    height = 50
)
solve_button.pack(side = "right", padx = 10)

root.mainloop()