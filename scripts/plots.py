from matplotlib import pyplot as plt
import pandas as pd
from scripts.advantage import get_all_advantages_and_disadvantages
import numpy as np


def plot_single_reponse(df, only_use_col=None):
    exclude_columns = ['Name', 'Score']

    for column in df.columns:
        if column not in exclude_columns and (only_use_col is None or column == only_use_col):
            # Print unique values
            unique_values = df[column].unique()

            # Print counts for each value, sorted from most to less
            value_counts = df[column].value_counts().sort_values(ascending=False)

            # Calculate and print average score per category within the column, sorted from highest to lowest
            average_score_per_category = df.groupby(column)['Score'].mean().sort_values(ascending=False)
            summary_df = pd.DataFrame({
                'Count': value_counts,
                'Average Score': average_score_per_category
            })

            # Sort the DataFrame by Average Score, descending
            summary_df = summary_df.sort_values(by='Average Score', ascending=False)

            # Print the result
            print(f"- - - {column} - - -\n{summary_df}\n")

            # Adjust figure size conditionally
            if column == 'Ethnicity':
                plt.figure(figsize=(10, 10))  # Taller figure for Ethnicity
            else:
                plt.figure(figsize=(10, 6))

            # Plotting with a colormap for more colors
            cmap = plt.get_cmap('viridis')  # Get a colormap
            colors = cmap(np.linspace(0, 1, len(average_score_per_category)))  # Generate colors
            average_score_per_category.sort_values().plot(kind='barh', color=colors)  # Use colors in plot
            plt.title(f'Average Score per {column}')
            plt.xlabel('Average Score')
            plt.ylabel(column)
            plt.tight_layout()
            plt.show()



def plot_all_advantages_and_disadvantages(dfs, alpha=0.001, only_use_col=None, verbose=False):
    num_dfs_checked = len(dfs)  # The number of dataframes checked
    columns = dfs[0].columns
    exclude_columns = ['Name', 'Score']

    for column in columns:
        if column not in exclude_columns and (only_use_col is None or column == only_use_col):
            advantages, disadvantages = get_all_advantages_and_disadvantages(dfs, column, alpha, verbose=verbose)
            
            # Combine and sort
            combined = [(label, advantages.get(label, 0), -disadvantages.get(label, 0)) for label in set(advantages) | set(disadvantages)]
            sorted_combined = sorted(combined, key=lambda x: (x[1], x[2]), reverse=True)
            
            # Unpack the sorted labels, advantages, and disadvantages (now positive for plotting)
            labels, adv_values, disadv_values = zip(*[(label, adv, -disadv) for label, adv, disadv in sorted_combined])
            
            # Plot
            cmap = plt.get_cmap('tab10')
            x = np.arange(len(labels))  # Use NumPy to generate array for x positions
            bar_width = 0.4  # Width of the bars

            fig, ax = plt.subplots()

            # Adjust the positions: subtract half the bar width from the x positions for advantages
            # and add half the bar width to the x positions for disadvantages.
            # This effectively moves the advantages bars to the left and the disadvantages bars to the right.
            ax.bar(x - bar_width / 2, adv_values, width=bar_width, label='Advantages', align='center', color=cmap(0))
            ax.bar(x + bar_width / 2, disadv_values, width=bar_width, label='Disadvantages', align='center', color=cmap(1))

            ax.set_xlabel('Unique Values')
            ax.set_ylabel('Counts')
            ax.set_title(f'Advantages and Disadvantages for {column}\n(Responses Checked: {num_dfs_checked})')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation='vertical')
            ax.legend()
            
            plt.xticks(rotation=45, ha="right", rotation_mode="anchor")  # Adjust rotation and alignment of x labels
            plt.tight_layout()
            plt.show()