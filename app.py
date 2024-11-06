import streamlit as st
import pandas as pd

def process_file(df):
    # Conversion de la colonne des dates en format datetime
    df['transaction_date'] = pd.to_datetime(df['transaction_date'], errors='coerce')
    
    # Déterminer dynamiquement le mois et l'année à partir des données
    if df['transaction_date'].notna().any():  # Vérifier si la colonne de date contient des valeurs valides
        # Extraire le mois et l'année de la première transaction
        first_date = df['transaction_date'].dropna().iloc[0]
        mois = first_date.month
        annee = first_date.year

        # Définir la date limite pour le 4 de ce mois à 23:59:59
        date_limite = pd.Timestamp(f"{annee}-{mois:02d}-04 23:59:59")

        # Filtrer les lignes pour garder uniquement celles qui ont une date avant ou égale au 4 à minuit
        df = df[df['transaction_date'] <= date_limite]
    else:
        st.warning("Erreur : aucune date valide trouvée dans la colonne 'transaction_date'.")

    # Suppression des colonnes inutiles et transformations
    # (Ajoutez ici les étapes de suppression de colonnes et de transformation)

    return df

# Interface Streamlit
st.title("Traitement des transactions jusqu'au 4 du mois")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Téléversez le fichier CSV", type="csv")

if uploaded_file:
    # Lire le fichier et traiter les données
    df = pd.read_csv(uploaded_file, skiprows=1)
    df_processed = process_file(df)
    
    # Afficher les premières lignes pour confirmation
    st.write("Transactions filtrées jusqu'au 4 à minuit :")
    st.dataframe(df_processed.head())

    # Exporter le fichier traité en Excel
    output_excel = "fichier_processee.xlsx"
    df_processed.to_excel(output_excel, index=False)
    
    # Télécharger le fichier Excel
    with open(output_excel, "rb") as file:
        st.download_button(
            label="Télécharger le fichier Excel",
            data=file,
            file_name="fichier_processee.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
