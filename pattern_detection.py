import requests
from io_module import input_handler

def main():

    communities = input_handler.get_input_communities("./input.csv")
    #response = requests.get('https://api.github.com/user/repos', auth=('gianwario', pat)) 
    #my_projects = response.json()
    #for project in my_projects:
    #    print(f"Project Name: {project['name']}\nProject URL    {project['html_url']}\n")

if __name__ == "__main__":
    main()