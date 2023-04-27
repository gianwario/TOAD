import csv
import os
from datetime import datetime, date, timedelta
from utils import validate_date
from community import community
from console import console

def get_input_files():
    input_path = console.input('[bold green]Please enter the path of the input file, including filename and its extension\n')
    if not os.path.isfile(input_path):
        console.print("[bold red]Error, the file does not exist")
        raise SystemExit(0)
    output_dir = console.input('[bold green]Please enter the directory path for the output file\n')
    if not os.path.isdir(output_dir):
        console.print("[bold red]Error, the directory does not exist")
        raise SystemExit(0)
    output_path = console.input('[bold green]Please enter the filename of the output file. Please do not include any extension, as it will be a csv file\n')
    open(os.path.join(output_dir,output_path+".csv"), "w")
    if not os.path.isfile(output_path+".csv"):
        console.print("[bold red]There was an error creating the output file")
        raise SystemExit(0)
    end_date = console.input('[bold green]Enter end date of time window (YYYY-MM-DD) in UTC\n')
    if not validate_date(end_date):
        console.print("[bold red]Invalid date")
        raise SystemExit(0)
    start_date = datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=90)
    return input_path, output_path, start_date, end_date

def get_input_communities(path):
    communities = []
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            communities.append(community.Community(row[0], row[1]))
    return communities