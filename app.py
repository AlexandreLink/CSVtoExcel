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
    # Étape 1 : Suppression de la première ligne (titres)
    df = df.iloc[1:]

    # Étape 2 : Filtrer les transactions jusqu'au 4 à minuit
    if 'Created at' in df.columns:
        # Conversion de la colonne 'Created at' en datetime, en utilisant errors='coerce' pour gérer les erreurs
        df['Created at'] = pd.to_datetime(df['Created at'], errors='coerce')

        # Supprimer les lignes avec des valeurs NaT dans 'Created at' après conversion
        df = df.dropna(subset=['Created at'])

        # Définir la date limite (le 4 du mois à 23:59:59)
        today = datetime.today()
        mois = today.month
        annee = today.year
        date_limite = pd.Timestamp(f"{annee}-{mois:02d}-04 23:59:59")

        # Filtrer les lignes dont la date est avant ou égale à la date limite
        df = df[df['Created at'] <= date_limite]
    else:
        st.error("Le fichier Excel ne contient pas de colonne 'Created at' pour les dates de commande.")

    # Étape 3 : Mettre toutes les valeurs en majuscules
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # Étape 4 : Suppression des colonnes inutiles en vérifiant leur existence
    columns_to_delete = ['Customer email', 'Customer phone', 'Imported ID', 'BAB Type', 'BAB reference',
                         'BAB name', 'Delivery Method', 'Delivery type', 'Delivery first name', 'Delivery last name',
                         'Delivery province code', 'Delivery country code', 'Delivery phone', 'Delivery company', 
                         'Shipping Price', 'Delivery price currency', 'Updated at', 'Next order date', 
                         'Billing interval type', 'Billing interval count', 'Billing min cycles', 'Billing max cycles',
                         'Billing address', 'Billing country', 'Billing country code', 'Billing city', 'Billing province code',
                         'Billing zip', 'Delivery interval type', 'Delivery interval count', 'Payment ID', 'Payment method', 
                         'Billing full name', 'Payment method brand', 'Payment method expiry year', 
                         'Payment method expiry month', 'Payment method last digits', 'Line title', 'Line SKU', 
                         'Line variant quantity', 'Line variant price', 'Line price currency', 'Line product ID', 
                         'Line variant ID', 'Line selling plan ID', 'Line selling plan name', 'Line Attributes', 
                         'Subscription Attributes', 'Order notes', 'Cancellation date', 'Cancellation reason', 
                         'Cancellation note', 'Paused on date', 'Total orders till date / Current Billing cycle', 
                         'Past order names', 'Total revenue generated (USD)', 'Total revenue generated (EUR)', 
                         'First order name', 'First order amount', 'Last order name', 'Last order date', 'Last order amount', 
                         'Discount applied', 'Total Processed', 'Delivery Price Override']

    df = df.drop(columns=[col for col in columns_to_delete if col in df.columns])

    # Étape 5 : Insérer une nouvelle ligne de titres
    new_titles = ['Customer ID', 'Delivery name', 'Delivery address 1', 'Delivery address 2', 'Delivery zip', 
                  'Delivery city', 'Delivery province code', 'Delivery country code', 'Billing country', 'Quantity']
    df.columns = new_titles

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
