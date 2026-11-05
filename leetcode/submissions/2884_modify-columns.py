import pandas as pd

def modifySalaryColumn(employees: pd.DataFrame) -> pd.DataFrame:
    salary_array = employees['salary'].to_numpy()
    np.multiply(salary_array, 2, out=salary_array)
    employees['salary'] = salary_array
    return employees