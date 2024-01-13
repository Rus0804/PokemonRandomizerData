import streamlit as st
import pandas as pd
from creation import get_index
import pokebase as pb


def lookup(excel):
    mon_db = pd.read_excel(excel, sheet_name="Pokemon")
    move_db = pd.read_excel(excel, sheet_name="Moves")

    Ch = st.sidebar.selectbox("Choose option: ", ["Pokemon", "Moves"])

    if Ch == "Pokemon":
        mon_db.set_index("DexNo",inplace=True)
        col = st.sidebar.selectbox(
            "Choose Filter: ", ["DexNo", "Name", "Type", "Abilities"]
        )
        if col in ["DexNo", "Name"]:
            ind = get_index(mon_db, col)
            
            if isinstance(ind, int):
                sprite_url=pb.pokemon(ind).sprites.front_default
                st.image(sprite_url)
                result = mon_db.loc[ind]
            else:
                return ind

        elif col == "Type":
            filter = st.selectbox(
                "Choose Type: ",
                [
                    "Normal",
                    "Fire",
                    "Water",
                    "Electric",
                    "Grass",
                    "Ice",
                    "Fighting",
                    "Poison",
                    "Ground",
                    "Flying",
                    "Psychic",
                    "Bug",
                    "Rock",
                    "Ghost",
                    "Dragon",
                    "Dark",
                    "Steel",
                ],
            )
            result = mon_db.loc[mon_db[col].str.contains(filter)]

        else:
            filter = st.text_input("Enter Ability: ")
            result = mon_db.loc[mon_db[col].str.contains(filter)]
    else:
        move_db.set_index("DexNo",inplace=True)
        col = st.sidebar.selectbox(
            "Choose Filter: ", ["DexNo", "Name", "Type", "Damage_Type"]
        )
        
        if col in ["DexNo", "Name"]:
            ind = get_index(move_db)
            if isinstance(ind, int):
                result = move_db.loc[ind - 1]
            else:
                return ind

        elif col == "Type":
            filter = st.sidebar.selectbox(
                "Choose Type: ",
                [
                    "Normal",
                    "Fire",
                    "Water",
                    "Electric",
                    "Grass",
                    "Ice",
                    "Fighting",
                    "Poison",
                    "Ground",
                    "Flying",
                    "Psychic",
                    "Bug",
                    "Rock",
                    "Ghost",
                    "Dragon",
                    "Dark",
                    "Steel",
                ],
            )
            result = move_db.loc[move_db[col] == filter]

        elif col == "Damage_Type":
            filter = st.sidebar.selectbox(
                "Choose Damage Class: ", ["Physical", "Special", "Status"]
            )
            result = move_db.loc[move_db[col] == filter]

    if result.empty:
        return "Records not found"
    else:
        return result


def check_progress(excel):
    mon_db = pd.read_excel(excel, sheet_name="Pokemon")
    move_db = pd.read_excel(excel, sheet_name="Moves")

    return mon_db.loc[(mon_db["Type"] != "0") | (mon_db["Abilities"] != "0")].set_index(
        "DexNo"
    ), move_db.loc[move_db["Type"] != "0"][move_db.columns[:5]].set_index("DexNo")
