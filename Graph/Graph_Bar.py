import matplotlib.pyplot as plt

class DynamicBarChart:
    def __init__(self, labels, values, title, xlabel, ylabel):
        """
        Initialize the DynamicBarChart class.
        :param labels: List of labels for the x-axis categories.
        :param initial_values: Initial list of values corresponding to each label.
        :param num_frames: Total number of frames to animate.
        :param interval: Interval in milliseconds between frames.
        """
        # Creating an instance of RectangleColumn

        if len(labels) != len(values):
            raise ValueError("Length of labels and initial_values must be the same.")
        
        self.labels = labels
        self.values = values
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        
        # Create the plot
        self.fig, self.ax = plt.subplots()
        self.bars = self.ax.bar(self.labels, self.values)
        
        # Set plot limits and labels
        self.ax.set_ylim(0, max(self.values) + 100)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

        plt.show()

