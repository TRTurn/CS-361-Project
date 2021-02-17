import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import wikipediaapi as wiki
import sys

if sys.argv[0]:
    pass
root = tk.Tk()

root.title("Content Generator")

primary_key = tk.Text(width=50, borderwidth=5, height=1, padx=20, pady=10)
primary_key.insert(1.0, "puppy")
primary_key.grid(row=0, column=0, pady=20)

secondary_key = tk.Text(width=50, borderwidth = 5, height=1, padx=20, pady=10)
secondary_key.insert(1.0, "dog")
secondary_key.grid(row=1, column=0)

output_box = tk.scrolledtext.ScrolledText(width=50, height=30, padx = 20, pady = 30, borderwidth=5)
output_box.insert(1.0, "Output will appear here")  # The 1.0 refers to line 1, character 0
output_box.grid(row=3, column=0, padx=20, pady=20)


# def generate_output():
#     keywords = primary_key.get(1.0, tk.END)[:-1].replace(" ", "").split(",")  # The -1 removes the newline token automatically included by tkinter
#     secondary_keyword = secondary_key.get(1.0, tk.END)
#     if len(keywords) > 2:
#         output_box.delete(1.0, tk.END)
#         output_box.insert(1.0, "Insert only two keywords")
#     elif keywords is None:
#         pass
#     elif len(keywords) == 1:
#         search_wikipedia(keywords[0])
#     else:
#         search_wikipedia(keywords[0], secondary_keyword)


def generate_output():
    primary_keyword = primary_key.get(1.0, tk.END)
    secondary_keyword = secondary_key.get(1.0, tk.END)
    if primary_keyword is None:
        pass
    else:
        search_wikipedia(primary_keyword[:-1], secondary_keyword[:-1])

def search_wikipedia(primary_keyword, secondary_keyword=None):
    wiki_search = wiki.Wikipedia('en')
    results = wiki_search.page(primary_keyword).text.splitlines()
    print(results)
    if secondary_keyword:
        for result in results:
            index = result.find(secondary_keyword)
            if index != -1:
                results = result
                break
            else:
                results = "Secondary Keyword Not Found" + results[0]
    else:
        results = results[0]
    output_box.delete(1.0, tk.END)
    output_box.insert(1.0, results)

def generate_csv():
    pass

output_generation_btn = tk.Button(root, text="Generate Output", padx=40, pady=20, command=generate_output)
output_generation_btn.grid(row=2, columnspan=2, pady=20)

root.mainloop()