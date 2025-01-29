import tkinter as tk
from tkinter import messagebox
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)

        # Game constants
        self.GAME_WIDTH = 700
        self.GAME_HEIGHT = 500
        self.SPEED = 100
        self.SPACE_SIZE = 20
        self.BODY_PARTS = 3
        self.SNAKE_COLOR = "#00FF00"
        self.FOOD_COLOR = "#FF0000"
        self.BACKGROUND_COLOR = "#000000"

        # Game variables
        self.direction = 'right'
        self.score = 0
        
        # Create score label
        self.label = tk.Label(self.root, text=f"Score: {self.score}", font=('consolas', 20))
        self.label.pack()

        # Create game canvas
        self.canvas = tk.Canvas(
            self.root, 
            bg=self.BACKGROUND_COLOR,
            height=self.GAME_HEIGHT,
            width=self.GAME_WIDTH
        )
        self.canvas.pack()

        # Initialize snake
        self.snake_positions = []
        self.food_position = []
        self.snake_body = []
        
        # Bind keyboard controls
        self.root.bind('<Left>', lambda event: self.change_direction('left'))
        self.root.bind('<Right>', lambda event: self.change_direction('right'))
        self.root.bind('<Up>', lambda event: self.change_direction('up'))
        self.root.bind('<Down>', lambda event: self.change_direction('down'))

        # Center the window
        self.center_window()
        
        # Start game
        self.start_game()

    def center_window(self):
        """Center the game window on the screen"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width/2) - (self.GAME_WIDTH/2)
        y = (screen_height/2) - (self.GAME_HEIGHT/2)
        
        self.root.geometry(f'{self.GAME_WIDTH}x{self.GAME_HEIGHT+30}+{int(x)}+{int(y)}')

    def start_game(self):
        """Initialize game state and start the game loop"""
        # Create snake
        for i in range(self.BODY_PARTS):
            x = self.SPACE_SIZE * (self.BODY_PARTS - i)
            y = self.SPACE_SIZE
            self.snake_positions.append([x, y])
            square = self.canvas.create_rectangle(
                x, y,
                x + self.SPACE_SIZE,
                y + self.SPACE_SIZE,
                fill=self.SNAKE_COLOR,
                tag="snake"
            )
            self.snake_body.append(square)

        # Create food
        self.create_food()
        
        # Start game loop
        self.next_turn()

    def create_food(self):
        """Create food at random position"""
        while True:
            x = random.randint(0, (self.GAME_WIDTH - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            y = random.randint(0, (self.GAME_HEIGHT - self.SPACE_SIZE) // self.SPACE_SIZE) * self.SPACE_SIZE
            
            # Make sure food doesn't appear on snake
            if [x, y] not in self.snake_positions:
                self.food_position = [x, y]
                break

        self.canvas.create_oval(
            x, y,
            x + self.SPACE_SIZE,
            y + self.SPACE_SIZE,
            fill=self.FOOD_COLOR,
            tag="food"
        )

    def next_turn(self):
        """Handle game logic for the next turn"""
        # Get head position
        head = self.snake_positions[0].copy()

        # Update head position based on direction
        if self.direction == 'left':
            head[0] -= self.SPACE_SIZE
        elif self.direction == 'right':
            head[0] += self.SPACE_SIZE
        elif self.direction == 'up':
            head[1] -= self.SPACE_SIZE
        elif self.direction == 'down':
            head[1] += self.SPACE_SIZE

        # Insert new head
        self.snake_positions.insert(0, head)

        # Create new snake square
        square = self.canvas.create_rectangle(
            head[0], head[1],
            head[0] + self.SPACE_SIZE,
            head[1] + self.SPACE_SIZE,
            fill=self.SNAKE_COLOR
        )
        self.snake_body.insert(0, square)

        # Check if food eaten
        if head == self.food_position:
            # Delete food
            self.canvas.delete("food")
            # Update score
            self.score += 1
            self.label.config(text=f"Score: {self.score}")
            # Create new food
            self.create_food()
        else:
            # Remove tail
            del self.snake_positions[-1]
            self.canvas.delete(self.snake_body[-1])
            del self.snake_body[-1]

        # Check for collision
        if self.check_collision():
            self.game_over()
        else:
            # Schedule next turn
            self.root.after(self.SPEED, self.next_turn)

    def check_collision(self):
        """Check for collisions with walls or self"""
        head = self.snake_positions[0]
        
        # Check wall collision
        if (head[0] < 0 or 
            head[0] >= self.GAME_WIDTH or 
            head[1] < 0 or 
            head[1] >= self.GAME_HEIGHT):
            return True
        
        # Check self collision
        if head in self.snake_positions[1:]:
            return True
            
        return False

    def change_direction(self, new_direction):
        """Change snake direction if valid"""
        opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
        
        if opposites.get(new_direction) != self.direction:
            self.direction = new_direction

    def game_over(self):
        """Handle game over state"""
        self.canvas.delete("all")
        game_over_text = f"Game Over!\nScore: {self.score}"
        self.canvas.create_text(
            self.GAME_WIDTH/2,
            self.GAME_HEIGHT/2,
            font=('consolas', 70),
            text=game_over_text,
            fill="red",
            anchor="center"
        )
        
        # Ask to play again
        if messagebox.askyesno("Game Over", "Would you like to play again?"):
            self.reset_game()
        else:
            self.root.quit()

    def reset_game(self):
        """Reset game state for a new game"""
        self.canvas.delete("all")
        self.score = 0
        self.label.config(text=f"Score: {self.score}")
        self.direction = 'right'
        self.snake_positions = []
        self.snake_body = []
        self.start_game()

def main():
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()