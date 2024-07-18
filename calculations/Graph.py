import matplotlib.pyplot as plt

class Beam:
    def __init__(self, width, height, cover, steeldim):
        self.width = width
        self.height = height
        self.cover = cover
        self.steeldim = steeldim

    def draw_beam(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(0, self.width + 20)
        ax.set_ylim(0, self.height + 20)
        
        # Draw the beam rectangle
        beam = plt.Rectangle((10, 10), self.width, self.height, edgecolor='black', facecolor='gray')
        ax.add_patch(beam)

        # Draw the cover
        cover_rect = plt.Rectangle((10 + self.cover, 10 + self.cover), 
                                   self.width - 2*self.cover, 
                                   self.height - 2*self.cover, 
                                   edgecolor='blue', linestyle='--', facecolor='none')
        ax.add_patch(cover_rect)

        # Draw the steel bars
        steel_x_positions = [10 + self.cover + self.steeldim / 2, 10 + self.width - self.cover - self.steeldim / 2]
        steel_y_positions = [10 + self.cover + self.steeldim / 2, 10 + self.height - self.cover - self.steeldim / 2]
        
        for x in steel_x_positions:
            for y in steel_y_positions:
                steel_bar = plt.Circle((x, y), radius=self.steeldim / 2, edgecolor='red', facecolor='red')
                ax.add_patch(steel_bar)

        # Add labels
        ax.text(self.width / 2, -10, f'Width: {self.width} mm', ha='center')
        ax.text(-20, self.height / 2, f'Height: {self.height} mm', va='center', rotation='vertical')

        plt.title('Concrete Beam Detail')
        plt.axis('off')
        plt.show()

# Example usage
beam = Beam(width=300, height=600, cover=40, steeldim=16)
beam.draw_beam()
