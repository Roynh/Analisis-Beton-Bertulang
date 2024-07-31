import matplotlib.pyplot as plt

class Interaction_Plotter:
    def __init__(self, column_instance):
        # Initialize with a RectangleColumn instance
        self.column_instance = column_instance
        
        # Retrieve e_balance from the column instance
        self.e_balance = self.column_instance._Eb
        
        # Initialize lists to store values for plotting
        self.brittle = []
        self.brittle_phi = []
        self.balance = []
        self.balance_phi = []
        self.ductile = []
        self.ductile_phi = []
        
        # Prepare balance values
        self.balance.append((self.column_instance._Mb, self.column_instance._Pb))
        self.balance_phi.append((self.column_instance._MbPhi, self.column_instance._PbPhi))
        
        # Calculate curves
        self.calculate_brittle_curve()
        self.calculate_ductile_curve()

    def calculate_brittle_curve(self):
        """Calculate brittle curve values."""
        i = 0
        while i < self.e_balance:
            x1, y1, x2, y2 = self.column_instance.Brittle_force(i)
            brittle_val1 = (x1, y1)
            brittle_val2 = (x2, y2)
            if brittle_val1 is not None:
                self.brittle.append(brittle_val1)
                self.brittle_phi.append(brittle_val2)
            print(f'Brittle value at {i}: {brittle_val1} and {brittle_val2}')  # Debug output
            i += 50

    def calculate_ductile_curve(self):
        """Calculate ductile curve values."""
        i = self.e_balance
        i_batas = self.e_balance + 1000
        while i < i_batas:
            x1, y1, x2, y2 = self.column_instance.Ductile_Force(i)
            ductile_val1 = (x1, y1)
            ductile_val2 = (x2, y2)
            if ductile_val1 is not None:
                self.ductile.append(ductile_val1)
                self.ductile_phi.append(ductile_val2)
            print(f'Ductile value at {i}: {ductile_val1} and {ductile_val2}')  # Debug output
            i += 50

    def plot(self):
        """Plot the calculated curves."""
        # Unpack values for plotting
        x1, y1 = zip(*self.brittle) if self.brittle else ([], [])
        x2, y2 = zip(*self.balance)
        x3, y3 = zip(*self.ductile) if self.ductile else ([], [])
        x4, y4 = zip(*self.brittle_phi) if self.brittle_phi else ([], [])
        x5, y5 = zip(*self.balance_phi)
        x6, y6 = zip(*self.ductile_phi) if self.ductile_phi else ([], [])

        # Plot each set of data
        plt.plot(x1, y1, label='Brittle', marker='o', linestyle='-', color='blue')
        plt.plot(x2, y2, label='Balance', marker='o', linestyle='-', color='green')
        plt.plot(x3, y3, label='Ductile', marker='o', linestyle='-', color='red')

        plt.plot(x4, y4, label='Brittle with Reduction', marker='x', linestyle='-', color='blue')
        plt.plot(x5, y5, label='Balance with Reduction', marker='x', linestyle='-', color='green')
        plt.plot(x6, y6, label='Ductile with Reduction', marker='x', linestyle='-', color='red')

        # Add title, axis labels, and legend
        plt.title('Diagram Interaksi')
        plt.xlabel('Mn Values')
        plt.ylabel('Pn Values')
        plt.legend()

        # Add grid
        plt.grid(True)

        # Display plot
        plt.show()

