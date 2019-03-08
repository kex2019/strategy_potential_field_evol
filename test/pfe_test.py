import potential_field_evolution.pfe as pfe
print("Starting evaluation")
pfe.evaluate(
    render=True,
    robots=4,
    spawn=10,
    capacity=1,
    shelve_length=2,
    shelve_width=2,
    shelve_height=2,
    steps=10000,
    periodicity_lower=450,
    periodicity_upper=550,
    generation_steps=1000,
    collect=True)
