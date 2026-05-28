import math
import os
import pandas as pd

standard_recipe = {
    'fkc': 30,
    'm9': 10,
    'auxin': 10,
}

no_auxin_recipe = {
    'fkc': 30,
    'm9': 20,
}

min_lifespan_recipe = {
    'kc': 16,
    'm9': 24,
}

lifespan_recipe = {
    'kc': 16,
    'm9': 16,
    'auxin': 8,
}

os.makedirs('outputs', exist_ok=True)

def get_stock_concentration(plate_concentration):
    log_val = math.log10(plate_concentration)
    exponent = math.ceil(round(log_val, 10))
    return 10 ** exponent

def get_m9_auxin_volumes(plate_concentration, total_volume=20):
    stock_concentration = get_stock_concentration(plate_concentration)
    auxin_volume = plate_concentration / stock_concentration * (total_volume / 2)
    m9_volume = total_volume - auxin_volume
    return auxin_volume, m9_volume

def recipe_calculator(plate_concentration, plates):
    if plate_concentration == 0:
        scaled_recipe = {key: value * plates for key, value in no_auxin_recipe.items()}
    else:
        stock_concentration = get_stock_concentration(plate_concentration)
        auxin_volume, m9_volume = get_m9_auxin_volumes(plate_concentration, total_volume=20)
        recipe = {**standard_recipe, 'm9': m9_volume, 'auxin': auxin_volume}
        scaled_recipe = {key: value * plates for key, value in recipe.items()}
        stock_key = str(stock_concentration) + 'M auxin'
        scaled_recipe[stock_key] = scaled_recipe.pop('auxin')

    return scaled_recipe

def lifespan_recipe_calculator(plate_concentration, plates):
    if plate_concentration == 0:
        scaled_recipe = {key: value * plates for key, value in min_lifespan_recipe.items()}
    else:
        stock_concentration = get_stock_concentration(plate_concentration)
        auxin_volume, m9_volume = get_m9_auxin_volumes(plate_concentration, total_volume=40)
        recipe = {**lifespan_recipe, 'm9': m9_volume, 'auxin': auxin_volume}
        scaled_recipe = {key: value * plates for key, value in recipe.items()}
        stock_key = str(stock_concentration) + 'M auxin'
        scaled_recipe[stock_key] = scaled_recipe.pop('auxin')

    return scaled_recipe

def add_units(row):
    exempt = {'plate_concentration (mM)', 'plates', 'lifespan'}
    return {f'{k} (uL)' if k not in exempt else k: v for k, v in row.items()}

all_results = []
filename = input('What would you like to name your output file? ')

while True:
    try:
        plate_concentration = float(input('What is the desired plate concentration (in mM)? '))
        plates = int(input('How many plates are you making? '))
    except ValueError:
        print('Error: please enter a valid number.')
        continue

    is_lifespan = input('Is this a lifespan plate? (y/n): ').lower() == 'y'

    if plate_concentration > 2 or plate_concentration < 0:
        print(f'Error: Plate concentration must be between 0 and 2mM.')
        continue

    if is_lifespan:
        result = lifespan_recipe_calculator(plate_concentration, plates)
    else:
        result = recipe_calculator(plate_concentration, plates)

    for ingredient, volume in result.items():
        print(f'  {ingredient}: {volume} uL')

    row = {'plate_concentration (mM)': plate_concentration, 'plates': plates, 'lifespan': is_lifespan, **result}
    all_results.append(add_units(row))

    again = input('\nCalculate another recipe? (y/n): ')
    if again.lower() != 'y':
        break

if all_results:
    df = pd.DataFrame(all_results).fillna(0)
    df.to_csv(f'outputs/{filename}.csv', index=False)
    print(f'Results saved to outputs/{filename}.csv')
else:
    print('No results to save.')