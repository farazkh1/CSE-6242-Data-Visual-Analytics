########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = False

############### SAMPLE CLASS AND SQL QUERY ###########################
######################################################################
class Sample():
    def sample(self):
        try:
            connection = sqlite3.connect("sample")
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
        print('\033[32m' + "Sample: " + '\033[m')
        
        # Sample Drop table
        connection.execute("DROP TABLE IF EXISTS sample;")
        # Sample Create
        connection.execute("CREATE TABLE sample(id integer, name text);")
        # Sample Insert
        connection.execute("INSERT INTO sample VALUES (?,?)",("1","test_name"))
        connection.commit()
        # Sample Select
        cursor = connection.execute("SELECT * FROM sample;")
        print(cursor.fetchall())

######################################################################

class HW2_sql():
    ############### DO NOT MODIFY THIS SECTION ###########################
    ######################################################################
    def create_connection(self, path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            connection.text_factory = str
        except Error as e:
            print("Error occurred: " + str(e))
    
        return connection

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        try:
            if query == "":
                return "Query Blank"
            else:
                cursor.execute(query)
                connection.commit()
                return "Query executed successfully"
        except Error as e:
            return "Error occurred: " + str(e)
    ######################################################################
    ######################################################################

    # GTusername [0 points]
    def GTusername(self):
        gt_username = "your_gt_username"  # replace your GT_Username
        return gt_username
    
    def part_1_a_i(self,connection):
        part_1_a_i_sql = """
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title TEXT,
            score REAL
        );
        """
        return self.execute_query(connection, part_1_a_i_sql)
    
    def part_1_a_ii(self,connection):
        part_1_a_ii_sql = """
        CREATE TABLE movie_cast (
            movie_id INTEGER,
            cast_id INTEGER,
            cast_name TEXT,
            birthday TEXT,
            popularity REAL,
            PRIMARY KEY (movie_id, cast_id)
        );
        """
        return self.execute_query(connection, part_1_a_ii_sql)
    
    def part_1_b_movies(self, connection, path):
     with open(path, encoding="utf8") as f:
         reader = csv.reader(f)
         movielist = list(reader)
     for movie in movielist:
     #print(movie)
         connection.execute("INSERT INTO movies VALUES (?,?,?)",
                            (movie[0],movie[1], movie[2]))
     ######################################################################
     sql = "SELECT COUNT(id) FROM movies;"
     cursor = connection.execute(sql)
     return cursor.fetchall()[0][0]
 
    def part_1_b_movie_cast(self, connection, path):
        with open(path, encoding="utf8") as f:
            reader = csv.reader(f)
            cast_list = list(reader)
        for cast in cast_list:
        #print(movie)
            connection.execute("INSERT INTO movie_cast VALUES (?,?,?,?,?)",
                               (cast[0],cast[1], cast[2], cast[3], cast[4]))
        ######################################################################
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_1_c(self,connection):
        part_1_c_sql = """
        CREATE TABLE cast_bio (
            cast_id INTEGER PRIMARY KEY,
            cast_name TEXT,
            birthday TEXT,
            popularity REAL
        );
        """
        self.execute_query(connection, part_1_c_sql)
    
        part_1_c_insert_sql = """
        INSERT INTO cast_bio 
        SELECT DISTINCT cast_id, cast_name, birthday, popularity 
        FROM movie_cast;
        """
        self.execute_query(connection, part_1_c_insert_sql)
    
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_2_a(self,connection):
        part_2_a_sql = "CREATE INDEX movie_index ON movies(id);"
        return self.execute_query(connection, part_2_a_sql)

    def part_2_b(self,connection):
        part_2_b_sql = "CREATE INDEX cast_index ON movie_cast(cast_id);"
        return self.execute_query(connection, part_2_b_sql)

    def part_2_c(self,connection):
        part_2_c_sql = "CREATE INDEX cast_bio_index ON cast_bio(cast_id);"
        return self.execute_query(connection, part_2_c_sql)
    
    def part_3(self,connection):
        part_3_sql = """
        SELECT PRINTF('%.2f', 
            (CAST(COUNT(CASE WHEN score BETWEEN 7 AND 20 THEN 1 END) AS FLOAT) /  CAST(COUNT(*) AS FLOAT) * 100)
    ) 
        FROM movies;
        """
        cursor = connection.execute(part_3_sql)
        return cursor.fetchall()[0][0]
    
    def part_4(self, connection):
        part_4_sql = """
        SELECT cast_name, COUNT(movie_id) FROM movie_cast WHERE popularity > 10 GROUP BY cast_name ORDER BY COUNT(movie_id) DESC, cast_name LIMIT 5;
            """
        cursor = connection.execute(part_4_sql)
        return cursor.fetchall()

    def part_5(self, connection):
        part_5_sql = """
        SELECT
            title AS movie_title,
            printf('%.2f', CAST(score AS FLOAT)) AS movie_score,
            COUNT(cast_id) AS cast_count
        FROM
            movies
        INNER JOIN movie_cast ON movie_cast.movie_id = movies.id
        GROUP BY
            movies.id
        ORDER BY
            CAST(score AS FLOAT) DESC,
            COUNT(cast_id) DESC,
            title
        LIMIT
            5;
        """
        cursor = connection.execute(part_5_sql)
        return cursor.fetchall()

 
    def part_6(self, connection):
        part_6_sql = """
        SELECT
            movie_cast.cast_id,
            movie_cast.cast_name,
            printf('%.2f', AVG(CAST(movies.score AS FLOAT))) AS average_score
        FROM
            movie_cast
        INNER JOIN movies ON movies.id = movie_cast.movie_id
        WHERE
            movies.score >= 25
        GROUP BY
            movie_cast.cast_id
        HAVING COUNT(movie_cast.movie_id) > 2
        ORDER BY
            AVG(CAST(movies.score AS FLOAT)) DESC,
            movie_cast.cast_name
        LIMIT 10;
        """
        cursor = connection.execute(part_6_sql)
        return cursor.fetchall()



    def part_7(self, connection):
        part_7_sql = """
        CREATE VIEW good_collaboration AS
        SELECT 
            a.cast_id AS cast_member_id1, 
            b.cast_id AS cast_member_id2,
            COUNT(DISTINCT a.movie_id) AS movie_count,  -- Use DISTINCT to avoid duplicates
            AVG(m.score) AS average_movie_score
        FROM movie_cast a
        JOIN movie_cast b ON a.movie_id = b.movie_id
        JOIN movies m ON a.movie_id = m.id
        WHERE a.cast_id < b.cast_id  -- Prevent mirror pairs and self-pairs
        GROUP BY a.cast_id, b.cast_id
        HAVING movie_count >= 2 AND average_movie_score >= 40;  -- Fix: >= 2 instead of > 2
        """
        return self.execute_query(connection, part_7_sql)
 
 
    def part_8(self, connection):
        part_8_sql = """
        SELECT 
            combined.cast_id,
            cb.cast_name,
            PRINTF('%.2f', AVG(combined.average_movie_score)) AS collaboration_score
        FROM (
            SELECT cast_member_id1 AS cast_id, average_movie_score
            FROM good_collaboration
            UNION ALL
            SELECT cast_member_id2 AS cast_id, average_movie_score
            FROM good_collaboration
        ) AS combined
        JOIN cast_bio cb ON combined.cast_id = cb.cast_id
        GROUP BY combined.cast_id, cb.cast_name
        ORDER BY collaboration_score DESC, cb.cast_name ASC
        LIMIT 5;
        """
        cursor = connection.execute(part_8_sql)
        return cursor.fetchall()
    
    def part_9_a(self, connection, path):
    # SQL statement to create the FTS table
        part_9_a_sql = "CREATE VIRTUAL TABLE movie_overview USING fts5(id, overview);"
        connection.execute(part_9_a_sql)
    
    # Import data from the CSV file
        import csv
        with open(path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            # Assuming the CSV does not have a header row
            for row in csv_reader:
                connection.execute("INSERT INTO movie_overview (id, overview) VALUES (?, ?)", (row[0], row[1]))
    
    # Return the count of rows in the table
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]



     

    def part_9_b(self, connection):
        part_9_b_sql = """
        SELECT COUNT(id) 
        FROM movie_overview 
        WHERE overview MATCH '"fight"';
        """
        cursor = connection.execute(part_9_b_sql)
        return cursor.fetchall()[0][0]
    

    def part_9_c(self, connection):
    ############### EDIT SQL STATEMENT ###################################
        part_9_c_sql = """
        SELECT COUNT(id) FROM movie_overview WHERE overview MATCH 'space AND program';
        """
        ######################################################################
        cursor = connection.execute(part_9_c_sql)
        return cursor.fetchall()[0][0]

if __name__ == "__main__":

    if SHOW == True:
        sample = Sample()
        sample.sample()

    print('\033[32m' + "Q2 Output: " + '\033[m')
    db = HW2_sql()
    try:
        conn = db.create_connection("Q2")
    except:
        print("Database Creation Error")

    try:
        conn.execute("DROP TABLE IF EXISTS movies;")
        conn.execute("DROP TABLE IF EXISTS movie_cast;")
        conn.execute("DROP TABLE IF EXISTS cast_bio;")
        conn.execute("DROP VIEW IF EXISTS good_collaboration;")
        conn.execute("DROP TABLE IF EXISTS movie_overview;")
    except Exception as e:
        print("Error in Table Drops")
        print(e)

    try:
        print('\033[32m' + "part 1.a.i: " + '\033[m' + str(db.part_1_a_i(conn)))
        print('\033[32m' + "part 1.a.ii: " + '\033[m' + str(db.part_1_a_ii(conn)))
    except Exception as e:
         print("Error in Part 1.a")
         print(e)

    try:
        print('\033[32m' + "Row count for Movies Table: " + '\033[m' + str(db.part_1_b_movies(conn,"data/movies.csv")))
        print('\033[32m' + "Row count for Movie Cast Table: " + '\033[m' + str(db.part_1_b_movie_cast(conn,"data/movie_cast.csv")))
    except Exception as e:
        print("Error in part 1.b")
        print(e)

    try:
        print('\033[32m' + "Row count for Cast Bio Table: " + '\033[m' + str(db.part_1_c(conn)))
    except Exception as e:
        print("Error in part 1.c")
        print(e)

    try:
        print('\033[32m' + "part 2.a: " + '\033[m' + db.part_2_a(conn))
        print('\033[32m' + "part 2.b: " + '\033[m' + db.part_2_b(conn))
        print('\033[32m' + "part 2.c: " + '\033[m' + db.part_2_c(conn))
    except Exception as e:
        print("Error in part 2")
        print(e)

    try:
        print('\033[32m' + "part 3: " + '\033[m' + str(db.part_3(conn)))
    except Exception as e:
        print("Error in part 3")
        print(e)

    try:
        print('\033[32m' + "part 4: " + '\033[m')
        for line in db.part_4(conn):
            print(line[0],line[1])
    except Exception as e:
        print("Error in part 4")
        print(e)

    try:
        print('\033[32m' + "part 5: " + '\033[m')
        for line in db.part_5(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 5")
        print(e)

    try:
        print('\033[32m' + "part 6: " + '\033[m')
        for line in db.part_6(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 6")
        print(e)
    
    try:
        print('\033[32m' + "part 7: " + '\033[m' + str(db.part_7(conn)))
        print("\033[32mRow count for good_collaboration view:\033[m", conn.execute("select count(*) from good_collaboration").fetchall()[0][0])
        print('\033[32m' + "part 8: " + '\033[m')
        for line in db.part_8(conn):
            print(line[0],line[1],line[2])
    except Exception as e:
        print("Error in part 7 and/or 8")
        print(e)

    try:   
        print('\033[32m' + "part 9.a: " + '\033[m'+ str(db.part_9_a(conn,"/data/movie_overview.csv")))
        print('\033[32m' + "Count 9.b: " + '\033[m' + str(db.part_9_b(conn)))
        print('\033[32m' + "Count 9.c: " + '\033[m' + str(db.part_9_c(conn)))
    except Exception as e:
        print("Error in part 9")
        print(e)

    conn.close()