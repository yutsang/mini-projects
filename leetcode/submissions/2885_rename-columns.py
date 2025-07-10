import pandas as pd

def renameColumns(students: pd.DataFrame) -> pd.DataFrame:
    column_names = ["student_id", "first_name", "last_name", "age_in_years"]
    students.columns = column_names
    return students
    