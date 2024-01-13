# Importing libraries
import pandas as pd
import pokebase as pb
import streamlit as st
from io import BytesIO

# Creating required dataframes


def get_files(gen=5, all=True):

    Kanto=("https://docs.google.com/spreadsheets/d/e/2PACX-1vTS2czIYW9-5pKZIPFtgYWfmuFZsgT20Eqsa50M4v5V2yye_h-MlWd8wZjKdWppWQ/pub?output=xlsx","https://docs.google.com/spreadsheets/d/e/2PACX-1vTS2czIYW9-5pKZIPFtgYWfmuFZsgT20Eqsa50M4v5V2yye_h-MlWd8wZjKdWppWQ/pub?output=xlsx")
    Jhoto=("https://docs.google.com/spreadsheets/d/e/2PACX-1vRnVcu2iZhNSzzWXcy_jBWE22w0G7u_8PLpDB6W9B11ky_fXA0IFf-lBlYSxAfurg/pub?output=xlsx","https://docs.google.com/spreadsheets/d/e/2PACX-1vTcWXwHGarD4igW48ANb6h4kKGYCrHXn-K0uh-lDUwoUkDfZ10U-KuWPf4kAS_0ZA/pub?output=xlsx")
    Hoenn=("https://docs.google.com/spreadsheets/d/e/2PACX-1vRnVcu2iZhNSzzWXcy_jBWE22w0G7u_8PLpDB6W9B11ky_fXA0IFf-lBlYSxAfurg/pub?output=xlsx","https://docs.google.com/spreadsheets/d/e/2PACX-1vQr9kAhdAb03qQUWPiieOxd9I-yXot67DmJzEoHr82d6YQvxuWxCJI5kaezg1XTxg/pub?output=xlsx")
    Sinnoh=("https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3SXsMI1vrJqq5xiOjogw1kO2SboZOf9_UZOf0rIDnhNGqgeXZ1k2UEJnTNNMVMw/pub?output=xlsx","https://docs.google.com/spreadsheets/d/e/2PACX-1vT5VazsQZVa99b4LC9JZPaR7bcV7gDbCq22cnZC4cI60C0MTJMMvfDWXFdhxFgDlw/pub?output=xlsx")
    Unova=("https://docs.google.com/spreadsheets/d/e/2PACX-1vTtBWsiSMVuX4IQibaTNaAjuIC9iciRNCC8T9SW0lazaXoEcIXE8QGTd6ekrpjnMw/pub?output=xlsx","https://docs.google.com/spreadsheets/d/e/2PACX-1vTUQcfs1fjoxZulCCBmrldwLeosm85e_rdgc8DU5YdtkUjeNQuLuxb5QLBQZ86-_A/pub?output=xlsx")

    generations = {
        "Kanto": Kanto,
        "Jhoto": Jhoto,
        "Hoenn": Hoenn,
        "Sinnoh": Sinnoh,
        "Unova": Unova,
    }

    if not all:
        list_of_gen = st.multiselect(
            "Select generations for your database: ",
            ["Kanto", "Jhoto", "Hoenn", "Sinnoh", "Unova"],
        )

        mon_db=pd.DataFrame()
        move_db=pd.DataFrame()
        for i in list_of_gen:
            data=pd.read_excel(generations[i][0])
            mon_db=pd.concat([mon_db,data])
            data=pd.read_excel(generations[i][0], sheet_name="Moves")
            move_db=pd.concat([move_db,data])

    else:
        Gen=list(generations.keys())[gen-1]
        mon_db=pd.read_excel(generations[Gen][1])
        move_db=pd.read_excel(generations[Gen][1], sheet_name="Moves")
    
    excel_buffer= BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        mon_db.to_excel(writer, sheet_name="Pokemon", index=False)
        move_db.to_excel(writer, sheet_name="Moves", index=False)

    return excel_buffer

# Saving the dfs to a file
def save_df(df, sheet, file):
    excel_buffer = BytesIO()
    if sheet == "Pokemon":
        sheet2 = "Moves"
    else:
        sheet2 = "Pokemon"
    df2 = pd.read_excel(file, sheet_name=sheet2)
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name=sheet, index=False)
        df2.to_excel(writer, sheet_name=sheet2, index=False)

    excel_buffer.seek(0)
    return excel_buffer


# To get index of any pokemon or move
def get_index(df, col="DexNo or Name"):
    # Getting user input
    ind = st.text_input(f"Enter {col}: ", key="get_index")

    # Checking if ind is None
    if ind:
        if ind[0].isdigit():
            if col == "Name":
                return "Given input is not appropriate for chosen column"

            else:
                return int(ind)

        # Extracting the index from the Name
        else:
            name = "-".join(ind.title().split())
            ind = list(df.loc[df["Name"] == name].index)
            print(ind, name)
            if ind:
                return ind[0] + 1
            else:
                return "Given Name not in Database"
    return "Empty Field"


def update(sheet, file):
    # reading the required df
    df = pd.read_excel(file, sheet_name=sheet)

    ind = get_index(df)

    if isinstance(ind, int):
        if sheet=="Pokemon":
            sprite_url=pb.pokemon(id).sprites.front_url
            st.image(sprite_url)
        row=df.set_index("DexNo")
        st.dataframe(row.loc[ind])
    else:
        return ind

    check=True
    with st.form(key="Update Form", clear_on_submit=True):
        col_list = st.multiselect(
            "Column name where change should occur: ", list(df.columns)
        )

        action = st.radio("Select Action: ", ["Overwrite", "Append"], index=0)

        if st.form_submit_button("Next"):
            check=False

    with st.form(key="Info", clear_on_submit=True):
        for col in col_list:
            new = st.text_input(f"Enter data for {col}: ")
            if action == "Append":
                existing = df[col][ind - 1]
                existing += " " + new
                df.loc[ind - 1, col] = existing

            elif action == "Overwrite":
                df.loc[ind - 1, col] = new

        if st.form_submit_button("Update",disabled=check):
            check=True

            return df

    return "Waiting for data"
