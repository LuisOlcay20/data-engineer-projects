import pandas as pd

def data_to_csv(data, fields, filename):
    """
    Converts data into a DataFrame and writes it to a CSV 
    """
    df = pd.DataFrame(data)
    df = df[fields]  
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data successfully written to {filename}")
