import math

standard_recipe = {
    'fkc': 30,
    'm9': 10,
    'auxin': 10,
}

no_auxin_recipe = {
    'fkc': 30,
    'm9': 20,
}

max_recipe = {
    'fkc': 30,
    '1M auxin': 20,
}

def get_stock_concentration(plate_concentration):
    log_val = math.log10(plate_concentration)
    exponent = math.ceil(round(log_val, 10))
    return 10 ** exponent

def get_m9_auxin_volumes(plate_concentration):
    stock_concentration = get_stock_concentration(plate_concentration)
    auxin_volume = plate_concentration / stock_concentration * 10
    m9_volume = 20 - auxin_volume
    return auxin_volume, m9_volume

def recipe_calculator(plate_concentration, plates):
    if math.isclose(plate_concentration, 0.1):
        scaled_recipe = {key: value * plates for key, value in standard_recipe.items()}
        scaled_recipe['1M auxin'] = scaled_recipe.pop('auxin')

    elif plate_concentration == 0:
        scaled_recipe = {key: value * plates for key, value in no_auxin_recipe.items()}

    elif math.isclose(plate_concentration, 2):
        scaled_recipe = {key: value * plates for key, value in max_recipe.items()}

    else:
        stock_concentration = get_stock_concentration(plate_concentration)
        auxin_volume, m9_volume = get_m9_auxin_volumes(plate_concentration)
        recipe = {**standard_recipe, 'm9': m9_volume, 'auxin': auxin_volume}
        scaled_recipe = {key: value * plates for key, value in recipe.items()}
        stock_key = str(stock_concentration) + 'M auxin'
        scaled_recipe[stock_key] = scaled_recipe.pop('auxin')

    return scaled_recipe

while True:
    try:
        plate_concentration = float(input('What is the desired plate concentration? '))
        plates = int(input('How many plates are you making? '))
    except ValueError:
        print('Error: please enter a valid number.')
        continue

    if plate_concentration > 2 or plate_concentration < 0:
        print('Error: concentration must be between 0 and 2mM.')
        continue

    result = recipe_calculator(plate_concentration, plates)
    for ingredient, volume in result.items():
        print(f'  {ingredient}: {volume} uL')

    again = input('\nCalculate another recipe? (y/n): ')
    if again.lower() != 'y':
        break