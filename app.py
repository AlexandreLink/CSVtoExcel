import streamlit as st
import pandas as pd
from datetime import datetime

def convert_csv_to_excel(csv_file):
    # Lire le fichier CSV
    df = pd.read_csv(csv_file)

    # Enregistrer en format Excel pour débuter le traitement en Excel
    output_excel = "fichier_converti.xlsx"
    df.to_excel(output_excel, index=False)
    
    # Charger le fichier Excel dans un DataFrame pour continuer les modifications
    df_excel = pd.read_excel(output_excel)
    return df_excel, output_excel

def process_file(df):
    # Suppression de la première ligne
    df = df.iloc[1:]

    # Vérification de la colonne de commande 'Y' et filtrage des dates
    if 'Y' in df.columns:
        df['Y'] = pd.to_datetime(df['Y'], errors='coerce')

        # Définir la date limite (4 du mois à 23:59:59)
        today = datetime.today()
        mois = today.month
        annee = today.year
        date_limite = pd.Timestamp(f"{annee}-{mois:02d}-04 23:59:59")

        # Filtrer les lignes jusqu'au 4 à minuit
        df = df[df['Y'] <= date_limite]
    else:
        st.error("Le fichier Excel ne contient pas de colonne 'Y' pour les dates de commande.")

    # Mettre toutes les valeurs en majuscules
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # Suppression des colonnes inutiles si elles existent
    columns_to_delete = ['BA', 'BU', 'AN', 'AZ', 'AA', 'AL', 'U', 'Z', 'B', 'J', 'C']
    for col_name in columns_to_delete:
        if col_name in df.columns:
            df.drop(columns=[col_name], inplace=True)

    # Ajouter des colonnes et copies
    if 'E' in df.columns:
        df.insert(df.columns.get_loc('E'), 'New Column E', '')
    if 'H' in df.columns:
        df.insert(df.columns.get_loc('H'), 'New Column H', '')
    if 'K' in df.columns and 'I' in df.columns:
        df['I'] = df['K']
    if 'H' in df.columns and 'K' in df.columns:
        df['K'] = df['H']
    if 'B' in df.columns:
        df.insert(12, 'New Column M', '')
        df['M'] = df['B']
        df.drop(['H', 'B'], axis=1, inplace=True)

    # Fusionner les colonnes 'B' et 'C' si elles existent
    if 'B' in df.columns and 'C' in df.columns:
        df['Full Name'] = df['B'] + ' ' + df['C']

    return df

# Interface Streamlit
st.title("Convertisseur CSV vers Excel et Traitement des Données")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Téléversez le fichier CSV", type="csv")

if uploaded_file:
    # Étape 1 : Convertir le fichier CSV en Excel
    df_excel, excel_path = convert_csv_to_excel(uploaded_file)
    
    # Étape 2 : Appliquer les transformations sur le fichier Excel
    df_processed = process_file(df_excel)
    
    if df_processed is not None:
        # Afficher un aperçu du DataFrame
        st.write("Aperçu des données après traitement :")
        st.dataframe(df_processed.head())

        # Sauvegarder le fichier traité
        processed_excel_path = "fichier_processee.xlsx"
        df_processed.to_excel(processed_excel_path, index=False)
        
        # Télécharger le fichier Excel transformé
        with open(processed_excel_path, "rb") as file:
            st.download_button(
                label="Télécharger le fichier Excel",
                data=file,
                file_name="fichier_processee.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
