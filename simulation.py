import pandas as pd
import numpy as np
from IPython.core import display as ICD
import matplotlib.pyplot as plt

deathprobs = pd.read_csv('deathprobs.csv').set_index('Age').T

def getCourtMakeup(rbgCounterfactual):
    makeup = [
        {
            "name": "Clarence Thomas",
            "age": 74,
            "yearsOnCourt": 30,
            "party": "R",

        },
        {
            "name": "Ketanji Brown Jackson",
            "age": 51,
            "yearsOnCourt": 0,
            "party": "D",

        },
        {
            "name": "John Roberts",
            "age": 67,
            "yearsOnCourt": 16,
            "party": "R",

        },
        {
            "name": "Samuel Alito",
            "age": 72,
            "yearsOnCourt": 16,
            "party": "R",

        },
        {
            "name": "Sonia Sotomayor",
            "age": 68,
            "yearsOnCourt": 12,
            "party": "D",

        },
        {
            "name": "Elena Kagan",
            "age": 62,
            "yearsOnCourt": 11,
            "party": "D",

        },
        {
            "name": "Neil Gorsuch",
            "age": 54,
            "yearsOnCourt": 5,
            "party": "R",

        },
        {
            "name": "Brett Kavanaugh",
            "age": 57,
            "yearsOnCourt": 3,
            "party": "R",

        },
        {
            "name": "Dem",
            "age": 59,
            "yearsOnCourt": 9,
            "party": "D",

        },
    ]

    if rbgCounterfactual:
        makeup.append({
            "name": "Amy Coney Barrett",
            "age": 50,
            "yearsOnCourt": 1,
            "party": "R",

        })
    else:
        makeup.append({
            "name": "Dem",
            "age": 59,
            "yearsOnCourt": 9,
            "party": "D",

        })
    return makeup

def getEndServiceProb(age, yearsOnCourt, justiceParty, presParty):
    if ((yearsOnCourt >= 18 or age >= 78) and (justiceParty==presParty)):
        return 1
    else:
        if age < 50:
            raise Exception("Age below range")
        if age >= 110:
            return 1
        else:
            return float(deathprobs[age])
    
def incrementCourtValues(courtMakeup):
    for justice in courtMakeup:
        justice["age"] += 1
        justice["yearsOnCourt"] += 1
        
def updateCourtMakeup(courtMakeup, presParty):
    for justice in courtMakeup:
        endServiceProb = getEndServiceProb(justice["age"], justice["yearsOnCourt"], justice["party"], presParty)
        endService = np.random.choice([True, False], p=[endServiceProb, 1-endServiceProb])
        
        if (endService):
            
            justice["name"] = "Dem" if presParty == "D" else "Repub"
            justice["age"] = 50
            justice["yearsOnCourt"] = 0
            justice["party"] = presParty
            
def getRepubsOnCourt(courtMakeup):
    return sum(justice.get("party") == 'R' for justice in courtMakeup)

def runAnalysis(rbgCounterfactual)
    data = {}
    republicanWinProbs = np.arange(0.3, 0.51, 0.05)
    for republicanWinProb in republicanWinProbs:
        monteCarloOutput = pd.DataFrame(0, index=np.arange(1, 51), columns=np.arange(0, 10))

        numTrials = 10000

        for trial in range(10000):
            if (trial % 100 == 0):
                print(trial)
            year = 2022
            presParty = "D"
            courtMakeup = getCourtMakeup(rbgCounterfactual)

            for yearsOut in range(1, 51):
                year += 1
                if (year % 4 == 0):
                    presParty = np.random.choice(["D", "R"], p=[1-republicanWinProb, republicanWinProb])
                incrementCourtValues(courtMakeup)
                updateCourtMakeup(courtMakeup, presParty)

                monteCarloOutput[getRepubsOnCourt(courtMakeup)][yearsOut] += 1

        data[republicanWinProb * 100] = monteCarloOutput/numTrials

    republicanMajorityColumns = []
    keys = []
    for x in range(50,29, -5):
        data[x] = pd.read_excel('{}.xlsx'.format(x), index_col=0)
        data[x]["Republican Majority"] = data[x][5] + data[x][6] + data[x][7] + data[x][8] + data[x][9]
        republicanMajorityColumns.append(data[x]["Republican Majority"])
        keys.append("{}% probability of Republican winning each presidential election".format(x))

    aggData = pd.concat(republicanMajorityColumns, axis=1, keys=keys)
    ICD.display(aggData.plot(title="Probability of Republican-appointed majority",kind='line', ylim=[0,1], grid=True, yticks=np.arange(0, 1.1, step=0.1)).set_xlabel("Years from Present"))

# Run main analysis.
runAnalysis(False)

# Run analysis assuming RBG had retired in 2013 and was replaced in that year by a 50-year-old Justice appointed by President Obama.
runAnalysis(True)

















