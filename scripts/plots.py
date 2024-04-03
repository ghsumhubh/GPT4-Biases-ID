from matplotlib import pyplot as plt
import pandas as pd
from scripts.advantage import get_all_advantages_and_disadvantages

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
            # Plotting average score per category, sorted
            plt.figure(figsize=(10, 6))
            average_score_per_category.sort_values().plot(kind='barh')  # Horizontal bar plot for better readability
            plt.title(f'Average Score per {column}')
            plt.xlabel('Average Score')
            plt.ylabel(column)
            plt.tight_layout()
            plt.show()



def plot_all_advantages_and_disadvantages(dfs, alpha=0.001, only_use_col=None, verbose=False):
    columns = dfs[0].columns
    exclude_columns = ['Name', 'Score']

    for column in columns:
        if column not in exclude_columns and (only_use_col is None or column == only_use_col):
            advantages, disadvantages = get_all_advantages_and_disadvantages(dfs, column, alpha, verbose=verbose)
            
            # Prepare data for plotting
            labels = list(set(advantages.keys()) | set(disadvantages.keys()))
            adv_values = [advantages.get(label, 0) for label in labels]
            disadv_values = [-disadvantages.get(label, 0) for label in labels]  # Make disadvantages negative for clarity
            
            # Plot
            x = range(len(labels))  # Label locations
            fig, ax = plt.subplots()
            ax.bar(x, adv_values, width=0.4, label='Advantages', align='center')
            ax.bar(x, disadv_values, width=0.4, label='Disadvantages', align='edge')
            
            ax.set_xlabel('Unique Values')
            ax.set_ylabel('Counts')
            ax.set_title(f'Advantages and Disadvantages for {column}')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation='vertical')
            ax.legend()
            
            # Show plot
            plt.tight_layout()
            plt.show()