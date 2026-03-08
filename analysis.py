import pandas as pd


# DATASET 1: NASA Planets


planets = pd.read_csv('planets.csv')
planets.replace('Unknown', pd.NA, inplace=True)

# Melt into tidy long format
planets_tidy = planets.melt(id_vars='Planet', var_name='Property', value_name='Value')

# Planets ranked by gravity
gravity = planets_tidy[planets_tidy['Property'] == 'Gravity (m/s^2)'].copy()
gravity['Value'] = pd.to_numeric(gravity['Value'])
gravity = gravity.sort_values('Value', ascending=False).reset_index(drop=True)
print("Planets ranked by surface gravity:")
print(gravity[['Planet', 'Value']].to_string(index=False))

print()

# Planets ranked by number of moons
moons = planets_tidy[planets_tidy['Property'] == 'Number of Moons'].copy()
moons['Value'] = pd.to_numeric(moons['Value'])
moons = moons.sort_values('Value', ascending=False).reset_index(drop=True)
print("Planets ranked by number of moons:")
print(moons[['Planet', 'Value']].to_string(index=False))

print()

# Hottest and coldest
temps = planets_tidy[planets_tidy['Property'] == 'Mean Temperature (C)'].copy()
temps['Value'] = pd.to_numeric(temps['Value'])
print(f"Average temperature across all planets: {temps['Value'].mean():.1f} C")
print(f"Hottest: {temps.loc[temps['Value'].idxmax(), 'Planet']} at {temps['Value'].max()} C")
print(f"Coldest: {temps.loc[temps['Value'].idxmin(), 'Planet']} at {temps['Value'].min()} C")



# DATASET 2: Box Office Mojo (2000-2024)


print("\n" + "-"*50)

box_office = pd.read_csv('box_office.csv')

# Yearly totals
yearly = box_office[['Year', 'Total Gross (USD)', 'Releases', 'Average Gross (USD)']].copy()
yearly['Total Gross (USD)'] = pd.to_numeric(yearly['Total Gross (USD)'], errors='coerce')
yearly['Average Gross (USD)'] = pd.to_numeric(yearly['Average Gross (USD)'], errors='coerce')

# Top films — melt from wide to long
frames = []
for rank in range(1, 6):
    temp = box_office[['Year', f'#{rank} Release', f'#{rank} Gross (USD)']].copy()
    temp.columns = ['Year', 'Film', 'Gross']
    temp['Rank'] = rank
    frames.append(temp)

top_films = pd.concat(frames, ignore_index=True)
top_films['Gross'] = pd.to_numeric(top_films['Gross'], errors='coerce')
top_films = top_films[['Year', 'Rank', 'Film', 'Gross']].sort_values(['Year', 'Rank']).reset_index(drop=True)

# Best and worst years
print("Best year at the box office:")
print(yearly.loc[yearly['Total Gross (USD)'].idxmax(), ['Year', 'Total Gross (USD)']])
print()
print("Worst year at the box office:")
print(yearly.loc[yearly['Total Gross (USD)'].idxmin(), ['Year', 'Total Gross (USD)']])

print()

# Top 10 films
print("Top 10 highest grossing films (2000-2024):")
print(top_films.nlargest(10, 'Gross')[['Year', 'Film', 'Gross']].to_string(index=False))

print()

# Pre vs post COVID
pre_covid = yearly[yearly['Year'] < 2020]['Total Gross (USD)'].mean()
post_covid = yearly[yearly['Year'] > 2020]['Total Gross (USD)'].mean()
print(f"Average annual gross before COVID (2000-2019): ${pre_covid:,.0f}")
print(f"Average annual gross after COVID (2021-2024):  ${post_covid:,.0f}")
print(f"Change: {((post_covid - pre_covid) / pre_covid * 100):.1f}%")



# DATASET 3: NYC Population by Borough (1950-2040)


print("\n" + "-"*50)

nyc = pd.read_csv('nyc_population.csv')
nyc['Borough'] = nyc['Borough'].str.strip()

# Grab just the plain year columns and melt
year_cols = [str(y) for y in range(1950, 2050, 10)]
nyc_tidy = nyc[['Borough'] + year_cols].melt(id_vars='Borough', var_name='Year', value_name='Population')
nyc_tidy['Year'] = nyc_tidy['Year'].astype(int)
nyc_tidy['Population'] = pd.to_numeric(nyc_tidy['Population'], errors='coerce')
nyc_tidy = nyc_tidy.sort_values(['Borough', 'Year']).reset_index(drop=True)

# Borough populations in 2020
boroughs = nyc_tidy[nyc_tidy['Borough'] != 'NYC Total']
in_2020 = boroughs[boroughs['Year'] == 2020].sort_values('Population', ascending=False)
print("Borough populations in 2020:")
print(in_2020[['Borough', 'Population']].to_string(index=False))

print()

# Growth from 1950 to 2040
pop_1950 = boroughs[boroughs['Year'] == 1950].set_index('Borough')['Population']
pop_2040 = boroughs[boroughs['Year'] == 2040].set_index('Borough')['Population']
growth = pd.DataFrame({
    '1950': pop_1950,
    '2040 (projected)': pop_2040,
    '% Change': ((pop_2040 - pop_1950) / pop_1950 * 100).round(1)
})
print("Population change from 1950 to 2040 projection:")
print(growth.to_string())

print()

# NYC total by decade
nyc_total = nyc_tidy[nyc_tidy['Borough'] == 'NYC Total'].sort_values('Year')
print("Total NYC population by decade:")
print(nyc_total[['Year', 'Population']].to_string(index=False))
