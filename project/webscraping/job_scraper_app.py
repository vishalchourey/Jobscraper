import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import time
import datetime

# it user define module
from scraper.naukri_scraper import naukri_job_scraper
from scraper.aijobs_scraper import job_data_scraper
from scraper.timesjobs_scraper import timesjob_scraper
from scraper.url_generator import custom_url 
from scraper.ai_jobs_url_generator import url_generator

def scrape_job_data(job_role, experience, location, page):
    # url generator for nukari.com
    new_url = custom_url(job_role, experience, location)
    # function calll naukri_job_scraper
    naukri = naukri_job_scraper(job_role, new_url, page)
    # url generator ai-job.net
    ai_url = url_generator(job_role)
    # function call ai_job_scraper
    ai_jobs = job_data_scraper(job_role, ai_url, page)



def search_jobs():
    job_role = job_role_entry.get()
    experience = experience_entry.get()
    location = location_entry.get()
    page = page_entry.get()
    scrape_job_data(job_role, experience, location, page)
    result_label.config(text= f"Data scraped and saved to '{job_role}_NaukriJobListing_{str(datetime.date.today())}.xlsx'")
    result_label1.config(text= f"Data scraped and saved to '{job_role}_Ai_JobListing_{str(datetime.date.today())}.xlsx'")


def browse_file():
    initial_dir = os.getcwd()  # Specify your desired initial directory here
    filename = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Excel files", "*.xlsx")])
    os.startfile(filename)  # Open the selected Excel file

# Create the main application window
root = tk.Tk()
root.title("Job Search Application")
head = tk.Label(text="Welcome to Job Scraper", font="SanFrancisco 16", pady=50)
head.pack()
# Styling
root.configure(background="#f0f0f0")
root.geometry('800x700+50-80')

style = ttk.Style(root)
style.configure('TLabel', background="#f0f0f0", font=('Arial', 12))
style.configure('TEntry', font=('Arial', 12))
style.configure('TButton', background="#4CAF50", foreground="Black", font=('Arial', 12))

# Create and pack widgets
job_role_label = ttk.Label(root, text="Job Role:")
job_role_label.pack(pady=5)
job_role_entry = ttk.Entry(root)
job_role_entry.pack(ipadx=50, pady=5)

experience_label = ttk.Label(root, text="Experience:")
experience_label.pack(pady=5)
experience_entry = ttk.Entry(root)
experience_entry.pack(ipadx=50, pady=5)

location_label = ttk.Label(root, text="Location:")
location_label.pack(pady=5)
location_entry = ttk.Entry(root)
location_entry.pack(ipadx=50, pady=5)

page_label = ttk.Label(root, text="Number of pages(optional):")
page_label.pack(pady=5)
page_entry = ttk.Entry(root)
page_entry.pack(ipadx=50, pady=5)

search_button = ttk.Button(root, text="Search", command=search_jobs)
search_button.pack(pady=10)

browse_button = ttk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=5)

result_label = ttk.Label(root, text="")
result_label.pack()

result_label1 = ttk.Label(root, text="")
result_label1.pack()


# Start the application
root.mainloop()