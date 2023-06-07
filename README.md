# <div align="center">Tactalyse Graph Generator</div>

#### <div align="center">Libraries for generating a graph from player match data.</div>

<div align="center">Authors: Mikko Brandon, Matteo Gennaro Giordano, Sangrok Lee, Bianca Raețchi</div>

## Table of Contents

* [About the Application](#about-the-application)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Running on Docker Container](#running-on-docker-container)
* [Endpoints](#endpoints)
* [Data Formatting](#data-formatting)
  * [Player Files](#player-files)
  * [League Files](#league-files)
* [Modules](#modules)
  * [controller](#controller)
  * [data](#data)
  * [graph_generator](#graph_generator)
* [Design](#design)
  * [MVC Pattern](#mvc-pattern)
  * [Factory Pattern](#factory-pattern)
* [Roadmap](#roadmap)

## About The Application

This repository's code was developed as part of the "Software Engineering" course at University of Groningen,  
which was undertaken in collaboration with Tactalyse. The project was designed to meet the requirements of both  
the course and Tactalyse as a company.  
The code functions as a backend API for generating graphs out of football player match data for Tactalyse's  
different graph bots. It was written in Python, and uses the Flask library as its web framework. Aside from a  
controller, the app has two distinct modules that are used to process the input data into a graph:

#### Data Preprocessing

The `data` module contains all functionality related to extracting data from  local Excel files into Pandas  
dataframes, and preprocessing the data for use in the other two modules. The processed data is passed back  
to the `controller`, which then sends it on to the other modules. As such, this essentially makes up our  
"Model" component in the MVC pattern. More on that can be found below in the [Design](#design) section.

#### Graph Generation

The `graph_generator` module contains all functionality related to generating graphs from data received  
from the `controller`, and outputting them in bytestring. Graph classes may contain additional data  
processing functions, strictly related to transforming values into formats that fit into the graphs, e.g.  
converting date strings to integer values for line plots. This makes up the "View" component.

## Getting Started

To get a local version of the API up and running follow these simple steps.

### Prerequisites

* [Python 3](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/) or a comparable Python package manager
* [Docker Desktop](https://docs.docker.com/desktop/)

### Installation

1. Install the newest version of Python.
2. Install your Python package manager of choice.
3. In this repository's root folder, run `pip install -r requirements.txt` (or a comparable call using another  
manager) to install the required Python libraries.
4. If you want to run the API on a container, install Docker Desktop, and run it.

### Running on Docker Container

1. In this repository's root folder, run `docker build -t test-image .` to create a Docker image. It should show  
up in Docker Desktop. `test-image` may be replaced by any name you wish to give the image.
2. Run `docker run -p 5001:5001 test-image`, or replace `test-image` with the name given in step 1.
3. The API should now be running on a container, visible in Docker Desktop. It can be accessed through  
http://localhost:5001/
4. Optionally, use an HTTP request tool such as Postman or Insomnia to make requests to the API.

## Endpoints

This section details the currently existing API endpoints, and their specifications.

#### POST /graph

Endpoint for generating a random graph. Currently, no parameters are required. However, the following parameters  
can be passed if you do not want them randomized:
- `graph-type`: String representing the type of graph that should be randomized. Currently supports ‘line’ and  
‘radar’.
- `league`: String representing the name of the league to use for radar graphs. The league must exist in the  
set of names of the local league files.
- `player`: String representing the name of the main player to graph stats for. For line graphs, the name must  
exist in the set of names of the local player files. For radar graphs, the name must exist in the file of the  
passed league.
- `compare`: String representing the name of the player to compare to in the generated graph. For line graphs,  
the name must exist in the set of names of the local player files. For radar graphs, the name must exist in the  
file of the passed league.
- `stat`: String representing the stat to graph for line graphs. The stat name must exist in the set of stats  
contained in the player files.
- `start-date`: String representing the starting date of Tactalyse’s services for the main player in YYYY-MM-DD  
format.
- `end-date`: String representing the ending date of Tactalyse’s services for the main player in YYYY-MM-DD  
format.

#### POST /graph/radar

Endpoint for generating a radar graph. Currently, no parameters are required. However, the following parameters  
can be passed if you do not want them randomized:
- `league`: String representing the name of the league to use for radar graphs. The league must exist in the  
set of names of the local league files.
- `player`: String representing the name of the main player to graph stats for. For line graphs, the name must  
exist in the set of names of the local player files. For radar graphs, the name must exist in the file of the  
passed league. NOTE: will cause an error if league was not passed and the player is not in the randomized league.
- `compare`: String representing the name of the player to compare to in the generated graph. For line graphs,  
the name must exist in the set of names of the local player files. For radar graphs, the name must exist in the  
file of the passed league. NOTE: will cause an error if league was not passed and the player is not in the  
randomized league.

#### POST /graph/line

Endpoint for generating a line graph. Currently, no parameters are required. However, the following parameters  
can be passed if you do not want them randomized:
- `player`: String representing the name of the main player to graph stats for. For line graphs, the name must  
exist in the set of names of the local player files. For radar graphs, the name must exist in the file of the  
passed league.
- `compare`: String representing the name of the player to compare to in the generated graph. For line graphs,  
the name must exist in the set of names of the local player files. For radar graphs, the name must exist in the  
file of the passed league.
- `stat`: String representing the stat to graph for line graphs. The stat name must exist in the set of stats  
contained in the player files.
- `start-date`: String representing the starting date of Tactalyse’s services for the main player in YYYY-MM-DD  
format.
- `end-date`: String representing the ending date of Tactalyse’s services for the main player in YYYY-MM-DD  
format.

## Data Formatting

As mentioned, the input data for the reports comes from local Excel files. These Excel files are obtained from  
[Wyscout](https://wyscout.com/), a professional platform for football statistics and data. All endpoint requests  
rely on String values that detail the players and league to use for graph generation. The actual data is  
contained in the `app/files` folder. We make a distinction between two types of data files:

#### Player Files

Player files are Excel files that contain match data for a single player. Every row consists of data from a  
single match. These files can be found in `app/files/players`. The files are  
named "Player stats [...]". For endpoints that graph player match data, ensure that the passed `player` name  
and `compare` name both have a file containing that name. Additionally, the `stat` parameter must exist as a  
column header in the player files.  The randomized columns can be found in the `random_player_stat()` function  
from `graph_app/data/preprocessors/randomizer`. These can be updated to fit with changes in column names.

#### League Files

League files are Excel files that contain stat totals and averages for multiple players in the same football  
league. Every row represents one player, whose name is included in the `Player` column. It is important that  
both `player` and `compare` are included in this column for the file named after the passed `league` string.  
As such, it is also important that the passed `league` parameter reflects the name of the league file in  
`app/files/leagues`. The used columns per position can be found in `graph_app/data/preprocessors/preprocessor`,  
in the `league_category_dictionary()` function. These can be updated to fit with changes in column names.

## Modules

#### controller

When a frontend application interacts with our API, it needs an entry point. To keep functionality decoupled and  
make sure that modules only have one responsibility, the `controller` module was created. It contains all  
functionality related to dealing with incoming requests, and acts as an intermediary between the other modules  
of the API. As such, it does not contain any data processing. The module contains the `app.py` file, which is  
essentially the Flask app itself, and contains all endpoints. It also contains `Service` classes, which extract  
parameters from the endpoint request, and pass them on to `Connector` classes. Each endpoint has a dedicated  
`Service` class. `Connector` classes act as the communication channels between the app, and their dedicated  
modules. The `Connector` classes were designed to return parameter maps, to improve code extendability  
(new required parameters only need to be added to the map instead of every function signature).

#### data

Although it would be very convenient, data can unfortunately not directly be translated from an Excel file to  
desired graphs. First, the data needs to be extracted, and preprocessed to fit the specific graphs. To allow for  
this, the `data` module was created. It contains an `ExcelReader` class, which handles the extraction of data  
from Excel files into Pandas dataframes. The `Preprocessor` classes contain data processing functionality for  
each dedicated graph, as well as a `Randomizer` class, which handles the randomization of not-passed parameters.  
The only data processing that is not contained in these classes is processing to do with converting values from  
their literal representations to representations that can be used in plots, as exemplified in [About the  
Application](#about-the-application).

#### graph_generator

Once data has been extracted from a file into a dataframe and preprocessed, it is passed to the `graph_generator`  
module. This module contains all functionality for generating graphs. All graph implementations are found in the  
`graphs` subdirectory. They all extend the abstract `Graph` class from the `abstract_models` file. Each  
implementation has its own class and file, and an optional class for all functions that are not directly  
related to visual output, such as `line_plot_data_helper`. The graphs are implemented with Seaborn wherever  
possible, and extended with matplotlib when required functionality does not exist in Seaborn.  
The `factories` subdirectory contains `Factory` classes. See more on this in the [Design](#design) section.  
Currently, they are not used for much other than creating an instance of the intended graph. It was mostly  
included for code maintenance and extendability.

## Design

#### MVC Pattern

We have tried to adhere to the Model-View-Controller pattern as closely as possible. It aids in decoupling  
functionality, and ensuring single-responsibility modules. The `controller` module comprises the Controller  
component in its entirety, since it functions as a relay station between functions from other modules, and  
calls those for processing data, and generating visual output. The `data` module comprises the Model component,  
as it contains all functionality to do with handling data for non-visual purposes. The `graph_generator` module  
comprises the View component, as it generates visual output based on input data.

#### Factory Pattern

We utilize the factory pattern in `graph_generator`. Factories are used for initializing `Graph` classes. In the  
future, graphs may require several lines of code to set up, or even entire methods. To ensure that we keep the  
code readable and decouple responsibilities, we chose to implement the factory pattern. Even though the current  
`Factory` class is only used to create an instance of a graph with a single constructor call, they may save  
code space in the future.

## Roadmap

Due to the nature of the "Software Engineering" course and its timeframe, not all potential features have been  
implemented. Here, we outline potential future work on the code.

#### Update Local Files

The current state of the files used for generating graphs is quite poor. League file names were given based on  
what league the majority of the players seemed to play in, and many players in these files do not have enough  
data entries to fill a radar graph. Furthermore, the player files may be outdated, as they were copied from an  
old PDF generator codebase. As such, we urge immediate further development to focus on updating the files.

#### CSRF Protection

At the end of the course, the team was required to test the codebase using Sonarqube. Through this, we were  
alerted to security concerns, most pressing of which was a lack of CSRF protection. We tried to implement it in  
the last few remaining days, but it proved too much of a headache on top of the work that was still left to be  
done for the course. Although there may not be an immediate security risk involved with unauthorized use of the  
API, it is still important to protect the company's intellectual property. As such, we urge future development  
to focus on implementing such protection.

#### Deployment

As of the delivery of this project, deployment on the company's servers has not been taken into account. A  
dockerfile exists for local deployment, but that's it. As such, deployment will have to be handled "from  
scratch".

#### PUT Endpoint

In the given timeframe, we were unable to implement functionality for updating the local files used for graph  
generation. As such, they would currently have to be replaced manually. In theory, it should be possible to  
create functionality for passing a list of league files and a list of player files, and replacing the existing  
ones with those. Future development could focus on this.

#### Graphs

We hope to have provided a solid framework for the easy addition of more graph types. As such, potential future  
development could be focused on adding new graph types to the PDF. The existing graphs may also need some  
fine-tuning in accordance with the company owner's needs.
