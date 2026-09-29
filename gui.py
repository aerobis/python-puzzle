import tkinter as tk
import random 

from tkinter import filedialog
from PIL import Image, ImageTk
from PIL import ImageOps

root = tk.Tk()
root.title("Image Puzzle Game")
root.geometry("1000x750")
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
        hint_button.config(state = "normal", text = "Hint (0/3)")

        # Enable The Solve Button
        solve_button.config(state = "normal")

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
        hint_button.config(state = "normal", 
                           text = "Hint (0/3)"
        )

        # Enable The Solve Button
        solve_button.config(state = "normal")
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
        outline = "#00E5FF",
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
        outline = "#00E5FF",
        width = 3,
        tags = "hint"
    )

    hints_used += 1 
    hint_button.config(text = f"Hint ({hints_used}/3)")

    if hints_used >= 3:
        hint_button.config(state = "disabled")

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
    hint_button.config(
        text = "Hint (0/3)",
        state = "disabled"
    )
    solve_button.config(state = "disabled")

# Grid Size Selection
grid_size = tk.StringVar(value="3x3")

grid_label = tk.Label(root, 
                      text = "Select Grid Size:",
                      font = ("Didot", 18),
                      fg = "#00E5FF",
                      bg = "#10072B"
                    )
grid_label.pack(pady = (10, 5))

grid_menu = tk.OptionMenu(root, 
                          grid_size, 
                          "3x3", "4x4", "5x5",
                          command = lambda _: change_grid())

# Decorate The Drop Down Button
grid_menu.config(
    font = ("Didot", 14,),
    fg = "#10072B",
    bg = "#10072B",
    width = 3,
    relief = "flat",
    highlightthickness = 0
)

# Decorate The Dropdown Options
grid_menu["menu"].config(
    font = ("Didot", 14),
    fg = "#10072B",
)
grid_menu.pack(pady = (5, 5))

# Frame To Hold Both Images
image_frame = tk.Frame(root)
image_frame.pack(pady = 20)
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
button_frame.pack(pady=15)

hint_button = tk.Button(
    button_frame,
    text = "Hint (0/3)",
    command = show_hint,
    state = "disabled",
    font = ("Arial", 16, "bold"),
    fg = "#8A2BE2",
    bg = "#F4E8FF",
    highlightbackground = "#10072B",
    cursor = "hand"
)
hint_button.pack(side = "left", padx = 10)

solve_button = tk.Button(
    button_frame,
    text = "Solve",
    command = solve_puzzle,
    state = "disabled",
    font = ("Arial", 16, "bold"),
    fg = "#8A2BE2",
    bg = "#F4E8FF",
    highlightbackground = "#10072B",
    cursor = "hand"
)
solve_button.pack(side = "right", padx = 10)

root.mainloop()