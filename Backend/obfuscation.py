

import json


with open("schema_config.json", "r") as file:
    schema_map = json.load(file)




def get_fake_schema_description():
    """
    Builds a text description of the database structure using ONLY
    fake names -- but NOW includes a data-type hint per column
    (e.g. "text (person name)", "number (links to table_A col_A1)").

    This is the key upgrade: without type hints, Gemini was guessing
    blindly and picking wrong columns (e.g. confusing an ID column
    with a name column). The type hint gives just enough context to
    pick correctly, WITHOUT revealing the real column name.

    Returns a string like:
    table_A:
      - col_A1: number (unique id)
      - col_A2: text (person name)
      - col_A3: text (city name)
    """
    description_lines = []

    for real_table_name, fake_table_name in schema_map["tables"].items():
        description_lines.append(f"{fake_table_name}:")

        
        columns = schema_map["columns"][real_table_name]

        for real_col_name, col_info in columns.items():
            fake_name = col_info["fake_name"]
            col_type = col_info["type"]
            description_lines.append(f"  - {fake_name}: {col_type}")

    return "\n".join(description_lines)


def fake_to_real(sql_query):
    """
    Takes SQL written using FAKE names (from Gemini) and replaces every
    fake table/column name with its REAL equivalent, so it can be run
    on the actual MySQL database.

    Example input:  "SELECT col_A2 FROM table_A"
    Example output: "SELECT name FROM customers"
    """
    result = sql_query

    
    for real_table_name, columns in schema_map["columns"].items():
        for real_col_name, col_info in columns.items():
            fake_col_name = col_info["fake_name"]
           
            result = result.replace(fake_col_name, real_col_name)

   
    for real_table_name, fake_table_name in schema_map["tables"].items():
        result = result.replace(fake_table_name, real_table_name)

    return result


def real_to_fake(sql_query):
    """
    The OPPOSITE direction -- takes SQL with REAL names and converts it
    to FAKE names. We don't need this often, but it's useful for testing
    (so we can write a real query ourselves and confirm the obfuscation
    works correctly in both directions).
    """
    result = sql_query

    for real_table_name, fake_table_name in schema_map["tables"].items():
        result = result.replace(real_table_name, fake_table_name)

    for real_table_name, columns in schema_map["columns"].items():
        for real_col_name, col_info in columns.items():
            fake_col_name = col_info["fake_name"]
            result = result.replace(real_col_name, fake_col_name)

    return result



if __name__ == "__main__":
    print("---- Fake schema sent to AI ----")
    print(get_fake_schema_description())

    print("\n---- Testing real_to_fake ----")
    real_query = "SELECT name, city FROM customers WHERE city = 'Delhi'"
    fake_query = real_to_fake(real_query)
    print("Real query: ", real_query)
    print("Fake query: ", fake_query)

    print("\n---- Testing fake_to_real (reverse) ----")
    back_to_real = fake_to_real(fake_query)
    print("Back to real:", back_to_real)