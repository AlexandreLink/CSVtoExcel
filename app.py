import streamlit as st
import pandas as pd
from datetime import datetime

def process_csv(csv_file):
    # Lire le fichier CSV
    df = pd.read_csv(csv_file)

    # Étape 1 : Supprimer les colonnes inutiles directement dans le CSV
    columns_to_keep = ['Customer ID', 'Delivery name', 'Delivery address 1', 'Delivery address 2', 
                       'Delivery zip', 'Delivery city', 'Delivery province code', 'Delivery country code', 
                       'Billing country', 'Quantity', 'Created at']
    df = df[[col for col in columns_to_keep if col in df.columns]]

    # Étape 2 : Créer la date limite au format du CSV (ex. "2024-11-04T23:59:59+01:00")
    today = datetime.today()
    date_limite_str = f"{today.year}-{today.month:02d}-04T23:59:59+01:00"

    # Étape 3 : Filtrer les lignes avec des dates 'Created at' <= date_limite_str
    # On compare les chaînes de caractères, car elles sont déjà dans un format comparable
    if 'Created at' in df.columns:
        df = df[df['Created at'] <= date_limite_str]
    else:
        st.error("Le fichier CSV ne contient pas de colonne 'Created at' pour les dates de commande.")

    # Renommer les colonnes pour le format final
    df.columns = ['Customer ID', 'Delivery name', 'Delivery address 1', 'Delivery address 2', 
                  'Delivery zip', 'Delivery city', 'Delivery province code', 'Delivery country code', 
                  'Billing country', 'Quantity']

    return df

# Interface Streamlit
st.title("Convertisseur CSV vers Excel et Traitement des Données")

# Upload du fichier CSV
uploaded_file = st.file_uploader("Téléversez le fichier CSV", type="csv")

if uploaded_file:
    # Traiter le fichier CSV
    df_processed = process_csv(uploaded_file)
    
    if df_processed is not None:
        # Afficher un aperçu du DataFrame
        st.write("Aperçu des données après traitement :")
        st.dataframe(df_processed.head())

        # Sauvegarder le fichier traité en Excel
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
