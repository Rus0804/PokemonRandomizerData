import streamlit as st
from creation import get_files, update, save_df
from poke_type import type_chart, type_check
from searching import lookup, check_progress


def download_data(excel_buffer):
    return st.download_button(
        label="Download File",
        data=excel_buffer,
        file_name="PokemonDatabase.xlsx",
        key="download_button",
    )


def main():
    st.title("Pokemon Randomizer App")

    # Sidebar
    st.sidebar.header("Menu")
    menu = st.sidebar.selectbox(
        "Choose an option",
        [
            "New Dataset",
            "Update Dataset",
            "Lookup",
            "Check Progress",
            "Type Chart",
            "Type Effectiveness",
        ]
    )

    if menu=="New Dataset":
        ch=st.radio("Choose Option: ", ["All Upto", "Select Specific"])
        if ch=="All Upto":
            gen=st.slider("Select Generation", 1, 5, 5, 1)
            excel_buffer=get_files(gen)
        else:
            excel_buffer=get_files(all=False)
        download_data(excel_buffer)

    elif menu == "Update Dataset":
        st.sidebar.subheader("Update Dataset")
        file = st.sidebar.file_uploader("Upload Your xlsx File: ", type=["xlsx"])
        sheet_to_update = st.sidebar.selectbox(
            "Select Sheet to Update", ["Pokemon", "Moves"]
        )

        if "latest" in st.session_state:
            file=st.session_state.latest

        if sheet_to_update and file:
            updated_df = update(sheet_to_update, file)
            if isinstance(updated_df, str):
                st.warning(updated_df)
            else:
                excel_buffer = save_df(df=updated_df, sheet=sheet_to_update, file=file)
                st.success("Dataset updated successfully!")
                if "latest" not in st.session_state:
                    st.session_state["latest"]=excel_buffer
                else:
                    st.session_state["latest"]=excel_buffer
                download_data(excel_buffer=excel_buffer)

    elif menu == "Lookup":
        st.sidebar.subheader("Lookup")
        if "latest" in st.session_state:
            file=st.session_state.latest
        else:
            file = st.sidebar.file_uploader("Upload Your xlsx File: ", type=["xlsx"])
        
        if file:
            result = lookup(file)
            if isinstance(result, str):
                st.warning(result)
            else:
                st.dataframe(result, use_container_width=True)

    elif menu == "Check Progress":
        st.sidebar.subheader("Check Progress")
        file = st.sidebar.file_uploader("Upload Your xlsx File: ", type=["xlsx"])
        if file:
            df1, df2 = check_progress(file)
            ch = st.sidebar.selectbox("Choose an option:", ["Pokemon", "Moves"])
            if ch == "Pokemon":
                st.dataframe(df1, use_container_width=True)
            elif ch == "Moves":
                st.dataframe(df2, use_container_width=True)

    elif menu == "Type Chart":
        st.sidebar.subheader("Type Chart")
        type_chart_df = type_chart()
        st.dataframe(type_chart_df)

    elif menu == "Type Effectiveness":
        st.sidebar.subheader("Type Effectiveness")
        selected_option = st.radio(
            "To find type of: ", ["Pokemon", "Move"], index=0, horizontal=True
        )

        # Display output based on the selected option
        if selected_option == "Pokemon":
            possible_types = type_check()
        elif selected_option == "Move":
            possible_types = type_check(rev=True)

        st.table(possible_types)

    st.sidebar.markdown("---")


if __name__ == "__main__":
    main()
