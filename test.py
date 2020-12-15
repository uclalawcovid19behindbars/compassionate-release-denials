import pandas as pd

d = {'col1': [1, 2], 'col2': [3, 4]}
df = pd.DataFrame(data=d)

def return_data(dat):
    return("column 1", dat['col1'], "column 2", dat['col2'])

return_data(df)