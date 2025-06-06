import http.client
import json
import csv


#############################################################################################################################
# cse6242 
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for submission to Gradescope.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your nodes and edges .csv files.
#
#############################################################################################################################

class Graph:
    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str) -> None:
        """
        Add a node to the graph if it doesn't exist
        Remove commas from names as per requirements
        """
        name = name.replace(',', '')  # Remove commas from names
        if not any(node[0] == id for node in self.nodes):
            self.nodes.append((id, name))

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an undirected edge to the graph if it doesn't exist
        """
        if source != target:  # Prevent self-loops
            # Sort the source and target to maintain consistency for undirected edges
            edge = tuple(sorted([source, target]))
            if edge not in self.edges:
                self.edges.append(edge)

    def total_nodes(self) -> int:
        """
        Returns the total number of nodes in the graph
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Returns the total number of edges in the graph
        """
        return len(self.edges)

    def max_degree_nodes(self) -> dict:
        """
        Returns a dictionary of nodes with the highest degree
        """
        degree_count = {}
        for edge in self.edges:
            degree_count[edge[0]] = degree_count.get(edge[0], 0) + 1
            degree_count[edge[1]] = degree_count.get(edge[1], 0) + 1

        if not degree_count:
            return {}

        max_degree = max(degree_count.values())
        return {node: degree for node, degree in degree_count.items() 
                if degree == max_degree}

    # Do not modify
    def write_nodes_file(self, path="nodes.csv") -> None:
        """
        Write nodes to a CSV file
        """
        with open(path, 'w', encoding='utf-8', newline='') as nodes_file:
            nodes_file.write("id,name\n")
            for n in self.nodes:
                nodes_file.write(f"{n[0]},{n[1]}\n")
        print("finished writing nodes to csv")

    # Do not modify
    def write_edges_file(self, path="edges.csv") -> None:
        """
        Write edges to a CSV file
        """
        with open(path, 'w', encoding='utf-8', newline='') as edges_file:
            edges_file.write("source,target\n")
            for e in self.edges:
                edges_file.write(f"{e[0]},{e[1]}\n")
        print("finished writing edges to csv")

class TMDBAPIUtils:
    # Do not modify
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list[int] = None) -> list:
               """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param string movie_id: a movie_id
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :param integer limit: maximum number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If after excluding, there are fewer cast members than the specified limit, then return the remaining members (excluding the ones whose order values are outside the limit range). 
            If cast members with 'order' attribute in the specified limit range have been excluded, do not include more cast members to reach the limit.
            If after excluding, the limit is not specified, then return all remaining cast members."
            e.g., if limit=5 and the actor whose id corresponds to cast member with order=1 is to be excluded,
            return cast members with order values [0, 2, 3, 4], not [0, 2, 3, 4, 5]
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ... ]
                Note that this is an example of the structure of the list and some of the fields returned by the API.
                The result of the API call will include many more fields for each cast member.
        """
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        try:
            url = f"/3/movie/{movie_id}/credits?api_key={self.api_key}&language=en-US"
            conn.request("GET", url)
            res = conn.getresponse()
            data = res.read()

            if res.status != 200:
                print(f"Error: Received status code {res.status} for movie_id {movie_id}")
                return []

            cast_data = json.loads(data.decode("utf-8"))["cast"]
            
            # Filter by order first
            if limit:
                cast_data = [cast for cast in cast_data if cast.get("order", float('inf')) < limit]
            
            # Then exclude specific IDs
            if exclude_ids:
                cast_data = [cast for cast in cast_data if cast["id"] not in exclude_ids]

            return cast_data

        except Exception as e:
            print(f"Error getting movie cast: {str(e)}")
            return []
        finally:
            conn.close()

    def get_movie_credits_for_person(self, person_id: str, start_date: str = None, end_date: str = None) -> list:
          """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param start_date: optional parameter to return the movie credit if the release date >= the specified date
            dates should be formatted like 'YYYY-MM-DD'
            e.g., if the start_date is '2024-01-01', then only return credits with a release_date on or after '2024-01-01'
        :param end_date: optional parameter to return the movie credit if the release date <= the specified date
            dates should be formatted like 'YYYY-MM-DD'
            e.g., if the end_date is '2024-01-01', then only return credits with a release_date on or before '2024-01-01'
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'release_date': '2024-01-01' # the string value of the release_date value for the credit}, ... ]
        
        IMPORTANT: You should format your dates like 'YYYY-MM-DD' e.g. '2024-01-29'.  You can assume the API will 
            format them in the same way. You can compare these as strings without doing any conversion.
        """
        conn = http.client.HTTPSConnection("api.themoviedb.org")
        try:
            url = f"/3/person/{person_id}/movie_credits?api_key={self.api_key}&language=en-US"
            conn.request("GET", url)
            res = conn.getresponse()
            data = res.read()

            if res.status != 200:
                print(f"Error: Received status code {res.status} for person_id {person_id}")
                return []

            credits_data = json.loads(data.decode("utf-8"))["cast"]
            filtered_credits = []

            for credit in credits_data:
                release_date = credit.get("release_date", "")
                if not release_date:
                    continue

                if start_date and release_date < start_date:
                    continue
                if end_date and release_date > end_date:
                    continue

                filtered_credits.append(credit)

            return filtered_credits

        except Exception as e:
            print(f"Error getting movie credits: {str(e)}")
            return []
        finally:
            conn.close()


#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' movies released in 1999.
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together in 1999.
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together in 1999.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the first 5 co-actors in each movie credit with a release date in 1999.
# Build your co-actor graph on the actor 'Laurence Fishburne' w/ person_id 2975.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your nodes.csv and edges.csv files.
#
# GRAPH SIZE
# Since the TMDB API is a live database, the number of nodes / edges in the final graph will vary slightly depending on when
# you execute your graph building code. We take this into account by rebuilding the solution graph every few days and
# updating the auto-grader.  We compare your graph to our solution with a margin of +/- 200 for nodes and +/- 300 for edges.
# 
# e.g., if the current solution contains 507 nodes then the min/max range is 307-707.
# The same method is used to calculate the edges with the exception of using the aforementioned edge margin.
# ----------------------------------------------------------------------------------------------------------------------
# BEGIN BUILD CO-ACTOR NETWORK
#
# INITIALIZE GRAPH
#   Initialize a Graph object with a single node representing Laurence Fishburne
#
# BEGIN BUILD BASE GRAPH:
#   Find all of Laurence Fishburne's movie credits that have a release date in 1999.
#   FOR each movie credit:
#   |   get the movie cast members having an 'order' value between 0-4 (these are the co-actors)
#   |
#   |   FOR each movie cast member:
#   |   |   using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#   |   |   using graph.add_edge(), add an edge between the Laurence Fishburne (actor) node
#   |   |   and each new node (co-actor/co-actress)
#   |   END FOR
#   END FOR
# END BUILD BASE GRAPH
#
#
# BEGIN LOOP - DO 2 TIMES:
#   IF first iteration of loop:
#   |   nodes = The nodes added in the BUILD BASE GRAPH (this excludes the original node of Laurence Fishburne!)
#   ELSE
#   |    nodes = The nodes added in the previous iteration:
#   ENDIF
#
#   FOR each node in nodes:
#   |  get the movie credits for the actor that have a release date in 1999.
#   |
#   |   FOR each movie credit:
#   |   |   try to get the 5 movie cast members having an 'order' value between 0-4
#   |   |
#   |   |   FOR each movie cast member:
#   |   |   |   IF the node doesn't already exist:
#   |   |   |   |    add the node to the graph (track all new nodes added to the graph)
#   |   |   |   ENDIF
#   |   |   |
#   |   |   |   IF the edge does not exist:
#   |   |   |   |   add an edge between the node (actor) and the new node (co-actor/co-actress)
#   |   |   |   ENDIF
#   |   |   END FOR
#   |   END FOR
#   END FOR
# END LOOP
#
# Your graph should not have any duplicate edges or nodes
# Write out your finished graph as a nodes file and an edges file using:
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# END BUILD CO-ACTOR NETWORK
# ----------------------------------------------------------------------------------------------------------------------

# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. If you continue to experience 'ConnectionRefusedError : [Errno 61] Connection refused',
#   - wait a while and then try again.  It may be necessary to insert periodic sleeps when you are building your graph.


def build_co_actor_network(api_key: str):
    """Build the co-actor network for Laurence Fishburne's 1999 movies."""
    tmdb = TMDBAPIUtils(api_key)
    graph = Graph()
    
    # Add initial node (Laurence Fishburne)
    graph.add_node(id='2975', name='Laurence Fishburne')
    
    # Get Fishburne's 1999 movies
    base_credits = tmdb.get_movie_credits_for_person(
        person_id='2975',
        start_date='1999-01-01',
        end_date='1999-12-31'
    )
    
    # First iteration: Add immediate co-actors
    new_nodes = set()
    for movie in base_credits:
        cast = tmdb.get_movie_cast(movie_id=str(movie['id']), limit=5)
        for member in cast:
            member_id = str(member['id'])
            if member_id != '2975':  # Don't add Fishburne again
                member_name = member['name'].replace(',', '')  # Remove commas from names
                graph.add_node(member_id, member_name)
                graph.add_edge('2975', member_id)
                new_nodes.add(member_id)
    
    # Second and third iterations
    for iteration in range(2):
        current_nodes = new_nodes
        new_nodes = set()
        
        for actor_id in current_nodes:
            credits = tmdb.get_movie_credits_for_person(
                person_id=actor_id,
                start_date='1999-01-01',
                end_date='1999-12-31'
            )
            
            for movie in credits:
                cast = tmdb.get_movie_cast(movie_id=str(movie['id']), limit=5)
                for member in cast:
                    member_id = str(member['id'])
                    member_name = member['name'].replace(',', '')
                    if member_id not in [node[0] for node in graph.nodes]:
                        graph.add_node(member_id, member_name)
                        new_nodes.add(member_id)
                    graph.add_edge(actor_id, member_id)
    
    return graph

def return_name() -> str:
    """Returns the current user's login name."""
    return 'your GT login name' # Replace with your GT login name

if __name__ == "__main__":
    api_key = 'your API key'  # Replace with your API key
    print(f"User: {return_name()}")
    
    # Build the network
    graph = build_co_actor_network(api_key)
    
    # Write the results to files
    graph.write_nodes_file()
    graph.write_edges_file()