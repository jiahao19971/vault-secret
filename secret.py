import dotenv, json, subprocess
import yaml
from cerberus import Validator

dotenv.load_dotenv()

def _open_config(config_name):
    with open(config_name, "r", encoding="utf-8") as stream:
      try:
        data = yaml.safe_load(stream)
        with open("config.json", "r", encoding="utf-8") as validation_rules:
          schema = json.load(validation_rules)
          v = Validator(schema)
          if v.validate(data, schema):
            print(
              "Validated config.yml and no issue has been found"
            )
            return data
          else:
            raise ValueError(v.errors)
      except ValueError as e:
        raise e
      except yaml.YAMLError as yamlerr:
        if hasattr(yamlerr, "problem_mark"):
          pm = yamlerr.problem_mark
          message = "Your file {} has an issue on line {} at position {}"
          format_message = message.format(pm.name, pm.line, pm.column)
          raise ValueError(format_message) from yamlerr
        else:
          message = "Something went wrong while parsing config.yaml file"
          raise ValueError(message) from yamlerr

if __name__ == "__main__":
  try:
    config = _open_config("config.yaml")
    for conf in config['secrets']:
      get_output = subprocess.check_output(["vlt","secrets", "get" ,"--plaintext", conf['key']]) 
      decoded = get_output.strip().decode()
      print(f"Patching secret {conf['key']}") 
      data = json.dumps({"data": {conf['key']: decoded}})
      patch_output = subprocess.check_output(["kubectl", "patch", "secret", config['name'], f'-p="{data}"', "-n", config['namespace'], "-v=1"])
      print(patch_output)
  except Exception as e:
      print(e)