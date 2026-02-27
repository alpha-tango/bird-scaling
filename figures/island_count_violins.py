import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import numpy as np
# from scipy.ndimage import uniform_filter1d

def tick_settings_1000(ax):
    ax.set_xticks([-3,-1,1,3,5,7], labels=[r'$10^{-3}$',r'$10^{-1}$',r'$10^{1}$',r'$10^{3}$',r'$10^{5}$',r'$10^{7}$'])
    ax.set_yticks([0,1,2,3,4],labels=[r'$10^{0}$',r'$10^{1}$',r'$10^{2}$',r'$10^{3}$',r'$10^{4}$'])

def main():
    
    # quartile plots
    counts_and_areas = pd.read_csv('figures/inputs/areas_and_counts_2024.csv')

    if True:
        n = 1000
        column = f'rank_group_{n}'
        groups = counts_and_areas[column].unique()

        fig, ax = plt.subplots(figsize=(12,8))

        for group in groups: # work by group of n islands
            # find species count data for that group of islands
            log10_count = np.log10(counts_and_areas[counts_and_areas[column] == group]['species_count'])
            median_count = np.median(log10_count)
            real_n = len(log10_count)

            # find the area data for that group of n islands
            log10_area = np.log10(counts_and_areas[counts_and_areas[column] == group]['area_km2'])
            # use the max area for the group
            max_area = np.max(log10_area)
            med_area = np.median(log10_area)
            
            # make percentiles for each group of islands
            # evenly spaced on the y-axis between their minimum and maximum
            # and include minimum and maximum (so 11 numbers overall)
            max_count = np.max(log10_count)
            min_count = np.min(log10_count)
            increments = np.linspace(min_count, max_count, 11)
            
            # find the number of items in each percentile for the group 
            for i in range(1,11):
                percentile_size = log10_count.where(log10_count < increments[i]).where(log10_count >= increments[i-1]).count()
                position = (max_area, increments[i])
                width = -percentile_size / real_n * 2
                height = -increments[1]
                inc = mpatches.Rectangle(position, width, height, color='paleturquoise')
                ax.add_patch(inc)

            # add a single rectangle at the median
            position = (max_area, median_count)
            width = -0.2
            height = -0.01
            median = mpatches.Rectangle(position, width, height)
            ax.add_patch(median)

            # add a vertical bar showing the group maximum area
            ax.axvline(max_area, color='gray', linestyle='dashed', linewidth=0.5)

            # ax.set_yscale('log')
        tick_settings_1000(ax)
        ax.set_title(f"Island species counts at median area of 1000 islands grouped")
        ax.set_xlabel(r"$log_{10}$ Island Area")
        ax.set_ylabel(r"$log_{10}$ Species Count")
        plt.savefig('figures/outputs/custom_violinplots_by_1000.png')
        plt.close()

    if True:
        n = 500
        column = f'rank_group_{n}'
        groups = counts_and_areas[column].unique()

        fig, ax = plt.subplots(figsize=(12,8))

        for group in groups: # work by group of n islands
            # find species count data for that group of islands
            log10_count = np.log10(counts_and_areas[counts_and_areas[column] == group]['species_count'])
            median_count = np.median(log10_count)
            real_n = len(log10_count)

            # find the area data for that group of n islands
            log10_area = np.log10(counts_and_areas[counts_and_areas[column] == group]['area_km2'])
            # use the max area for the group
            max_area = np.max(log10_area)
            med_area = np.median(log10_area)
            
            # make percentiles for each group of islands
            # evenly spaced on the y-axis between their minimum and maximum
            # and include minimum and maximum (so 11 numbers overall)
            max_count = np.max(log10_count)
            min_count = np.min(log10_count)
            increments = np.linspace(min_count, max_count, 11)
            
            # find the number of items in each percentile for the group 
            for i in range(1,11):
                percentile_size = log10_count.where(log10_count < increments[i]).where(log10_count >= increments[i-1]).count()
                position = (max_area, increments[i])
                width = -percentile_size / real_n
                height = -increments[1]
                inc = mpatches.Rectangle(position, width, height, color='paleturquoise')
                ax.add_patch(inc)

            # add a single rectangle at the median
            position = (max_area, median_count)
            width = -0.2
            height = -0.01
            median = mpatches.Rectangle(position, width, height)
            ax.add_patch(median)

            # add a vertical bar showing the group maximum area
            ax.axvline(max_area, color='gray', linestyle='dashed', linewidth=0.5)

            # ax.set_yscale('log')
        tick_settings_1000(ax)
        ax.set_title(f"Island species counts at median area of 500 islands grouped")
        ax.set_xlabel(r"$log_{10}$ Island Area")
        ax.set_ylabel(r"$log_{10}$ Species Count")
        plt.savefig('figures/outputs/custom_violinplots_by_500.png')

    return 0

if __name__=="__main__":
    main()