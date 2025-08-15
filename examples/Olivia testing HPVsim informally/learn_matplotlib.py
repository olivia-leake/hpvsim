#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 13:10:20 2025

@author: olivialeake
"""

# Pracitsing matplotlib.pyplot

# %%

# Line plot

from matplotlib import pyplot as plt

x_values = [1,2,3,4]
y_values = [5,4,6,2]

plt.plot(x_values, y_values)

plt.show()

# %%

# scatter plot

plt.scatter(x_values, y_values)

# %%

other_x_values = [1,2,3,4]
other_y_values = [4,2,3,9]

plt.plot(other_x_values, other_y_values, color ='red')

plt.title('sample plot')
plt.xlabel('xvalues')
plt.ylabel('yvalues')

# %%

import hpvsim as hpv

base = hpv.Sim().run()
base.results['cancers'] # This is given as an array as it gives the results
base.results['cancers'][-1] 
base.results['hpv_prevalence']
len(base.results['cancers']) # 36
len(base.results['hpv_prevalence']) # 36 both same length so suspect taken at time time-step

                 
sim = hpv.Sim()
multi= hpv.MultiSim(sim)
multi.run(n_runs=5)

multi.sims
# Out[81]: 
# [Sim("Sim 0"; 1995.0 to 2030.0; pop: 20000 default; epi: 8.24814e+08⚙, 512386♋︎),
#  Sim("Sim 1"; 1995.0 to 2030.0; pop: 20000 default; epi: 8.45642e+08⚙, 502543♋︎),
#  Sim("Sim 2"; 1995.0 to 2030.0; pop: 20000 default; epi: 7.13767e+08⚙, 435282♋︎),
#  Sim("Sim 3"; 1995.0 to 2030.0; pop: 20000 default; epi: 7.80586e+08⚙, 470827♋︎),
#  Sim("Sim 4"; 1995.0 to 2030.0; pop: 20000 default; epi: 7.63244e+08⚙, 457156♋︎)]

# Suppose we want to plot the final prevalence of HPV from each run
final_values = []

for s in multi.sims:
    # Extract the outcome of interest, e.g., prevalence at last time step
    # Replace 'prevalence' with the correct key in your simulation
    final_values.append(s.results['hpv_prevalence'][-1])

# Make a box plot
plt.figure(figsize=(6,4))
plt.boxplot(final_values)
plt.ylabel("HPV prevalence at final timestep")
plt.title("Distribution of final HPV prevalence across 5 runs")
plt.show()


# Results to extract

# KeyNotFoundError: odict key "incidence" not found; available keys are:
# infections
# infections_by_genotype
# infections_by_age
# dysplasias
# dysplasias_by_genotype
# dysplasias_by_age
# precins
# precins_by_genotype
# precins_by_age
# cins
# cins_by_genotype
# cins_by_age
# cancers
# cancers_by_genotype
# cancers_by_age
# detected_cancers
# detected_cancers_by_genotype
# detected_cancers_by_age
# cancer_deaths
# cancer_deaths_by_genotype
# cancer_deaths_by_age
# detected_cancer_deaths
# detected_cancer_deaths_by_genotype
# detected_cancer_deaths_by_age
# reinfections
# reinfections_by_genotype
# reinfections_by_age
# reactivations
# reactivations_by_genotype
# reactivations_by_age
# n_susceptible
# n_susceptible_by_genotype
# n_infectious
# n_infectious_by_genotype
# n_inactive
# n_inactive_by_genotype
# n_normal
# n_normal_by_genotype
# n_cin
# n_cin_by_genotype
# n_cancerous
# n_cancerous_by_genotype
# n_infected
# n_infected_by_genotype
# n_abnormal
# n_abnormal_by_genotype
# n_latent
# n_latent_by_genotype
# n_precin
# n_precin_by_genotype
# n_detected_cancer
# n_detected_cancer_by_genotype
# n_screened
# n_screened_by_genotype
# n_cin_treated
# n_cin_treated_by_genotype
# n_cancer_treated
# n_cancer_treated_by_genotype
# n_vaccinated
# n_vaccinated_by_genotype
# n_tx_vaccinated
# n_tx_vaccinated_by_genotype
# n_infectious_by_age
# n_females_infectious_by_age
# n_susceptible_by_age
# n_precin_by_age
# n_cin_by_age
# hpv_incidence
# hpv_incidence_by_genotype
# hpv_incidence_by_age
# dysplasia_incidence
# dysplasia_incidence_by_genotype
# dysplasia_incidence_by_age
# cancer_incidence
# cancer_incidence_by_genotype
# cancer_incidence_by_age
# births
# other_deaths
# migration
# infections_by_sex
# other_deaths_by_sex
# asr_cancer_incidence
# asr_cancer_mortality
# precin_genotype_dist
# cin_genotype_dist
# cancerous_genotype_dist
# new_vaccinated
# new_total_vaccinated
# cum_vaccinated
# cum_total_vaccinated
# new_doses
# cum_doses
# new_txvx_doses
# new_tx_vaccinated
# cum_txvx_doses
# cum_tx_vaccinated
# new_screens
# new_screened
# new_cin_treatments
# new_cin_treated
# new_cancer_treatments
# new_cancer_treated
# cum_screens
# cum_screened
# cum_cin_treatments
# cum_cin_treated
# cum_cancer_treatments
# cum_cancer_treated
# detected_cancer_incidence
# cancer_mortality
# n_alive
# n_alive_by_sex
# n_alive_by_age
# n_females_alive_by_age
# cdr
# cbr
# hpv_prevalence
# hpv_prevalence_by_genotype
# hpv_prevalence_by_age
# precin_prevalence
# precin_prevalence_by_genotype
# precin_prevalence_by_age
# cin_prevalence
# cin_prevalence_by_genotype
# cin_prevalence_by_age
# female_hpv_prevalence_by_age
# lsil_prevalence
# lsil_prevalence_by_age
# year
# t

