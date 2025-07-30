
from database.DB_connect import DBConnect

from model.circuit import Circuit


class DAO():
    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT distinct s.`year` as y
                        FROM seasons s
                        ORDER BY s.`year`
                        """
            cursor.execute(query)

            for row in cursor:
                result.append(row['y'])

            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllNodes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT c.*, r.round as r
                        FROM circuits c, races r 
                        WHERE c.circuitId = r.circuitId
                            AND r.`year` = %s
                        ORDER BY c.name
                            """
            cursor.execute(query, (year,))

            for row in cursor:
                result.append((Circuit(**row)))

            cursor.close()
            cnx.close()

        return result


    @staticmethod
    def getAllEdges(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT t1.c as c1, t2.c as c2
                        FROM (SELECT c.circuitId as c, r.round as r
                                FROM circuits c, races r 
                                WHERE c.circuitId = r.circuitId
                                    AND r.`year` = %s) t1, 
                                (SELECT c.circuitId as c, r.round as r
                                    FROM circuits c, races r 
                                    WHERE c.circuitId = r.circuitId
                                        AND r.`year` = %s) t2
                        WHERE t1.c <> t2.c
                        and t1.r = t2.r-1
                                    """
            cursor.execute(query, (year, year))

            for row in cursor:
                result.append((row['c1'], row['c2']))

            cursor.close()
            cnx.close()

        return result


