import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np
# from scipy.ndimage import uniform_filter1d

def tick_settings(ax):
    ax.set_xticks([-4,-2,0,2,4,6], labels=[r'$10^{-4}$',r'$10^{-2}$',r'$10^{0}$',r'$10^{2}$',r'$10^{4}$',r'$10^{6}$'])

def main():
    
    # quartile plots
    counts_and_areas = pd.read_csv('figures/inputs/areas_and_counts.csv')

    groupings = [50,100,500,1000]
    # groupings = []
    for n in groupings:
        # set up
        column = f'rank_group_{n}'
        groups = counts_and_areas[column].unique()
        
        species_count_y = []
        observer_count_y = []
        checklist_count_y = []
        x = []

        for group in groups:
            species_count_data = counts_and_areas[counts_and_areas[column] == group]['species_count']
            species_count_y.append(species_count_data)

            observer_data = counts_and_areas[counts_and_areas[column] == group]['observer_count']
            observer_count_y.append(observer_data)

            checklist_data = counts_and_areas[counts_and_areas[column] == group]['checklists_submitted']
            checklist_count_y.append(checklist_data)
            
            area_data = counts_and_areas[counts_and_areas[column] == group]['area_km2']
            median = np.median(area_data)
            x.append(np.log10(median))

        # species counts - boxplot
        fig, ax = plt.subplots()
        ax.boxplot(species_count_y, positions=x, widths=0.20, showfliers=False)
        ax.set_yscale('log')
        tick_settings(ax)
        ax.set_title(f"Island species counts at median area of {n} islands grouped")
        ax.set_xlabel(r"$log_{10}$ Island Area")
        ax.set_ylabel(r"$log_{10}$ Species Count")
        plt.savefig(f'figures/outputs/boxplot_by_{n}.png')
        plt.close()

        # species count - violinplot
        fig, ax = plt.subplots()
        ax.violinplot(species_count_y, positions=x, side='both', showmedians=True, points=1000)
        ax.set_yscale('log')
        tick_settings(ax)
        ax.set_title(f"Island species counts at median area of {n} islands grouped")
        ax.set_xlabel(r"$log_{10}$ Island Area")
        ax.set_ylabel(r"$log_{10}$ Species Count")
        plt.savefig(f'figures/outputs/violinplot_by_{n}.png')
        plt.close()

        # observer counts - violinplot
        fig, ax = plt.subplots()
        ax.violinplot(species_count_y, positions=x, side='both', showmedians=True, points=1000)
        ax.set_yscale('log')
        tick_settings(ax)
        ax.set_title(f"Island observer counts at median area of {n} islands grouped")
        ax.set_xlabel(r"$log_{10}$ Island Area")
        ax.set_ylabel(r"$log_{10}$ Observer Count")
        plt.savefig(f'figures/outputs/observer_violinplot_by_{n}.png')
        plt.close()

        # checklist counts - violinplot
        fig, ax = plt.subplots()
        ax.violinplot(species_count_y, positions=x, side='both', showmedians=True, points=1000)
        ax.set_yscale('log')
        tick_settings(ax)
        ax.set_title(f"Island checklist counts at median area of {n} islands grouped")
        ax.set_xlabel(r"$log_{10}$ Island Area")
        ax.set_ylabel(r"$log_{10}$ Checklist Count")
        plt.savefig(f'figures/outputs/checklist_violinplot_by_{n}.png')
        plt.close()
        
    return 0

if __name__=="__main__":
    main()