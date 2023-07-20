import dotenv, json, subprocess
import yaml
from cerberus import Validator
from base64 import b64encode

dotenv.load_dotenv()

def _open_config(config_name: str):
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

def b64encodestr(string: str):
  return b64encode(string.encode("utf-8")).decode()

if __name__ == "__main__":
  try:
    config = _open_config("config.yaml")
    for conf in config['secrets']:
      get_output = subprocess.check_output(["vlt","secrets", "get" ,"--plaintext", conf['key']]) 
      decoded = get_output.strip().decode()
      print(f"Patching secret {conf['key']}") 
      b64val = b64encodestr(decoded)
      cmd = f"""kubectl patch secret {config['name']} -p='{{"data":{{"{conf['value']}": "{b64val}"}}}}' -n {config['namespace']} -v=1"""
      patch_output = subprocess.check_output(cmd, shell=True)
      print(patch_output.strip().decode())
  except Exception as e:
      print(e)