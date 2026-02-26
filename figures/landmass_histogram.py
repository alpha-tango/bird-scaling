import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    landmasses = pd.read_csv(f'island_species_area/outputs/all_areas_and_counts_2024.csv')
    landmasses['log_rounded_area'] = round(np.log10(landmasses['area_km2']))

    all_lands = landmasses.groupby('log_rounded_area')['FID'].count().reset_index()
    checklist_lands = landmasses.groupby('log_rounded_area')['species_count'].count().reset_index()

    fig,ax = plt.subplots()
    ax.bar(all_lands['log_rounded_area'], all_lands['FID'],label="All OSM Coastline Polygons", width=0.33)
    ax.bar(checklist_lands['log_rounded_area'] + 0.33, checklist_lands['species_count'], width=0.33, label="OSM Coastline Polygons with Ebird Checklists in 2024")
    ax.set_yscale('log')
    ax.set_xticks([-8,-6,-4,-2,0,2,4,6,8], labels=[r'$10^{-8}$',r'$10^{-6}$',r'$10^{-4}$',r'$10^{-2}$',r'$10^{0}$',r'$10^{2}$',r'$10^{4}$',r'$10^{6}$',r'$10^{8}$'])
    ax.set_title(r"Landmass counts by area ($km^2$) order of magnitude")
    ax.set_ylabel(r"$log_{10}$ count of landmasses")
    ax.set_xlabel(r"$log_{10}$ area ($km^2$)")
    ax.legend()
    plt.savefig('figures/outputs/landmass_histogram.png')

    return 0

if __name__=="__main__":
    main()