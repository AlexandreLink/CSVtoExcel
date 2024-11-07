import streamlit as st
import pandas as pd
from datetime import datetime

def process_csv(csv_file):
    # Lire le fichier CSV avec toutes les colonnes
    df = pd.read_csv(csv_file)

    # Liste des colonnes à supprimer
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

    # Supprimer les colonnes inutiles si elles existent dans le CSV
    df = df.drop(columns=[col for col in columns_to_delete if col in df.columns])

    # Liste des colonnes finales que nous voulons conserver après suppression
    columns_to_keep = ['Customer ID', 'Delivery name', 'Delivery address 1', 'Delivery address 2', 
                       'Delivery zip', 'Delivery city', 'Delivery province code', 'Delivery country code', 
                       'Billing country', 'Quantity', 'Created at']
    
    # Filtrer pour conserver seulement les colonnes nécessaires qui sont présentes
    df = df[[col for col in columns_to_keep if col in df.columns]]

    # Étape 2 : Créer la date limite au format du CSV (ex. "2024-11-04T23:59:59+01:00")
    today = datetime.today()
    date_limite_str = f"{today.year}-{today.month:02d}-04T23:59:59+01:00"

    # Étape 3 : Filtrer les lignes avec des dates 'Created at' <= date_limite_str
    if 'Created at' in df.columns:
        df = df[df['Created at'] <= date_limite_str]
    else:
        st.error("Le fichier CSV ne contient pas de colonne 'Created at' pour les dates de commande.")

    # Vérification du nombre et des noms de colonnes avant le renommage
    st.write("Nombre de colonnes après filtrage : ", len(df.columns))
    st.write("Colonnes actuelles : ", df.columns.tolist())

    # Liste des noms de colonnes souhaités
    expected_columns = ['Customer ID', 'Delivery name', 'Delivery address 1', 'Delivery address 2', 
                        'Delivery zip', 'Delivery city', 'Delivery province code', 'Delivery country code', 
                        'Billing country', 'Quantity']
    
    # Renommer uniquement si le nombre de colonnes correspond
    if len(df.columns) == len(expected_columns):
        df.columns = expected_columns
    else:
        st.warning("Le nombre de colonnes dans le CSV ne correspond pas au nombre attendu après filtrage.")

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
