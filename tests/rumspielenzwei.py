from models.selectstate import SelectState

if __name__=="__main__":
    oeins = SelectState()
    oeins.agg="SUM"
    ozwei = SelectState()
    ozwei.agg = "AVG"
    print("fertig")
