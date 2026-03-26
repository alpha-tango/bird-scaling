import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
from numpy.polynomial.polynomial import Polynomial 
# from scipy.ndimage import uniform_filter1d

def tick_settings(ax):
    ax.set_xticks([-4,-2,0,2,4,6], labels=[r'$10^{-4}$',r'$10^{-2}$',r'$10^{0}$',r'$10^{2}$',r'$10^{4}$',r'$10^{6}$'])

def main():
    
    # quartile plots
    counts_and_areas = pd.read_csv('figures/inputs/areas_and_counts_2024.csv')
    print(counts_and_areas.columns)

    groupings = [50,100,500,1000]
    # groupings = []

    fig, ax = plt.subplots(4,1, sharex=True, figsize=(6,8))

    for j, n in enumerate(groupings):
        # set up
        column = f'rank_group_{n}'
        groups = counts_and_areas[column].unique()
        
        species_count_0 = []
        species_count_25 = []
        species_count_50 = []
        species_count_75 = []
        species_count_100 = []
        # observer_count_y = []
        # checklist_count_y = []
        x = []

        for group in groups:
            species_count_data = counts_and_areas[counts_and_areas[column] == group]['species_count']
            species_count_0.append(np.min(species_count_data))
            species_count_25.append(np.percentile(species_count_data, 25))
            species_count_50.append(np.percentile(species_count_data, 50))
            species_count_75.append(np.percentile(species_count_data, 75))
            species_count_100.append(np.max(species_count_data))

            # observer_data = counts_and_areas[counts_and_areas[column] == group]['observer_count']
            # observer_count_y.append(observer_data)

            # checklist_data = counts_and_areas[counts_and_areas[column] == group]['checklists_submitted']
            # checklist_count_y.append(checklist_data)
            
            area_data = counts_and_areas[counts_and_areas[column] == group]['area_km2']
            median = np.median(area_data)
            x.append(np.log10(median))

        # calculate log species count for fit line
        log_med_species_count = np.log10(species_count_50)

        # calculate fit line
        linear_fit = Polynomial.fit(x, log_med_species_count, 1)  # linear fit

        # get coefficients
        coefficients = linear_fit.convert().coef
        c = coefficients[0]
        z = coefficients[1]

        # get fit x
        transformed_x = np.array(x)*z + c
        power_transformed_x = [10**i for i in transformed_x]


        # species counts - percentile lines
        # ax.plot(x, species_count_0, color='thistle')
        # ax.plot(x, species_count_25, color='orchid')
        ax[j].fill_between(x, species_count_0, species_count_100, color='thistle')
        ax[j].fill_between(x, species_count_25, species_count_75, color='orchid')
        # ax.plot(x, species_count_75, color='orchid')
        ax[j].plot(x, species_count_50, color='darkorchid')
        # ax.plot(x, species_count_100, color='thistle')
        ax[j].plot(x, power_transformed_x, color='black', linestyle='--')
        ax[j].text(-3,1000,f"z = {z:.3f}")
        ax[j].set_yscale('log')
        tick_settings(ax[j])
        ax[j].set_title(f"{n} islands grouped", fontsize=10)
        ax[j].set_xlabel(r"$log_{10}$ Median Island Area ($km^2$)", fontsize=8)
        ax[j].set_ylabel(r" ")  # just here to create a litte room in the figure for the shared y-label

    fig.text(0.025, 0.5, r"$log_{10}$ Median Species Count", ha='center', va='center', rotation='vertical')
    fig.suptitle("Z-value remains fairly constant over different island groupings")
    plt.tight_layout()
    plt.savefig(f'figures/outputs/quartiles_with_z_values.png')
    plt.close()

        
    return 0

if __name__=="__main__":
    main()