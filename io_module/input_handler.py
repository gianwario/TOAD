import csv
import os
from datetime import datetime, date, timedelta
from utils import validate_date
from community import community, metrics, data
from console import console


def get_input_files():
    """
    This function prompts the user to insert the needed input/output files and the end date of the time window to analyze.
    :return: the input given by the user
    """

    # TODO REMOVE HARD CODED INPUT BEFORE FINAL COMMIT

    # input_path = console.input('[bold green]Please enter the path of the input file, including filename and its extension\n')

    input_path = "C:/Users/gianm/Desktop/master-thesis/input.csv"
    if not os.path.isfile(input_path):
        console.print("[bold red]Error, the file does not exist")
        raise SystemExit(0)
    # output_dir = console.input('[bold green]Please enter the directory path for the output file\n')
    output_dir = "C:/Users/gianm/Desktop/master-thesis"
    if not os.path.isdir(output_dir):
        console.print("[bold red]Error, the directory does not exist")
        raise SystemExit(0)
    # output_path = console.input('[bold green]Please enter the filename of the output file. Please do not include any extension, as it will be a csv file\n')
    output_path = "output"
    with open(os.path.join(output_dir, output_path + ".csv"), "w") as file:
        if not os.path.isfile(output_path + ".csv"):
            console.print("[bold red]There was an error creating the output file")
            raise SystemExit(0)
        dw = csv.DictWriter(
            file,
            delimiter=",",
            fieldnames=[
                "owner",
                "name",
                "start_date",
                "end_date",
                "SN",
                "NoP",
                "IN",
                "FN",
                "CoP",
                "PT",
                "FG",
                "IC",
            ],
        )
        dw.writeheader()

    return (
        input_path,
        os.path.join(output_dir, output_path + ".csv"),
    )


def get_input_communities(path: str):
    """
    This function gets the communities contained in the file specified by the user.

    :param path: the path of the csv containing communities
    :return: the list of communities contained in the file
    """
    communities = []
    start_date = None
    end_date = None
    with open(path, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")
        for row in reader:
            # TODO switch 0 and 1
            comm = community.Community(row[1], row[0])
            d = data.Data()
            end_date = row[2]
            if not validate_date(end_date):
                console.print("[bold red]Invalid date")
                raise SystemExit(0)
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            start_date = end_date - timedelta(days=90)
            d.start_date = start_date
            d.end_date = end_date
            comm.add_data(d)

            m = metrics.Metrics()
            m.dispersion = {}
            m.structure = {}
            m.engagement = {}
            m.formality = {}
            m.longevity = 0
            comm.add_metrics(m)
            communities.append(comm)

    return communities
