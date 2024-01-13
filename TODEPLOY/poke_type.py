import pandas as pd
import numpy as np
import streamlit as st


def type_chart():
    t_chart1 = {}
    t=["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel"]
    t_chart1["Normal"]  =np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0])
    t_chart1["Fire"]    =np.array([1.0, 0.5, 2.0, 1.0, 0.5, 0.5, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 0.5])
    t_chart1["Water"]   =np.array([1.0, 0.5, 0.5, 2.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5])
    t_chart1["Electric"]=np.array([1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5])
    t_chart1["Grass"]   =np.array([1.0, 2.0, 0.5, 0.5, 0.5, 2.0, 1.0, 2.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0])
    t_chart1["Ice"]     =np.array([1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0])
    t_chart1["Fighting"]=np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0])
    t_chart1["Poison"]  =np.array([1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 0.5, 0.5, 2.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0])
    t_chart1["Ground"]  =np.array([1.0, 1.0, 2.0, 0.0, 2.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0])
    t_chart1["Flying"]  =np.array([1.0, 1.0, 1.0, 2.0, 0.5, 2.0, 0.5, 1.0, 0.0, 1.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0])
    t_chart1["Psychic"] =np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 2.0, 1.0])
    t_chart1["Bug"]     =np.array([1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 0.5, 1.0, 0.5, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0])
    t_chart1["Rock"]    =np.array([0.5, 0.5, 2.0, 1.0, 2.0, 1.0, 2.0, 0.5, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0])
    t_chart1["Ghost"]   =np.array([0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.5, 1.0, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 2.0, 1.0])
    t_chart1["Dragon"]  =np.array([1.0, 0.5, 0.5, 0.5, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0])
    t_chart1["Dark"]    =np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.0, 2.0, 1.0, 0.5, 1.0, 0.5, 1.0])
    t_chart1["Steel"]   =np.array([0.5, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0, 0.0, 2.0, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 1.0, 0.5])

    type_chart = {}
    for i in range(len(t)):
        for j in range(len(t)):
            if i == j:
                type_chart[t[i]] = t_chart1[t[i]]
            else:
                if t[j] + " " + t[i] in list(type_chart.keys()):
                    continue
                type_chart[t[i] + " " + t[j]] = np.multiply(
                    t_chart1[t[i]], t_chart1[t[j]]
                )

    data = [[t] + list(type_chart[t]) for t in type_chart.keys()]

    col = ["Types"] + t
    df = pd.DataFrame(columns=col)
    for i in data:
        df.loc[len(df.index)] = i

    df = df.set_index("Types")
    return df


def type_check(rev=False):
    T_Chart = type_chart()

    possibilities = []
    if rev:
        T_Chart = T_Chart.transpose()

    type_col = list(T_Chart.columns)

    SE = st.sidebar.multiselect("Super Effective: ", type_col)
    N = st.sidebar.multiselect("Neutral: ", type_col)
    NE = st.sidebar.multiselect("Not Very Effective: ", type_col)
    I = st.sidebar.multiselect("Immune: ", type_col)

    types = SE + N + NE + I

    for i in range(len(types)):
        if types[i] in SE:
            possibilities.append(list(T_Chart.loc[T_Chart[types[i]] > 1].index))

        elif types[i] in N:
            possibilities.append(list(T_Chart.loc[T_Chart[types[i]] == 1].index))

        elif types[i] in NE:
            possibilities.append(
                list(
                    T_Chart.loc[(T_Chart[types[i]] < 1) & (T_Chart[types[i]] > 0)].index
                )
            )

        else:
            possibilities.append(list(T_Chart.loc[T_Chart[types[i]] == 0].index))

    Types_actual = []
    if possibilities:
        for i in possibilities[0]:
            Types_actual.append(i)
            for j in possibilities[1:]:
                if i not in j:
                    Types_actual.pop()
                    break

    return pd.DataFrame(Types_actual, columns=["Type"])
