import streamlit as st
import pandas as pd
from datetime import datetime

def process_file(df):
    # Étape 1 : Suppression de la première ligne
    df = df.iloc[1:]

    # Étape 2 : Convertir la colonne Y en datetime pour faciliter le filtrage
    if 'Y' in df.columns:
        df['Y'] = pd.to_datetime(df['Y'], errors='coerce')

        # Déterminer le mois et l'année actuels
        today = datetime.today()
        mois = today.month
        annee = today.year

        # Définir la date limite (le 4 de ce mois à 23:59:59)
        date_limite = pd.Timestamp(f"{annee}-{mois:02d}-04 23:59:59")

        # Filtrer les lignes pour garder uniquement celles avant ou égales au 4 à minuit
        df = df[df['Y'] <= date_limite]
    else:
        st.error("Le fichier CSV ne contient pas de colonne 'Y' pour les dates de commande.")

    # Étape 3 : Mettre toutes les valeurs en majuscule
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # Étape 4 : Suppression des colonnes inutiles
    columns_to_delete = ['BA:BU', 'AN:AZ', 'AA:AL', 'U:Z', 'B:J', 'C:C']
    for col_range in columns_to_delete:
        start_col, end_col = col_range.split(':')
        start_idx = df.columns.get_loc(start_col)
        end_idx = df.columns.get_loc(end_col)
        df.drop(df.columns[start_idx:end_idx + 1], axis=1, inplace=True)

    # Étape 5 : Ajouter des colonnes vides et effectuer les copies
    df.insert(4, 'New Column E', '')  # Insérer une colonne vide en position E
    df.insert(7, 'New Column H', '')  # Insérer une colonne vide en position H
    df['I'] = df['K']  # Copier la colonne K vers I
    df['K'] = df['H']  # Copier la colonne H vers K
    df.insert(12, 'New Column M', '')  # Insérer une colonne vide en position M
    df['M'] = df['B']  # Copier la colonne B vers M
    df.drop(['H', 'B'], axis=1, inplace=True)  # Supprimer les colonnes H et B

    # Étape 6 : Fusionner les colonnes 'B' et 'C' dans une nouvelle colonne 'Full Name'
    if 'B' in df.columns and 'C' in df.columns:
        df['Full Name'] = df['B'] + ' ' + df['C']

    return df

# Interface Streamlit
st.title("Convertisseur CSV vers Excel et Traitement des Données")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Téléversez le fichier CSV", type="csv")

if uploaded_file:
    # Lire le fichier CSV
    df = pd.read_csv(uploaded_file)
    
    # Traiter le fichier
    df_processed = process_file(df)
    
    if df_processed is not None:
        # Afficher les premières lignes pour confirmation
        st.write("Aperçu des données après traitement :")
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
