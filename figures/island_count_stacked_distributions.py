import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
import numpy as np
# from scipy.ndimage import uniform_filter1d

def area_label_string(area):
    return r"$10^{{{}}} \, km^{{2}} $".format(area)

def main():
    
    # quartile plots
    counts_and_areas = pd.read_csv('figures/inputs/areas_and_counts_2024.csv')

    n = 1000
    column = f'rank_group_{n}'
    groups = counts_and_areas[column].unique()

    # initialize plot
    fig, ax = plt.subplots(figsize=(12,8))
    # create a color gradient
    # Create a color gradient based on the y-values
    color_checkpoints = np.linspace(0, 1, len(groups))
    color_list = plt.cm.viridis(color_checkpoints)

    median_group_areas = []

    for j, group in enumerate(groups): # work by group of n islands
        # find species count data for that group of islands
        log10_count = np.log10(counts_and_areas[counts_and_areas[column] == group]['species_count'])
        median_count = np.median(log10_count)
        real_n = len(log10_count)
        print(real_n)

        # make percentiles for each group of islands
        # evenly spaced on the x-axis between their minimum and maximum
        # and include minimum and maximum (so 11 numbers overall)
        max_count = np.max(log10_count)
        min_count = np.min(log10_count)
        increments = np.linspace(min_count, max_count, 11)

        # now subtract out the median species for the group of islands
        # to center the distribution
        med_count = np.median(log10_count)
        increments_centered = increments - med_count

        # find the area data for that group of n islands
        log10_area = np.log10(counts_and_areas[counts_and_areas[column] == group]['area_km2'])
        # use the median area of the group for labeling
        med_area = np.median(log10_area)
        median_group_areas.append(med_area)
        
        # build deciles
        group_x = []
        group_y = []

        for i in range(1,11):
            # the y axis is the number of land areas in that decile group
            percentile_size = log10_count.where(log10_count < increments[i]).where(log10_count >= increments[i-1]).count()
            y = percentile_size / real_n

            # the x-axis is the species 
            x = increments_centered[i]

            group_x.append(x)
            group_y.append(y)

        # plot that group's data
        ax.plot(group_x, group_y, label= f"{med_area:.2f}" + r" $km^{2}", color=color_list[j])

    ax.set_title(f"Scaling function within groups of 1000 islands is approximately normal")
    ax.set_xlabel(r"Centered $log_{10}$ Species Count")
    ax.set_ylabel(r"Fraction of land areas within 1000-island group")

    def create_line_label(x, y, i):
        area = round(median_group_areas[i],1)
        color = color_list[i]
        label = area_label_string(area)
        plt.text(x, y, label, fontdict={'color':color, 'weight': 'bold'})

    create_line_label(-1.75, 0.0, 7)
    create_line_label(-1.75, 0.02, 6)
    create_line_label(-1.3, 0.01, 5)
    create_line_label(-1.5, 0.03, 4)
    create_line_label(-1.35, 0.04, 3)
    create_line_label(-1.3, 0.06,2)
    create_line_label(-1.1, 0.08, 1)
    create_line_label(-0.9, 0.145, 0)

    plt.savefig('figures/outputs/stacked_distributions.png')

    return 0

if __name__=="__main__":
    main()