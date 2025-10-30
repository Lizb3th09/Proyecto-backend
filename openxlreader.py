import openpyxl

def read_and_print_excel_data(file_path):
    """
    Reads all data from the first worksheet of an Excel file
    and prints it row by row.
    """
    try:
        # Load the workbook from the specified file path
        workbook = openpyxl.load_workbook(file_path)

        # Get the active worksheet (usually the first one)
        sheet = workbook.active

        print(f"Reading data from sheet: {sheet.title}")
        print("-" * 30)

        # Iterate through all rows in the worksheet
        # The .rows attribute provides an iterator of all rows
        for row in sheet.rows:
            # Create a list to hold the values of the current row
            row_data = []
            # Iterate through all cells in the current row
            for cell in row:
                # Append the value of the cell to the list
                row_data.append(cell.value)
            
            # Print the list of values for the current row
            print(row_data)

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Call the function with your file name
# Make sure 'your_file_name.xlsx' is in the same directory as the script
# or provide the full path to the file.
read_and_print_excel_data('db-ens-RL.xlsx')
