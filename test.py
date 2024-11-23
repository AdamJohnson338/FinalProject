import matplotlib.pyplot as plt
import numpy as np

# Frequency
frequency = 3

# The coordinates
x = np.linspace(0,2 * np.pi, 100)
y = np.sin(frequency * x)


# Create the plot
plt.plot(x,y)

# Add labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Sine plot')

# Display the plot
plt.show()