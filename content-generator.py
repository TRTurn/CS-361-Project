import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import wikipediaapi as wiki
import sys
import pandas as pd
import os
from os import path

def generate_output():
    """Retrieves input values and displays data corresponding to the values passed."""
    primary_keyword = primary_key.get(1.0, tk.END)
    secondary_keyword = secondary_key.get(1.0, tk.END)
    if primary_keyword is None or primary_keyword == 'Primary-Key':
        display_output('Please Enter Key')
    else:
        results = search_wikipedia(primary_keyword[:-1].strip(), secondary_keyword[:-1].strip())
        display_output(results)

        
def display_output(data):
    """Displays data on the Output Box within the GUI"""
    output_box.delete(1.0, tk.END)
    output_box.insert(1.0, data)
    
def search_wikipedia(primary_keyword, secondary_keyword=None):
    """Searches wikipedia for a page corresponding with the primary keyword.
    The secondary keyword is then used to find a paragraph containing both keywords"""
    wiki_search = wiki.Wikipedia('en')
    results = wiki_search.page(primary_keyword).text.splitlines()

    if secondary_keyword and secondary_keyword != "Secondary-Key":
        for paragraph in results:
            index = paragraph.find(secondary_keyword)
            if index != -1:
                return paragraph
        return 'Secondary Keyword Not Found'

    else:
        return results[0]

def generate_csv(output, primary_key, secondary_key):
    """Generates a CSV containing the passed keywords and their results"""
    if secondary_key == 'Secondary-Key':
        secondary_key = None
    data = {'input_keywords':[str(primary_key) + '; ' + str(secondary_key)],
            'output_content' :[output]}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv('output.csv', index=False)


def use_person_generator():
    if path.exists('pg-input.csv'):
        os.system("python person-generator.py pg-input.csv")

        person_generator_output = pd.read_csv('pg_output.csv')
        state_key = person_generator_output['input_state'].iloc[0]
        results = search_wikipedia(state_key, 'temperature')
        display_output(results)
        primary_key.delete(1.0, tk.END)
        primary_key.insert(1.0, state_key)
        secondary_key.delete(1.0, tk.END)
        secondary_key.insert(1.0, 'Temperature')

    else:
        display_output('No person generator file')
        
    
if __name__ == '__main__':
    # If a csv is passed with the command line generate CSV directly
    if len(sys.argv) > 1:
        df = pd.read_csv(sys.argv[1])
        keywords = list(df['input_keywords'])[0].split(';')
        output = search_wikipedia(keywords[0], keywords[1])
        generate_csv(output, keywords[0], keywords[1])

    else:  # Create GUI

        # Working with other generator
        root = tk.Tk()

        # Window Title
        root.title("Content Generator")

        # Primary Key Text Box
        primary_label = tk.Label(root, text='Primary-Key')
        primary_label.config(font=24)
        primary_label.grid(row=0, column=0, pady=(10,0))
        primary_key = tk.Text(width=50, borderwidth=5, height=1, padx=20)
        primary_key.insert(1.0, "Primary-Key")
        primary_key.grid(row=1, column=0, pady=10)

        # Secondary Key Text Box
        secondary_label = tk.Label(root, text='Secondary-Key')
        secondary_label.config(font=24)
        secondary_label.grid(row=2, column=0, pady=(10, 0))
        secondary_key = tk.Text(width=50, borderwidth=5, height=1, padx=20, pady=5)
        secondary_key.insert(1.0, "Secondary-Key")
        secondary_key.grid(row=3, column=0)

        # Output Text Box
        output_label = tk.Label(root, text='Output')
        output_label.config(font=24)
        output_label.grid(row=4, column=0, pady=(10, 0))
        output_box = tk.scrolledtext.ScrolledText(width=50, height=30, padx=20, pady=15, borderwidth=5)
        output_box.insert(1.0, "Output will appear here after request")
        output_box.grid(row=5, column=0, padx=20, pady=15)

        # Output Generation Button
        output_generation_btn = tk.Button(root, text="Generate Output", padx=40, pady=15, command=generate_output)
        output_generation_btn.grid(row=6, columnspan=2, pady=10)

        # CSV Generation Button
        csv_generation_btn = tk.Button(root, text="Generate CSV", padx=40, pady=20, command=lambda: generate_csv(search_wikipedia(primary_key.get(1.0, tk.END)[:-1], secondary_key.get(1.0, tk.END)[:-1]), primary_key.get(1.0, tk.END)[:-1], secondary_key.get(1.0, tk.END)[:-1]))
        csv_generation_btn.grid(row=7, columnspan=2, pady=10)


        # Person_Generation Button
        person_generation_btn = tk.Button(root, text="Use Person Generation Input", padx=40, pady= 15, command=use_person_generator)
        person_generation_btn.grid(row=8, columnspan=2, pady=10)

        root.mainloop()

