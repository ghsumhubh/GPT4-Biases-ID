import os

def extract_first_number(s):
    # Initialize an empty string to hold the number
    num_str = ''
    # Start scanning the string
    for char in s:
        # If the current character is a digit or if we have already started
        # a number and the current character is a dot (for decimal numbers),
        # append it to num_str
        if char.isdigit():
            num_str += char
        # If we encounter a non-digit character after finding some digits,
        # stop the search as we have found our first number
        elif num_str:
            break
    # Convert the string to an integer or float, depending on its content
    if num_str:
        return int(num_str)
    else:
        return None
    


def get_all_csv_files_in_folder(folder):
    # Initialize an empty list to hold the file names
    csv_files = []
    # Iterate over all files in the folder
    for file in os.listdir(folder):
        # If the file is a CSV file, add its name to the list
        if file.endswith('.csv'):
            csv_files.append(file)
    
    if folder in ['responses/first_prompt/part a']: # bad output files
        csv_files = [file for file in csv_files if file != 'gpt_response2.csv']

    # order the list of files by extracting the first number in the file name
    csv_files.sort(key=extract_first_number)

    # concact the folder path to the file name
    csv_files = [os.path.join(folder, file) for file in csv_files]

    
    return csv_files



def get_all_csv_files_for_experiment(experiment, prompt='first'):
    prompt_name = f'{prompt}_prompt'
    base_path = f'responses/{prompt_name}'
    if experiment == 'part a':
        files = get_all_csv_files_in_folder(f'{base_path}/part a')
    
    elif experiment == 'part b':
        files = get_all_csv_files_in_folder(f'{base_path}/part a')
        files.extend(get_all_csv_files_in_folder(f'{base_path}/part b'))
    
    elif experiment == 'prompt 1 only gender':
        files = get_all_csv_files_in_folder(f'{base_path}/part a')
        files.extend(get_all_csv_files_in_folder(f'{base_path}/part b'))
        files.extend(get_all_csv_files_in_folder(f'{base_path}/part c/color'))
        files.extend(get_all_csv_files_in_folder(f'{base_path}/part c/utensil'))
        files.extend(get_all_csv_files_in_folder(f'{base_path}/part c/gibberish'))



    elif experiment == 'color':
        files = get_all_csv_files_in_folder(f'{base_path}/part c/color')
    
    elif experiment == 'utensil':
        files = get_all_csv_files_in_folder(f'{base_path}/part c/utensil')
    
    elif experiment == 'gibberish':
        files = get_all_csv_files_in_folder(f'{base_path}/part c/gibberish')

    return files
    