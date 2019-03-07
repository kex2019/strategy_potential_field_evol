import potential_field_evolution.pfe as pfe
print("Starting evaluation")
pfe.evaluate(
    render=True,
    robots=1,
    spawn=4,
    capacity=1,
    shelve_length=2,
    shelve_width=2,
    shelve_height=2,
    steps=10000,
    periodicity_lower=150,
    periodicity_upper=200,
    collect=True)
