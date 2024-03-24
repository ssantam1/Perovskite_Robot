import pandas as pd
import matplotlib.pyplot as plt

def progX(input_value):
    # Use the input value in the main script
    print(input_value)

    # Example: Create a DataFrame with a column named 'col'
    df = pd.DataFrame({'col': [input_value]})

    # Example: Create a boxplot of the 'col' column
    plt.boxplot(df['col'])

    # Display the plot
    plt.show()

# Call the main script by passing the input value as an argument
my_input_value = " example value"
progX(my_input_value)
