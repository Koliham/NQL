from models.nql import NQL

testresult = {'sel': 3, 'conds': [[5, 0, 'Butler CC (KS)']], 'agg': 0}
testresult2 = {'sel': 2, 'conds': [[4, 1, 'Butler AA (KS)']], 'agg': 0}

testtable = {"header": ["Player", "No.", "Nationality", "Position", "Years in Toronto", "School/Club Team"],
             "page_title": "Toronto Raptors all-time roster", "types": ["text", "text", "text", "text", "text", "text"],
             "id": "1-10015132-11", "section_title": "L", "caption": "L",
             "rows": [["Antonio Lang", "21", "United States", "Guard-Forward", "1999-2000", "Duke"],
                      ["Voshon Lenard", "2", "United States", "Guard", "2002-03", "Minnesota"],
                      ["Martin Lewis", "32, 44", "United States", "Guard-Forward", "1996-97", "Butler CC (KS)"],
                      ["Brad Lohaus", "33", "United States", "Forward-Center", "1996", "Iowa"],
                      ["Art Long", "42", "United States", "Forward-Center", "2002-03", "Cincinnati"],
                      ["John Long", "25", "United States", "Guard", "1996-97", "Detroit"],
                      ["Kyle Lowry", "3", "United States", "Guard", "2012-Present", "Villanova"]],
             "name": "table_10015132_11"}

testtable2 = {"header": ["Player", "No.", "Music", "Position", "Years in Toronto", "School/Club Team"],
             "page_title": "Toronto Raptors all-time roster", "types": ["text", "text", "text", "text", "text", "text"],
             "id": "1-10015132-11", "section_title": "L", "caption": "L",
             "rows": [["Antonio Lang", "21", "United States", "Guard-Forward", "1999-2000", "Duke"],
                      ["Voshon Lenard", "2", "United States", "Guard", "2002-03", "Minnesota"],
                      ["Martin Lewis", "32, 44", "United States", "Guard-Forward", "1996-97", "Butler CC (KS)"],
                      ["Brad Lohaus", "33", "United States", "Forward-Center", "1996", "Iowa"],
                      ["Art Long", "42", "United States", "Forward-Center", "2002-03", "Cincinnati"],
                      ["John Long", "25", "United States", "Guard", "1996-97", "Detroit"],
                      ["Kyle Lowry", "3", "United States", "Guard", "2012-Present", "Villanova"]],
             "name": "table_10015132_11"}

obj1 = NQL.fromwikisql(testresult, testtable)

# obj1.selstate.agg = "SUM"
# obj2 = SQLState.fromwikisql(testresult2, testtable2)


print(obj1.inl())
print(obj1.sql())
print("---")
sqlo = NQL.fromwikisql(testresult, testtable)
gtsql = r"SELECT Position FROM table_10015132_11 WHERE 'School/Club Team' = 'Butler CC (KS)'"
result = sqlo.sql()
print(result)
print(sqlo.sql())
print(result==gtsql)
