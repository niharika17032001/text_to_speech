import pandas as pd
import json


def read_excel( excel_file):
    df = pd.read_excel(excel_file)
    data = df.to_dict('records')
    return data

def read_json_as_list(json_file):
  # Open and read the JSON file
  with open(json_file, 'r') as file:
      data = json.load(file)
  return data
    
def read_json(json_file):
  df=pd.read_json(json_file)
  data=df.to_dict('records')
  return data
def write_list_to_json(data_list, file_path):

    with open(file_path, 'w') as file:
        json.dump(data_list, file, indent=4)
        
def read_json_into_table(json_file):
  df=pd.read_json(json_file)
  data=df.to_dict('records')
  return df

def read_list_into_table(data):
  df = pd.DataFrame(data)
  return df


def excel_to_json(json_file, excel_file):

    df = pd.read_excel(excel_file)
    data = df.to_dict('records')
    with open(json_file, 'w') as jf:
      json.dump(data, jf, indent=4)
    return data

def json_to_excel(json_file, excel_file):
  with open(json_file, 'r') as f:
    data = json.load(f)

  df = pd.DataFrame(data)
  df.to_excel(excel_file, index=False)
  
if __name__ == "__main__":
  json_file = 'voices.json'
  excel_file = 'voices.xlsx'
  # json_to_excel(json_file, excel_file)
  # excel_to_json(json_file, excel_file)
  print(read_json_into_table(json_file))
    



