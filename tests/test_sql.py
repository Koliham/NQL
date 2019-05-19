import unittest

from models.nql import NQL
from nldslfuncs.reader import inltoobj
from moz_sql_parser import parse


class TestSum(unittest.TestCase):
    testresult = {'sel': 3, 'conds': [[5, 0, 'Butler CC (KS)']], 'agg': 0}
    testtable = {"header": ["Player", "No.", "Nationality", "Position", "Years in Toronto", "School/Club Team"],
                 "page_title": "Toronto Raptors all-time roster",
                 "types": ["text", "text", "text", "text", "text", "text"],
                 "id": "1-10015132-11", "section_title": "L", "caption": "L",
                 "name": "table_10015132_11"}

    testresult2 = {"sel": 1, "conds": [[0, 0, "Australian Capital Territory"]], "agg": 0}
    testtable2 = {"id": "1-1000181-1", "header": ["State/territory", "Text/background colour", "Format", "Current slogan", "Current series", "Notes"], "types": ["text", "text", "text", "text", "text", "text"], "name": "table_1000181_1"}

    testresult3 = {"sel": 1, "conds": [[0, 0, ""]], "agg": 0}

    def test_wikisql_toinl(self):
        """
        Test for converting
        """

        sql = NQL.fromwikisql(self.testresult, self.testtable)
        gtinl = "show the Position where 'School/Club Team' is 'Butler CC (KS)'"
        result = sql.inl()
        self.assertEqual(result, gtinl)


    def test_wikisql_tosql(self):

        sqlo = NQL.fromwikisql(self.testresult, self.testtable)
        gtsql = "SELECT Position FROM L WHERE 'School/Club Team' = 'Butler CC (KS)'"
        result = sqlo.sql()
        self.assertEqual(result, gtsql)

        #when value is empty
        sqlo = NQL.fromwikisql(self.testresult3, self.testtable2)
        gtsql = "SELECT 'Text/background colour' FROM table_1000181_1 WHERE State/territory = ''"
        result = sqlo.sql()
        self.assertEqual(result, gtsql)



    def test_wikisql_toinl2(self):

        sqlo = NQL.fromwikisql(self.testresult2, self.testtable2)
        gtinl = "show the 'Text/background colour' where State/territory is 'Australian Capital Territory'"

        result = sqlo.inl()

        self.assertEqual(result, gtinl)


    def test_fromsql(self):
        sql = "SELECT MAX(price) FROM table WHERE source='Berlin' or month<5"
        nql = NQL.fromsql(sql)
        sqlgt = "select MAX(price) from table where source = 'Berlin' or month < 5"
        nlgt = "show the highest price where source is Berlin or month is lower than 5"
        nlpred = nql.inl()
        sqlpred = nql.sql()
        self.assertEqual(sqlgt.lower(), sqlpred.lower())
        self.assertEqual(nlgt.lower(), nlpred.lower())

    def test_question(self):
        sqlo = NQL.fromwikisql(self.testresult2, self.testtable2)
        gtinl_question = "what is the 'Text/background colour' where State/territory is 'Australian Capital Territory'"
        resultq = sqlo.inl(question=True)
        self.assertEqual(resultq, gtinl_question)

        #for count
        input = "count the flights where the state is washington"
        gtoutput = "how many flights are there where state is washington"
        sqlo = NQL.frominl(input)
        resultq = sqlo.inl(question=True)
        self.assertEqual(resultq, gtoutput)



    def test_agg(self):
        # inl to inl and SQL
        inputnl1 = "show the average price where destination is 'new york'"
        inputnl2 = "show the sum of all prices where destination is 'new york'"
        inputnl3 = "show the highest price where destination is 'new york'"
        inputnl4 = "show the lowest price where destination is 'new york'"

        sqlo = NQL.frominl(inputnl1)
        result1 = sqlo.inl()
        self.assertEqual(result1, inputnl1)

        sqlo = NQL.frominl(inputnl2)
        result1 = sqlo.inl()
        self.assertEqual(result1, inputnl2)

        sqlo = NQL.frominl(inputnl3)
        result1 = sqlo.inl()
        self.assertEqual(result1, inputnl3)

        sqlo = NQL.frominl(inputnl4)
        result1 = sqlo.inl()
        self.assertEqual(result1, inputnl4)


    def test_inl_tosql(self):
        inputinl = "show the flights, airbport and destination where source is 'New York', destination is Berlin and the baggage is lower than 500 for which the price is the lowest"
        gtoutputinl = "show the flight, airbport and destination where source is 'New York', destination is Berlin and baggage is lower than 500 for which price is the lowest"
        gtoutputsql = "SELECT flight, airbport, destination FROM table WHERE source = 'New York' AND destination = 'Berlin' AND baggage < 500 ORDER BY price ASC LIMIT 1"
        sqlobj = inltoobj.inltosqlobj(inputinl)
        resultinl = sqlobj.inl()
        resultsql = sqlobj.sql()
        result = gtoutputinl==resultinl and gtoutputsql==resultsql
        self.assertEqual(gtoutputinl, resultinl)
        self.assertEqual(gtoutputsql, resultsql)

        # same with OR
        inputinl = "show the flights, airbport and destination where source is 'New York', destination is Berlin or the baggage is lower than 500 for which the price is the highest"
        gtoutputinl = "show the flight, airbport and destination where source is 'New York', destination is Berlin or baggage is lower than 500 for which price is the highest"
        gtoutputsql = "SELECT flight, airbport, destination FROM table WHERE source = 'New York' OR destination = 'Berlin' OR baggage < 500 ORDER BY price DESC LIMIT 1"
        sqlobj = inltoobj.inltosqlobj(inputinl)
        resultinl = sqlobj.inl()
        resultsql = sqlobj.sql()
        result = gtoutputinl == resultinl and gtoutputsql == resultsql
        self.assertEqual(gtoutputinl, resultinl)
        self.assertEqual(gtoutputsql, resultsql)

    def test_wikisql_dictexport(self):
        sqlo = NQL.fromwikisql(self.testresult, self.testtable)
        refresult = sqlo.wikisqldict()
        self.assertEqual(self.testresult, refresult)


if __name__ == '__main__':
    unittest.main()