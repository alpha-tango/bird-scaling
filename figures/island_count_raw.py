import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy as np

def main():
    
    counts_and_areas = pd.read_csv('figures/inputs/areas_and_counts.csv')

    if True:
        # basic plot
        fig, ax = plt.subplots()
        im = ax.scatter(
            counts_and_areas['area_km2'],
            counts_and_areas['species_count'], 
            s=2)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title('2024 Island Species Counts')
        ax.set_xlabel(r'$Log_{10}$ Area ($km^{2}$)')
        ax.set_ylabel(r'$Log_{10}$ Species Count')
        plt.savefig('figures/outputs/island_species_counts.png')

    if True:
        # colored by number of checklists submitted
        fig, ax = plt.subplots()
        im = ax.scatter(
            counts_and_areas['area_km2'],
            counts_and_areas['species_count'], 
            c=np.log(counts_and_areas['checklists_submitted']),
            cmap='inferno',
            s=4)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title('2024 Island Species Counts')
        ax.set_xlabel(r'$Log_{10}$ Area ($km^{2}$)')
        ax.set_ylabel(r'$Log_{10}$ Species Count')
        fig.colorbar(im, ax=ax, label=r"$Log_{10}$ checklists submitted on landmass", orientation="horizontal")
        plt.savefig('figures/outputs/island_species_counts_by_checklists.png')

    if True:
        # by observers
        fig, ax = plt.subplots()
        im = ax.scatter(
            counts_and_areas['area_km2'],
            counts_and_areas['species_count'], 
            c=np.log(counts_and_areas['observer_count']),
            cmap='viridis',
            s=4)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title('2024 Island Species Counts')
        ax.set_xlabel(r'$Log_{10}$ Area ($km^{2}$)')
        ax.set_ylabel(r'$Log_{10}$ Species Count')

        fig.colorbar(im, ax=ax, label=r"$Log_{10}$ observer count on landmass", orientation="horizontal")
        plt.savefig('figures/outputs/island_species_counts_by_observers.png')

    if True:
        # checklists per km2
        fig, ax = plt.subplots()
        im = ax.scatter(
            counts_and_areas['area_km2'],
            counts_and_areas['species_count'], 
            c=np.log(counts_and_areas['checklists_per_km2']),
            cmap='cividis',
            s=4)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title('2024 Island Species Counts')
        ax.set_xlabel(r'$Log_{10}$ Area ($km^{2}$)')
        ax.set_ylabel(r'$Log_{10}$ Species Count')

        fig.colorbar(im, ax=ax, label="r$Log_{10}$ checklists per $km^2$ on landmass", orientation="horizontal")
        
        plt.savefig('figures/outputs/island_species_counts_by_checklists_per_km2.png')

    if True:
        # observers per km2
        fig, ax = plt.subplots()
        im = ax.scatter(
            counts_and_areas['area_km2'],
            counts_and_areas['species_count'], 
            c=np.log(counts_and_areas['observers_per_km2']),
            cmap='cividis',
            s=4)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title('2024 Island Species Counts')
        ax.set_xlabel(r'$Log_{10}$ Area ($km^{2}$)')
        ax.set_ylabel(r'$Log_{10}$ Species Count')

        fig.colorbar(im, ax=ax, label="r$Log_{10}$ observers per $km^2$ on landmass", orientation="horizontal")
        plt.savefig('figures/outputs/island_species_counts_by_observers_per_km2.png')
    return

if __name__=="__main__":
    main()