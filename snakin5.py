import scene
import random
import sound

class SnakeGame(scene.Scene):
    def setup(self):
        self.cell_size = 15
        self.snake = [(10 * self.cell_size, 10 * self.cell_size)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.food = self.new_food_position()
        self.score = 0
        self.game_over = False
        self.update_interval = 0.2
        self.update_time = 0
        self.has_turned = False
        self.background_color = "white"

    def new_food_position(self):
        cells_wide = int(self.size.w / self.cell_size)
        cells_high = int(self.size.h / self.cell_size)
        return (random.randint(0, cells_wide - 1) * self.cell_size,
                random.randint(0, cells_high - 1) * self.cell_size)

    def update(self):
        if not self.game_over:
            self.update_time += self.dt
            if self.update_time > self.update_interval:
                self.update_time = 0
                self.direction = self.next_direction
                self.move_snake()
                self.check_for_collisions()
                self.has_turned = False

    def move_snake(self):
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0] * self.cell_size, 
                    head_y + self.direction[1] * self.cell_size)
        if new_head == self.food:
            self.snake.insert(0, new_head)
            #sound.play_effect('Chompin.m4a')  # Play the chomp sound effect
            self.food = self.new_food_position()
            self.score += 1
        else:
            self.snake.insert(0, new_head)
            self.snake.pop()

    def check_for_collisions(self):
        head_x, head_y = self.snake[0]
        # Check for collisions with the wall
        if head_x < 0 or head_x >= self.size.w or head_y < 0 or head_y >= self.size.h:
            self.game_over = True
        # Check for collisions with itself
        for segment in self.snake[1:]:
            if self.snake[0] == segment:
                self.game_over = True
                break

    def draw(self):
        scene.background(0, 0, 0)
        self.draw_snake()
        self.draw_food()
        if self.game_over:
            self.draw_game_over()

    def draw_snake(self):
		    for segment in self.snake:
		        random_color = (random.random(), random.random(), random.random())  # Generate a random color
		        scene.fill(*random_color)  # Use the random color for this segment
		        scene.rect(segment[0], segment[1], self.cell_size, self.cell_size)
        
    def draw_food(self):
        scene.fill(1, 0, 0)
        scene.ellipse(self.food[0], self.food[1], self.cell_size, self.cell_size)

    def draw_game_over(self):
        scene.tint(1, 1, 1)
        scene.text('Game Over! Score: {}'.format(self.score), x=self.size.w * 0.5, y=self.size.h * 0.5, font_size=20)

    def touch_began(self, touch):
        if self.game_over:
            self.setup()
            return

        if not self.has_turned:
            x, y = touch.location
            dx, dy = self.direction
            if abs(dx) > abs(dy):
                if y > self.snake[0][1]:
                    self.next_direction = (0, 1)  # Up
                elif y < self.snake[0][1]:
                    self.next_direction = (0, -1)  # Down
            else:
                if x > self.snake[0][0]:
                    self.next_direction = (1, 0)  # Right
                elif x < self.snake[0][0]:
                    self.next_direction = (-1, 0)  # Left
            self.has_turned = True

if __name__ == '__main__':
    scene.run(SnakeGame(), scene.PORTRAIT, show_fps=False)
