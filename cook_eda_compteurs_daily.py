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
top5 = (
    comptages
    .groupby('Identifiant du site de comptage')
    .agg({
        'Comptage horaire': 'sum'
    })
    .sort_values('Comptage horaire', ascending=False)
    .head(5)
)

top5

# %%
table = (
    comptages
    .assign(
        Jour = lambda df: df.datetime.dt.day_name(),
        Heure = lambda df: ( df.datetime.dt.hour + 2 ) % 24
    )
    .pivot_table(
        index='Heure',
        columns=["Identifiant du site de comptage", "Jour"],
        values = "Comptage horaire",
        aggfunc="mean"
    )
    [top5.index]
    # .plot
    # .line(
    #     subplots = True
    # )
)

table

# %%
fig, ax = plt.subplots(nrows=7, ncols=5, figsize=(18, 14), sharey=True)

for i, jour in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
    for j, compteur in enumerate(top5.index):
        (
            table
            [compteur]
            .pipe(lambda df: df[[c for c in df.columns if c != jour ]])
            .plot
            .line(
                ax=ax[i,j],
                drawstyle='steps',
                legend=False,
                color='#bbb'
            )
        )
        
        (
            table
            .swaplevel(axis=1)
            [jour]
            [[compteur]]
            .plot
            .line(
                ax=ax[i,j],
                drawstyle='steps',
                legend=False,
                color='black'
            )
        )
        
plt.tight_layout()


plt.show()

# %%
last_week = (
    comptages
    .assign(
        Jour = lambda df: df.datetime.dt.day_name(),
        Heure = lambda df: ( df.datetime.dt.hour + 2 ) % 24
    )
    .pivot_table(
        index = [comptages.datetime.dt.date, "Jour"],
        columns = ['Identifiant du site de comptage', 'Heure'],
        values = "Comptage horaire",
        #aggfunc='sum'
    )
    [top5.index]
    .iloc[-7:]
    .droplevel(0)
    .reset_index()
    .melt(id_vars="Jour")
    .pivot_table(
        index="Heure",
        columns=['Identifiant du site de comptage', "Jour"],
        values='value'
    )
)

last_week

# %%
fig, ax = plt.subplots(nrows=7, ncols=5, figsize=(18, 14), sharey=True)

for i, jour in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]):
    for j, compteur in enumerate(top5.index):
        (
            table
            .swaplevel(axis=1)
            [jour]
            [[compteur]]
            .plot
            .line(
                ax=ax[i,j],
                drawstyle='steps',
                legend=False,
                color='#bbb'
            )
        )
        
        (
            last_week
            #.swaplevel(axis=1)
            [compteur]
            [[jour]]
            .plot
            .line(
                ax=ax[i,j],
                drawstyle='steps',
                legend=False,
                color='black'
            )
        )
        
plt.tight_layout()


plt.show()

# %%
