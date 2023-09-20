# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 11:11:13 2023

@author: ben69
"""

# Librairies
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import numpy as np
from joblib import load

# Insérer du code HTML pour personnaliser le style de la sidebar
sidebar_custom_style = """
<style>
[data-testid="stSidebar"] {
    background-color: darkgrey;
}
.stOptionMenu {
    border-radius: 20px;
    padding: 20px;
    background-color: white;
}
.style{
    color: yellow;
}
"""

# Afficher le style personnalisé dans la sidebar
st.markdown(sidebar_custom_style, unsafe_allow_html=True)

# instanciation du Sidebar

menu_pays=['Accueil', 'France']

sous_menu_ligue={'Accueil':[],
                 'France':['Ligue1','Ligue2']}

selected_pays = st.sidebar.selectbox('PAYS', menu_pays)
selected_sous_menu_ligue = st.sidebar.selectbox("LIGUE", sous_menu_ligue[selected_pays])

if selected_pays == 'Accueil':
    st.title("Application Statistique des Matchs de Foot")

#################################################################################################

if selected_pays == 'France':
    if selected_sous_menu_ligue == 'Ligue1':
        st.title("Statistiques du Championnat Français : Ligue 1")
        st.write("Les statistiques reposent sur les 2 dernières saisons complètes ainsi que la saison en cours.")
        
        saison_n_3 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2021/F1.csv")
        saison_n_2 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2122/F1.csv")
        saison_n_1 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2223/F1.csv")
        saison_actu = pd.read_csv("https://www.football-data.co.uk/mmz4281/2324/F1.csv")  
        france_L1 = pd.concat([saison_n_3, saison_n_2, saison_n_1, saison_actu], axis=0)
        
        #st.dataframe(france_L1)
        
        

            #Sélection des colonnes
        data = france_L1[['Date','HomeTeam','AwayTeam','FTHG','FTAG','HS','AS','HST','AST','HC','AC']]

#Renomme les colonnes
        nom_colonnes=({'FTHG':'ScoreFinalHT',
               'FTAG':'ScoreFinalAT',
               'HS':'TirHT',
               'AS':'TirAT',
               'HST':'TirCadreHT',
               'AST':'TirCadreAT',
               'HC':'CornerHT',
               'AC':'CornerAT'})
        data = data.rename(columns=nom_colonnes)

#Ajout des colonnes de calculs
        data['TotalTirCadres']=data['TirCadreHT']+data['TirCadreAT']
        data['TotalTir']=data['TirAT']+data['TirHT']
        data['TotalBut']=data['ScoreFinalHT']+data['ScoreFinalAT']
        data['TotalCorner']=data['CornerHT']+data['CornerAT']
        data['Date']=data['Date'].apply(lambda line : line[-4:])
        data['But 2 Equipe']='Non'
        data.loc[(data['ScoreFinalHT']!=0)&(data['ScoreFinalAT']!=0), 'But 2 Equipe']='Oui'
        data['Plus de 1.5 But'] = 'Non'
        data.loc[(data['TotalBut']>=2), 'Plus de 1.5 But']='Oui'
        data['Plus de 2.5 But'] = 'Non'
        data.loc[(data['TotalBut']>=3), 'Plus de 2.5 But']='Oui'
        data["Winner"] = np.where(data["ScoreFinalHT"] > data["ScoreFinalAT"], data["HomeTeam"],
                         np.where(data["ScoreFinalHT"] < data["ScoreFinalAT"], data["AwayTeam"], "Match nul"))
        
        but_total = data['ScoreFinalHT'].sum() + data['ScoreFinalAT'].sum()
        total_tir_cadres = data['TotalTirCadres'].sum()

        #Perf Attaque
        data['AttaqueHT'] = ((data['ScoreFinalHT'] / but_total) * 100).round(2)
        data['AttaqueAT'] = ((data['ScoreFinalAT'] / but_total) * 100).round(2)
        #st.dataframe(data)
        
        st.write("-------------------------------------------------------------------------------------")

        st.markdown('<h3 style="color:green;font-weight:bold;font-size:20px;">Equipe Domcile:</h3>', unsafe_allow_html=True)
        domicile = st.selectbox("Choisissez une Equipe Domicile", data['HomeTeam'].unique())
        exterieur = st.selectbox("Choisissez une Equipe Exterieur", data['HomeTeam'].unique())
        
        col1, col2 = st.columns(2)
        
            #Calcul
        with col1:
            resultats_dom = data.loc[(data['HomeTeam']==domicile)|(data['AwayTeam']==domicile)]
            but_marques = resultats_dom['ScoreFinalHT'].sum()+resultats_dom['ScoreFinalAT'].sum()
            tir_cadres = resultats_dom['TirCadreHT'].sum()+resultats_dom['TirCadreAT'].sum()
            corner = resultats_dom['CornerHT'].sum()+resultats_dom['CornerAT'].sum()
            
            st.write("--------------------------------------------")
            st.write("Résultats Statistiques (saison précédente et actuelle):")
            st.write("Nombre de buts marqués:", but_marques)
            st.write("Moyenne de Buts marqués par match:", (but_marques/len(resultats_dom['HomeTeam'])).round(2))
            st.write("Nombre de Tirs Cadrés:", tir_cadres)
            st.write("Moyenne de Tirs Cadrés:", (tir_cadres/len(resultats_dom['HomeTeam'])).round(2))
            st.write("Nombre de Corner:", corner)
            st.write("Moyenne de Corner par Match:", (corner/len(resultats_dom['HomeTeam'])).round(2))
        
        with col2:
            resultats_2 = data.loc[(data['HomeTeam']==exterieur)|(data['AwayTeam']==exterieur)]
            but_marques_2 = resultats_2['ScoreFinalHT'].sum()+resultats_2['ScoreFinalAT'].sum()
            tir_cadres_2 = resultats_2['TirCadreHT'].sum()+resultats_2['TirCadreAT'].sum()
            corner_2 = resultats_2['CornerHT'].sum()+resultats_2['CornerAT'].sum()
            
            st.write("--------------------------------------------")
            st.write("Résultats Statistiques (saison précédente et actuelle):")
            st.write("Nombre de buts marqués:", but_marques_2)
            st.write("Moyenne de Buts marqués par match:", (but_marques_2/len(resultats_2['HomeTeam'])).round(2))
            st.write("Nombre de Tirs Cadrés:", tir_cadres_2)
            st.write("Moyenne de Tirs Cadrés:", (tir_cadres_2/len(resultats_2['HomeTeam'])).round(2))
            st.write("Nombre de Corner:", corner_2)
            st.write("Moyenne de Corner par Match:", (corner_2/len(resultats_2['HomeTeam'])).round(2))
             
        #equipe_ligue_1 = saison
        #st.selectbox('Sélectionner une équipe', equipe_ligue_1)
        
        st.write("--------------------------------------------------------------------------------------")
        st.markdown('<h3 style="color:green;font-weight:bold;font-size:20px;">Confrontations:</h3>', unsafe_allow_html=True)
        confrontations = data.loc[((data['HomeTeam']==domicile)&(data['AwayTeam']==exterieur))|((data['HomeTeam']==exterieur)&(data['AwayTeam']==domicile))]
        st.dataframe(confrontations)
        resultats_confrontations = confrontations['Winner'].value_counts()
        victoire_dom = resultats_confrontations.get(domicile,0)
        st.write("Nombre de Victoires pour",domicile,":",victoire_dom)
        victoire_ext = resultats_confrontations.get(exterieur,0)
        st.write("Nombre de Victoires pour",exterieur,":",victoire_ext)
        match_nul = len(confrontations) - (victoire_dom + victoire_ext)
        st.write('Le nombre de Match Nul est:', match_nul)
        
        st.write("--------------------------------------------------------")
        st.markdown('<h3 style="color:green;font-weight:bold;font-size:20px;">Probabilitées des 3 dernières saisons et actuelle:</h3>', unsafe_allow_html=True)
        
        #Plus de n But
        over_1_but = 0
        under_1_but = 0
        
        for i in confrontations['TotalBut']:
            if i >= 2:
                over_1_but += 1
            elif i < 2:
                under_1_but += 1
        
        probs_over_1 = ((over_1_but/len(confrontations['TotalBut']))*100)
        probs_under_1 = ((under_1_but/len(confrontations['TotalBut']))*100)
            
                    
        st.write("Probabilitées qu'il y ai plus de 1.5 but dans le match:", round(probs_over_1,2), "%")
        st.write("Probabilitées qu'il y ai moins de 1.5 but dans le match:", round(probs_under_1,2), "%")
        
        over_2_but = 0
        under_2_but = 0
        
        for i in confrontations['TotalBut']:
            if i >= 3:
                over_2_but += 1
            elif i < 2:
                under_2_but += 1
        
        probs_over_2 = ((over_2_but/len(confrontations['TotalBut']))*100)
        probs_under_2 = ((under_2_but/len(confrontations['TotalBut']))*100)
            
                    
        st.write("Probabilitées qu'il y ai plus de 2.5 but dans le match:", round(probs_over_2,2), "%")
        st.write("Probabilitées qu'il y ai moins de 2.5 but dans le match:", round(probs_under_2,2), "%")
        
        #But pour les deux équipe
        count_oui = 0
        count_non = 0
        
        for i in confrontations['But 2 Equipe']:
            if i == 'Oui':
                count_oui += 1
            elif i == 'Non':
                count_non += 1
        
        probs_but_2_equipe_oui = ((count_oui/len(confrontations['But 2 Equipe']))*100)
        probs_but_2_equipe_non = ((count_non/len(confrontations['But 2 Equipe']))*100)
            
                    
        st.write("Probabilitées que les deux équipe marquent:", round(probs_but_2_equipe_oui,2), "%")
        st.write("Probabilitées que les deux équipes ne marquent pas:", round(probs_but_2_equipe_non,2), "%")
        
        st.write('-----------------------------------------------------------')
        st.markdown('<h3 style="color:green;font-weight:bold;font-size:20px;">Prédictions:</h3>', unsafe_allow_html=True)
        domicile_pred = domicile
        exterieur_pred = exterieur
        
        saison_n_1 = pd.read_csv("https://www.football-data.co.uk/mmz4281/2223/F1.csv")
        saison_actu = pd.read_csv("https://www.football-data.co.uk/mmz4281/2324/F1.csv")  
        origine = pd.concat([saison_n_1, saison_actu], axis=0)
        
        data_pred = origine[['Date','HomeTeam','AwayTeam','FTHG','FTAG','HS','AS','HST','AST','HC','AC']]

        #Renomme les colonnes
        nom_colonnes=({'FTHG':'ScoreFinalHT',
               'FTAG':'ScoreFinalAT',
               'HS':'TirHT',
               'AS':'TirAT',
               'HST':'TirCadreHT',
               'AST':'TirCadreAT',
               'HC':'CornerHT',
               'AC':'CornerAT'})
        data_pred = data_pred.rename(columns=nom_colonnes)

        #Ajout des colonnes de calculs
        data_pred['TotalTirCadres']=data_pred['TirCadreHT']+data_pred['TirCadreAT']
        data_pred['TotalTir']=data_pred['TirAT']+data_pred['TirHT']
        data_pred['TotalBut']=data_pred['ScoreFinalHT']+data_pred['ScoreFinalAT']
        data_pred['TotalCorner']=data_pred['CornerHT']+data_pred['CornerAT']
        data_pred['Date']=data_pred['Date'].apply(lambda line : line[-4:])
        data_pred['But 2 Equipe']='Non'
        data_pred.loc[(data_pred['ScoreFinalHT']!=0)&(data_pred['ScoreFinalAT']!=0), 'But 2 Equipe']='Oui'
        data_pred['Plus de 1.5 But'] = 'Non'
        data_pred.loc[(data_pred['TotalBut']>=2), 'Plus de 1.5 But']='Oui'
        data_pred['Plus de 2.5 But'] = 'Non'
        data_pred.loc[(data_pred['TotalBut']>=3), 'Plus de 2.5 But']='Oui'
        data_pred["Winner"] = np.where(data_pred["ScoreFinalHT"] > data_pred["ScoreFinalAT"], data_pred["HomeTeam"],
                         np.where(data_pred["ScoreFinalHT"] < data_pred["ScoreFinalAT"], data_pred["AwayTeam"], "Match nul"))
        
        but_total = data_pred['ScoreFinalHT'].sum() + data_pred['ScoreFinalAT'].sum()
        total_tir_cadres = data_pred['TotalTirCadres'].sum()

        #Perf Attaque
        data_pred['AttaqueHT'] = ((data_pred['ScoreFinalHT'] / but_total) * 100).round(2)
        data_pred['AttaqueAT'] = ((data_pred['ScoreFinalAT'] / but_total) * 100).round(2)
        
        #Création d'un dataset avec les performances moyennes et mises à jour automatique à chaque journées de championnat.
        stats_equipes_HT = data_pred.groupby(['HomeTeam']).agg({'AttaqueHT':'mean',
                                                                'TirHT':'mean',                                                        
                                                                'TirCadreHT':'mean',
                                                                'CornerHT':'mean'}).reset_index()

        stats_equipes_AT = data_pred.groupby(['AwayTeam']).agg({'AttaqueAT':'mean',
                                                                'TirAT':'mean',
                                                                'TirCadreAT':'mean',
                                                                'CornerAT':'mean'}).reset_index()

        stats = pd.concat([stats_equipes_HT, stats_equipes_AT],axis=1, ignore_index=True)

        stats = stats.rename(columns={0:'Equipe',
                                      1:'AttaqueHT',
                                      2:'TirHT',
                                      3:'TirCadreHT',
                                      4:'CornerHT',
                                      5:'Equipe-2',
                                      6:'AttaqueAT',
                                      7:'TirAT',
                                      8:'TirCadreAT',
                                      9:'CornerAT'})

        stats=stats.drop('Equipe-2', axis=1)

        stats_df = pd.DataFrame(stats)
        
        equipe_1 = stats_df.loc[stats_df['Equipe']==domicile].reset_index()
        equipe_2 = stats_df.loc[stats_df['Equipe']==exterieur].reset_index()

        equipe_2 = equipe_2.rename(columns={'Equipe':'Equipe_2',
                                            'AttaqueHT':'AttaqueHT_2',
                                            'TirHT':'TirHT_2',
                                            'TirCadreHT':'TirCadreHT_2',
                                            'CornerHT':'CornerHT_2',
                                            'AttaqueAT':'AttaqueAT_2',
                                            'TirAT':'TirAT_2',
                                            'TirCadreAT':'TirCadreAT_2',
                                            'CornerAT':'CornerAT_2',})

        stats_pred = equipe_1.merge(equipe_2, left_index=True, right_index=True)
        stats_pred.reset_index()
        stats_pred.drop(['index_x','index_y'], axis=1)
        predictions_final = stats_pred[['Equipe', 'Equipe_2', 'AttaqueHT', 'AttaqueAT_2', 'TirCadreHT', 'TirCadreAT_2', 'CornerHT', 'CornerAT_2']]

        predictions_final['Equipe'] = predictions_final['Equipe'].map({'Lyon':0, 'Strasbourg':1, 'Clermont':2, 'Toulouse':3, 'Angers':4, 'Lens':5, 'Lille':6,
                                                                       'Montpellier':7, 'Rennes':8, 'Marseille':9, 'Nantes':10, 'Monaco':11, 'Paris SG':12,
                                                                       'Ajaccio':13, 'Auxerre':14, 'Reims':15, 'Troyes':16, 'Nice':17, 'Brest':18, 'Lorient':19,
                                                                       'Metz':20, 'Le Havre':21})

        predictions_final['Equipe_2'] = predictions_final['Equipe_2'].map({'Lyon':0, 'Strasbourg':1, 'Clermont':2, 'Toulouse':3, 'Angers':4, 'Lens':5, 'Lille':6,
                                                                           'Montpellier':7, 'Rennes':8, 'Marseille':9, 'Nantes':10, 'Monaco':11, 'Paris SG':12,
                                                                           'Ajaccio':13, 'Auxerre':14, 'Reims':15, 'Troyes':16, 'Nice':17, 'Brest':18, 'Lorient':19,
                                                                           'Metz':20, 'Le Havre':21})
        
        predictions_final = predictions_final.rename(columns={'Equipe':'HomeTeam',
                                                              'Equipe_2':'AwayTeam',
                                                              'AttaqueAT_2':'AttaqueAT',
                                                              'TirCadreAT_2':'TirCadreAT',
                                                              'CornerAT_2':'CornerAT'})
        
        final_model = load('Model-Sport-1.joblib')
        final = final_model.predict(predictions_final)
        
        #Correspondances
        names_teams = {0:'Lyon', 1:'Strasbourg', 2:'Clermont', 3:'Toulouse', 4:'Angers', 5:'Lens', 6:'Lille',
                       7:'Montpellier', 8:'Rennes', 9:'Marseille', 10:'Nantes', 11:'Monaco', 12:'Paris SG',
                       13:'Ajaccio', 14:'Auxerre', 15:'Reims', 16:'Troyes', 17:'Nice', 18:'Brest', 19:'Lorient',
                       20:'Metz', 21:'Le Havre', 22:'Match Nul'}
        
        resultat = [names_teams[i] for i in final]
        
        st.write("Le résultat du match est:", resultat)
        
        st.dataframe(predictions_final)