import yaml

# FIXME do better
with open('secrets.yaml', 'r') as file:
    SECRETS = yaml.safe_load(file)
