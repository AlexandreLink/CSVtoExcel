import streamlit as st
import pandas as pd
from datetime import datetime

def process_csv(csv_file):
    # 1. Lire le fichier CSV avec toutes les colonnes
    df = pd.read_csv(csv_file)

    # 2. Mettre toutes les valeurs en majuscules
    df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

    # 3. Créer la date limite au format du CSV (ex. "2024-11-04T23:59:59+01:00")
    today = datetime.today()
    date_limite_str = f"{today.year}-{today.month:02d}-04T23:59:59+01:00"

    # 4. Filtrer les lignes avec des dates 'Created at' <= date_limite_str
    if 'Created at' in df.columns:
        df = df[df['Created at'] <= date_limite_str]
    else:
        st.error("Le fichier CSV ne contient pas de colonne 'Created at' pour les dates de commande.")

    # 5. Supprimer la colonne 'Created at' après le filtrage
    df = df.drop(columns=['Created at'], errors='ignore')

    # 6. Correspondance des colonnes pour le fichier final
    column_mapping = {
        "ID": "Customer ID",
        "Customer name": "Delivery name",
        "Delivery address 1": "Delivery address 1",
        "Delivery address 2": "Delivery address 2",
        "Delivery zip": "Delivery zip",
        "Delivery city": "Delivery city",
        "Delivery province code": "Delivery province code",
        "Delivery country code": "Delivery country code",
        "Billing country": "Billing country",
        "Delivery interval count": "Quantity"
    }

    # 7. Renommer les colonnes pour correspondre aux noms finaux
    df = df.rename(columns=column_mapping)

    # 8. Filtrer uniquement les colonnes nécessaires pour le fichier final
    columns_to_keep = list(column_mapping.values())
    df = df[[col for col in columns_to_keep if col in df.columns]]

    # 9. Assurer la présence de toutes les colonnes demandées, même si elles sont absentes du CSV initial
    final_columns = ['Customer ID', 'Delivery name', 'Delivery address 1', 'Delivery address 2', 
                     'Delivery zip', 'Delivery city', 'Delivery province code', 'Delivery country code', 
                     'Billing country', 'Quantity']
    for col in final_columns:
        if col not in df.columns:
            df[col] = ""  # Ajouter des colonnes manquantes avec des valeurs vides

    # 10. Réorganiser les colonnes pour correspondre à l'ordre final souhaité
    df = df[final_columns]

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
