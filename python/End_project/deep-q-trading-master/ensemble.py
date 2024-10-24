import os
import pandas as pd
import numpy as np

def full_ensemble(df):
    m1 = df.eq(1).all(axis=1)
    m2 = df.eq(2).all(axis=1)
    local_df = df.copy()
    local_df['ensemble'] = np.select([m1, m2], [1, 2], 0)
    local_df = local_df.drop(local_df.columns.difference(['ensemble']), axis=1)
    return local_df

def perc_ensemble(df, thr = 0.7):
    c1 = (df.eq(1).sum(1) / df.shape[1]).gt(thr)
    c2 = (df.eq(2).sum(1) / df.shape[1]).gt(thr)
    return pd.DataFrame(np.select([c1, c2], [1, 2], 0), index=df.index, columns=['ensemble'])

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def ensemble(numWalks, perc, type, numDel):
    dollSum = 0
    rewSum = 0
    posSum = 0
    negSum = 0
    covSum = 0
    numSum = 0

    values = []

    # Directory for output
    output_dir = "./Output/ensemble"
    create_dir_if_not_exists(output_dir)

    output_file = os.path.join(output_dir, "daxValidDel9th60.csv")
    with open(output_file, "w+") as output:
        output.write("Iteration,Reward%,#Wins,#Losses,Euro,Coverage,Accuracy\n")
        columns = ["Iteration", "Reward%", "#Wins", "#Losses", "Dollars", "Coverage", "Accuracy"]
        
        dax = pd.read_csv("./datasets/sp500Day.csv", index_col='Date')
        for j in range(0, numWalks):
            df = pd.read_csv(f"./Output/ensemble/walk{j}ensemble_{type}.csv", index_col='Date')
            
            for deleted in range(1, numDel):
                del df[f'iteration{deleted}']
            
            if perc == 0:
                df = full_ensemble(df)
            else:
                df = perc_ensemble(df, perc)

            num = 0
            rew = 0
            pos = 0
            neg = 0
            doll = 0
            cov = 0

            for date, i in df.iterrows():
                num += 1
                if date in dax.index:
                    if (i['ensemble'] == 1):
                        pos += 1 if (dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 0
                        neg += 0 if (dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 1
                        rew += (dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open']
                        doll += (dax.at[date, 'Close'] - dax.at[date, 'Open']) * 50
                        cov += 1
                    elif (i['ensemble'] == 2):
                        neg += 0 if -(dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 1
                        pos += 1 if -(dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 0
                        rew += -(dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open']
                        doll += -(dax.at[date, 'Close'] - dax.at[date, 'Open']) * 50
                        cov += 1

            values.append([str(round(j, 2)), str(round(rew, 2)), str(round(pos, 2)), str(round(neg, 2)), str(round(doll, 2)), str(round(cov/num, 2)), (str(round(pos/cov, 2)) if (cov > 0) else "")])

            dollSum += doll
            rewSum += rew
            posSum += pos
            negSum += neg
            covSum += cov
            numSum += num

        values.append(["sum", str(round(rewSum, 2)), str(round(posSum, 2)), str(round(negSum, 2)), str(round(dollSum, 2)), str(round(covSum/numSum, 2)), (str(round(posSum/covSum, 2)) if (covSum > 0) else "")])
    
    return values, columns

def evaluate(csvname=""):
    output_dir = "./Output/results"
    create_dir_if_not_exists(output_dir)

    output_file = os.path.join(output_dir, "resultsSPFinal.csv")
    with open(output_file, "w+") as output:
        output.write("Iteration,Reward%,#Wins,#Losses,Euro,Coverage,Accuracy\n")
        
        df = pd.read_csv(csvname)
        dax = pd.read_csv("./datasets/sp500Day.csv", index_col='Date')
        df['date'] = pd.to_datetime(df['date'])
        df['date'] = df['date'].dt.strftime('%m/%d/%Y')
        df.set_index('date', inplace=True)
        
        num = 0
        rew = 0
        pos = 0
        neg = 0
        doll = 0
        cov = 0

        for date, i in df.iterrows():
            num += 1
            if date in dax.index:
                if (i['ensemble'] == 1):
                    pos += 1 if (dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 0
                    neg += 0 if (dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 1
                    rew += (dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open']
                    doll += (dax.at[date, 'Close'] - dax.at[date, 'Open']) * 50
                    cov += 1
                elif (i['ensemble'] == -1):
                    neg += 0 if -(dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 1
                    pos += 1 if -(dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open'] > 0 else 0
                    rew += -(dax.at[date, 'Close'] - dax.at[date, 'Open']) / dax.at[date, 'Open']
                    doll += -(dax.at[date, 'Close'] - dax.at[date, 'Open']) * 50
                    cov += 1

        output.write(f"0,{round(rew, 2)},{round(pos, 2)},{round(neg, 2)},{round(doll, 2)},{round(cov/num, 2)},{(str(round(pos/cov, 2)) if (cov > 0) else '')}\n")

# evaluate("./Output/results/finalEnsembleSP500.csv")
