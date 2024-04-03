
from scipy import stats
import numpy as np


def get_advantages_and_disadvantages(df, file_index, column_name, alpha,dfs_count):
    advantages = []
    disadvantages = []
    unique_values = df[column_name].unique()
    n_unique_values = len(unique_values)
    for unique_value in unique_values:
        df_only_unique_value = df[df[column_name] == unique_value]
        df_no_unique_value = df[df[column_name] != unique_value]

        mean_score_unique_value = df_only_unique_value['Score'].mean()
        mean_score_no_unique_value = df_no_unique_value['Score'].mean()

        std_score_unique_value = df_only_unique_value['Score'].std(ddof=0) # ddof=0 to get population std
        std_score_no_unique_value = df_no_unique_value['Score'].std(ddof=0) # ddof=0 to get population std

        n_unique_values = len(df_only_unique_value)
        n_no_unique_values = len(df_no_unique_value)

        z_statistic = (mean_score_unique_value - mean_score_no_unique_value) / np.sqrt((std_score_unique_value**2/n_unique_values) + (std_score_no_unique_value**2/n_no_unique_values))

        p_value = 2 * (1 - stats.norm.cdf(np.abs(z_statistic)))

        bonferonni_alpha = alpha / (n_unique_values * dfs_count)


        if p_value < bonferonni_alpha:
            print(f"Significant difference for {column_name}={unique_value} (p={p_value:.4f}) in {file_index}th dataset")
            if mean_score_unique_value > mean_score_no_unique_value:
                advantages.append((unique_value, p_value))
            else:
                disadvantages.append((unique_value, p_value))

    return advantages, disadvantages



def get_all_advantages_and_disadvantages(dfs, column_name, alpha):
    advantages = {}
    disadvantages = {}
    dfs_count = len(dfs)
    for i, df in enumerate(dfs):
        df_advantages, df_disadvantages = get_advantages_and_disadvantages(df, i, column_name,alpha,dfs_count)
        for unique_value, p_value in df_advantages:
            if unique_value in advantages:
                advantages[unique_value] += 1
            else:
                advantages[unique_value] = 1

        for unique_value, p_value in df_disadvantages:
            if unique_value in disadvantages:
                disadvantages[unique_value] += 1
            else:
                disadvantages[unique_value] = 1

    return advantages, disadvantages


