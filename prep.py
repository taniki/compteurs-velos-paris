# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pandas as pd

# %%
comptages = (
    pd
    .read_csv('/home/tk/Downloads/comptage-velo-donnees-compteurs.csv', sep=';')
    [[
        "Identifiant du compteur",
        "Identifiant du site de comptage",
        "Date et heure de comptage",
        "Comptage horaire",
    ]]
)

comptages

# %%
comptages.to_csv('datasets/comptages.csv', index=False)

# %%
compteurs = (
    pd
    .read_csv('/home/tk/Downloads/comptage-velo-donnees-compteurs.csv', sep=';')
    .groupby('Identifiant du compteur')
    .first()
    #.reset_index()
    [[
        "Nom du compteur",
        "Identifiant du site de comptage",
        "Nom du site de comptage",
        "Coordonnées géographiques"
    ]]
)

compteurs

# %%
compteurs.to_csv('datasets/compteurs.csv')

# %%
