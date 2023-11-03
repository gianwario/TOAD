# TOAD - Towards Open-source community health Analysis and Diagnosis

## Introduction
TOAD is a social network analysis tool able to identify community patterns of an open-source GitHub project. It is able to classify 8 of the 13 community types most relevant by analyzing five key characteristics of open-source communities, namely (1) structure, (2) geodispersion, (3) formality, (4) engagement and (5) longevity.

## Content of the repository
This section contains a brief explaination of the content of this repository.

- the file *pattern_detection.py* contains the source code responsible of the main execution of the tool;
- the folder *thesis* contains the master thesis for which the tool has been implemented, providing insights and additional information:
- the folders *data* and *graphs* contain all the data computed by the tool for the repositories analyzed during its experimentation phase;
- the file *requirements.txt* contains all the dependencies needed to run the tool;
- all the other files and folders contain the source code of the tool.


## Detectable Community Patterns
This section contains the list of the detectable community patterns by TOAD.


Community Pattern | Definition
|---|---|
Informal Community (IC) | Usually sets of people part of an organization, with a common interest, often closely dependent on their practice. Informal interactions, usually across unbound distances.|
Community of Practice (CoP) | Groups of people sharing a concern, a set of problems, or a passion about a topic, who deepen their knowledge and expertise in this area by interacting frequently in the same geolocation. |
Formal Network (FN) | Members are rigorously selected and prescribed by management (often in the form of FG), directed according to corporate strategy and mission. |
Social Network (SN) | SNs can be seen as a supertype for all OSSs. To identify an SN, it is sufficient to split the structure of organizational patterns into macrostructure and microstructure. |
Informal Network (IN) | Looser networks of ties between individuals that happen to come in contact in the same context. Their driving force is the strength of the ties between members.|
Network of Practice (NoP) | A networked system of communication and collaboration connecting CoPs. Anyone can join. They span geographical and time distances alike. |
Formal Group (FG) | People grouped by corporations to act on (or by means of) them. Each group has an organizational goal, called mission. Compared to FN, no reliance on networking technologies, local in nature. |
Project Team (PT) | People with complementary skills who work together to achieve a common purpose for which they are accountable. Enforced by their organization and follow specific strategies or organizational guidelines.|



## Installation

The tool is executable through command line. In the Requirements section, you will find the softwares and helpers you will need to install the tool. We suggest you to use the same versions we used, which will be specified alongside the requirements.

### Requirements
- Python 3.11.3
- Git
- A GitHub account

### Installation Steps

- Clone the current repository on your system
- In our repository, find the *requirements.txt* file which contains the dependencies needed
- Create a virtual environment with the specified Python version and run the following command: *python -m venv .venv*
- Activate the environment and run the following command to install all the dependencies: *pip install -r requirements.txt*
- Create a file named *.env* in the main folder of the tool
- Within the *.env* file, insert the following information:
  ```
    CLIENT_ID = "f5fc77806e10b7e7d5f0" # This is the ID of the TOAD application registered on GitHub 
    SIMILARITY_MAX_DISTANCE = 0.4 # This threshold is used to control the similarity metric of authors' usernames in the alias extraction process
  ```
  

## Usage

### Authentication Process
Once you run the tool for the first time, you will be prompted with a request to log with your GitHub account. The tool will ask you to follow a link that will open in your browser, showing a GitHub login page. In such page, you will need to insert the code that the tool shows you in console. After such process, a Git Personal Access Token will be created and persisted locally in the *.env* file, allowing the tool to perform requests to the GitHub API also for future uses.

### Input file configuration
To use the tool, you will need to setup a *.csv* file containing the community/communities you want to analyze. Afterwards, you will have to provide the tool with the path on your disk to such file. This file must contain the information about the GitHub repository representing the community to analyze. The information needed are:
- The name of the owner of the repository
- The name of the repository
- The ending date of the 3-month time window that the tool will analyze

This file should look like follows:
```
owner1,name1,date1
owner2,name2,date2
```
For example, if you wanted to analyze the current repository in the 3 months of August, September and October you will need to provide the tool with an input file defined as follows:
```
gianwario,toad,31/10/2023
```

### Reading the output
After computing all the needed metrics, the tool will provide you with many useful information in addition to the community patterns computed. 

- In console, you will read all the community patterns and characteristics computed;
- In the folded *data* you will find a *json* file containing the value of each of the metrics computed by TOAD for your repository;
- In the folder *graph* you will find a weighted graph representing your community in two different formats: (1) a *pdf* file and (2) a *gexf* file that can be opened with the software Gephi;
- In the *output file* you specified at the beginning of the execution, you will find the community patterns computed.

