########################### DO NOT MODIFY THIS SECTION ##########################
#################################################################################
import sqlite3
from sqlite3 import Error
import csv
#################################################################################

## Change to False to disable Sample
SHOW = True

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
        gt_username = "gburdell3"
        return gt_username
    
    # Part 1.a.i Create Tables [2 points]
    def part_1_a_i(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_1_a_i_sql = ""
        ######################################################################
        
        return self.execute_query(connection, part_1_a_i_sql)

    def part_1_a_ii(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_1_a_ii_sql = ""
        ######################################################################
        
        return self.execute_query(connection, part_1_a_ii_sql)
    
    # Part 1.b Import Data [2 points]
    def part_1_b_movies(self,connection,path):
        ############### CREATE IMPORT CODE BELOW ############################

       ######################################################################
        
        sql = "SELECT COUNT(id) FROM movies;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
    
    def part_1_b_movie_cast(self,connection, path):
        ############### CREATE IMPORT CODE BELOW ############################
        
        ######################################################################
        
        sql = "SELECT COUNT(cast_id) FROM movie_cast;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]

    # Part 1.c Vertical Database Partitioning [5 points]
    def part_1_c(self,connection):
        ############### EDIT CREATE TABLE SQL STATEMENT ###################################
        part_1_c_sql = ""
        ######################################################################
        
        self.execute_query(connection, part_1_c_sql)
        
        ############### CREATE IMPORT CODE BELOW ############################
        part_1_c_insert_sql = ""
        ######################################################################
        
        self.execute_query(connection, part_1_c_insert_sql)
        
        sql = "SELECT COUNT(cast_id) FROM cast_bio;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
       

    # Part 2 Create Indexes [1 points]
    def part_2_a(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_a_sql = ""
        ######################################################################
        return self.execute_query(connection, part_2_a_sql)
    
    def part_2_b(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_b_sql = ""
        ######################################################################
        return self.execute_query(connection, part_2_b_sql)
    
    def part_2_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_2_c_sql = ""
        ######################################################################
        return self.execute_query(connection, part_2_c_sql)
    
    # Part 3 Calculate a Proportion [3 points]
    def part_3(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_3_sql = ""
        ######################################################################
        cursor = connection.execute(part_3_sql)
        return cursor.fetchall()[0][0]

    # Part 4 Find the Most Prolific Actors [4 points]
    def part_4(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_4_sql = ""
        ######################################################################
        cursor = connection.execute(part_4_sql)
        return cursor.fetchall()

    # Part 5 Find the Highest Scoring Movies With the Least Amount of Cast [4 points]
    def part_5(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_5_sql = ""
        ######################################################################
        cursor = connection.execute(part_5_sql)
        return cursor.fetchall()
    
    # Part 6 Get High Scoring Actors [4 points]
    def part_6(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_6_sql = ""
        ######################################################################
        cursor = connection.execute(part_6_sql)
        return cursor.fetchall()

    # Part 7 Creating Views [6 points]
    def part_7(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_7_sql = ""
        ######################################################################
        return self.execute_query(connection, part_7_sql)
    
    def part_8(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_8_sql = ""
        ######################################################################
        cursor = connection.execute(part_8_sql)
        return cursor.fetchall()
    
    # Part 9 FTS [4 points]
    def part_9_a(self,connection,path):
        ############### EDIT SQL STATEMENT ###################################
        part_9_a_sql = ""
        ######################################################################
        connection.execute(part_9_a_sql)
        ############### CREATE IMPORT CODE BELOW ############################
        
        ######################################################################
        sql = "SELECT COUNT(id) FROM movie_overview;"
        cursor = connection.execute(sql)
        return cursor.fetchall()[0][0]
        
    def part_9_b(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_9_b_sql = ""
        ######################################################################
        cursor = connection.execute(part_9_b_sql)
        return cursor.fetchall()[0][0]
    
    def part_9_c(self,connection):
        ############### EDIT SQL STATEMENT ###################################
        part_9_c_sql = ""
        ######################################################################
        cursor = connection.execute(part_9_c_sql)
        return cursor.fetchall()[0][0]


if __name__ == "__main__":
    
    ########################### DO NOT MODIFY THIS SECTION ##########################
    #################################################################################
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
        print('\033[32m' + "part 9.a: " + '\033[m'+ str(db.part_9_a(conn,"data/movie_overview.csv")))
        print('\033[32m' + "Count 9.b: " + '\033[m' + str(db.part_9_b(conn)))
        print('\033[32m' + "Count 9.c: " + '\033[m' + str(db.part_9_c(conn)))
    except Exception as e:
        print("Error in part 9")
        print(e)

    conn.close()
    #################################################################################
    #################################################################################
  
