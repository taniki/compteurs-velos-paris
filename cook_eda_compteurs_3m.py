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
import matplotlib.pyplot as plt

# %%
comptages = (
    pd
    .read_csv('datasets/comptages.csv')
    .assign(
        datetime = lambda df: pd.to_datetime(df["Date et heure de comptage"], utc=True, errors='coerce')
    )
)
    
comptages

# %%
compteurs = (
    pd
    .read_csv('datasets/compteurs.csv')
    .groupby('Identifiant du site de comptage')
    .first()
    [['Nom du site de comptage']]
)
    
compteurs

# %%
comptages.datetime.dt.to_period('d')

# %%
table = (
    comptages
    .pivot_table(
        index   = comptages.datetime.dt.to_period('d'),
        columns = 'Identifiant du site de comptage',
        values  = 'Comptage horaire',
        aggfunc = 'sum'
    )
)

table

# %%
(
    table
    [table.sum().sort_values(ascending=False).head(5).index]
    .rename(
        lambda c: compteurs.loc[c]["Nom du site de comptage"],
        axis=1
    )
    .loc['2023-04':]
    .plot
    .line(
        drawstyle='steps-post',
        sharey=True,
        subplots=True,
        figsize=(15,10),
        color='black'
    )
)

# %%
fig, ax = plt.subplots(figsize=(15,10))

(
    table
    .loc['2023-04':]
    [table.sum().sort_values(ascending=False).head(5).index]
    .rename(
        lambda c: compteurs.loc[c]["Nom du site de comptage"],
        axis=1
    )
    .assign(
        Jour = lambda df: df.index.astype('datetime64[ns]').weekday,
        Semaine = lambda df: df.index.astype('datetime64[ns]').strftime('%Y-%U')
    )
    .groupby('Jour')
    .mean()    
    .plot
    .line(
        ax=ax,
        marker="o",
        sharey=True,
        subplots=True,
        color='black'
    )
)

# %%
(
    table
    .loc['2023-04':]
    [table.sum().sort_values(ascending=False).head(5).index]
    .assign(
        Jour = lambda df: df.index.astype('datetime64[ns]').weekday,
        Semaine = lambda df: df.index.astype('datetime64[ns]').strftime('%Y-%U')
    )
    .plot
    .line(
        x = "Jour",
        color='#666',
        alpha=.2,
        marker="o",
        sharey=True,
        subplots=True,
        figsize=(15,10),
    )
)

# %%
