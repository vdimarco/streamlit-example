import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import pytz

from sklearn.metrics import (accuracy_score, auc, f1_score, precision_score, recall_score,
                            mean_absolute_error, mean_squared_error, r2_score)
st.set_option('deprecation.showfileUploaderEncoding', False)

# funtions
def relative_time(t_diff):
    days, seconds = t_diff.days, t_diff.seconds
    if days > 0: 
        return f"{days}d"
    else:
        hours = t_diff.seconds // 3600
        minutes = t_diff.seconds // 60
        if hours >0 : #hour
            return f"{hours}h"
        elif minutes >0:
            return f"{minutes}m"
        else:
            return f"{seconds}s"

# TODO: last updated on X date

def get_leaderboard_dataframe(csv_file = 'leaderboard.csv', greater_is_better = True):
    df_leaderboard = pd.read_csv('leaderboard.csv')
    # df_leaderboard.columns = ['rank','index','Pick1','Pick2','Pick3','Name','Submitted_At','Paid','Return1','Return2','Return3','Score','Competition_Start','Competition_End']
    df_leaderboard['counter'] = 1
    df_leaderboard = df_leaderboard.groupby('Name').agg({
                                                            # "Submitted_At": "max",
                                                            "Score": "max",
                                                            # "counter": "count",
                                                            "Pick1": "max",
                                                            "Pick2": "max",
                                                            "Pick3": "max",
                                                            # "Submitted": "max",
                                                            # "Competition_Number" : "max"
                                                            })
    df_leaderboard = df_leaderboard.sort_values("Score", ascending = not greater_is_better)
    df_leaderboard = df_leaderboard.reset_index()                                                    
    df_leaderboard.columns = ['Username','Score', '1st Pick','2nd Pick','3rd Pick']
    # df_leaderboard['Submission Time'] = df_leaderboard['Submitted']
    return df_leaderboard

# Title
# st.title("Global Leaderboard")

# Username Input
# username = st.text_input("Username", value = "Wiz", max_chars= 20,)
# username = username.replace(",","") # for storing csv purpose
# st.header(f"What's Up {username}!")


# Check if master data has been registered:
master_files = os.listdir('master')
if ("df_master.csv" not in master_files) | ("cfg_master.json" not in master_files):
    st.text("Admin please insert master data")
elif (os.stat("master/df_master.csv").st_size == 0) | (os.stat("master/cfg_master.json").st_size == 0):
    st.text("Master data should not empty")
else:
    # Load Master
    df_master = pd.read_csv('master/df_master.csv')
    with open('master/cfg_master.json') as json_file:
        cfg_master = json.load(json_file)

    competition_type, metric_type= cfg_master['competition_type'], cfg_master['metric_type']
    index_col, target_col = cfg_master['index_col'], cfg_master['target_col']



    st.text("####### Updated {}".format(datetime.today().strftime("%Y-%m-%d")))
    # st.code(f"""
    #     Competition Type: {competition_type}
    #     Metric: {metric_type}
    #     index  column name : {index_col}
    #     target column name : {target_col}
    # """)

    # set scorer as metric type
    scorer_dict = {"Accuracy": accuracy_score, "Precision": precision_score, "Recall" : recall_score, "Auc" : auc, 
                    "F1": f1_score, "MAE" : mean_absolute_error, "MSE" : mean_squared_error, "r2": r2_score}
    scorer = scorer_dict[metric_type] # CHANGE HERE AS YOU WANT
    greater_is_better = False if metric_type in ["MAE", "MSE"] else True # CHANGE HERE AS YOU WANT

    # uploaded_file = st.file_uploader("Upload Submission CSV File",type='csv')
    # if st.button("SUBMIT"):
    #     if uploaded_file is None:
    #         st.text("UPLOAD FIRST")
    #     else:
    #         # save submission
    #         df_submission = pd.read_csv(uploaded_file)
    #         datetime_now = datetime.now().strftime("%Y%m%d_%H%M%S")
    #         filename_submission = f"submission/sub_{username}__{datetime_now}.csv"
    #         df_submission[[index_col, target_col]].to_csv(filename_submission, index = False)
    #         # calculate score
    #         df = df_master.merge(df_submission, how = 'left', on = index_col)
    #         score = scorer(df[target_col + "_x"], df[target_col + "_y"]) # scorer(true_label, pred_label)
    #         score = round(score,5)
    #         st.text(f"YOUR {metric_type}: {score}")
    #         # save score
    #         with open("leaderboard.csv", "a+") as leaderboard_csv:
    #             leaderboard_csv.write(f"{username},{score},{datetime_now}\n")

    # Showing Leaderboard 
    # st.text("Leaderboard Updated Daily")
    if os.stat("leaderboard.csv").st_size == 0:
        st.text("NO SUBMISSION YET")
    else:
        df_leaderboard = get_leaderboard_dataframe(csv_file = 'leaderboard.csv', greater_is_better = greater_is_better)
        st.write(df_leaderboard)

# # To register master data
# if username == 'wiseguy':
#     change_master_key = st.checkbox('Change Master Key')

#     if change_master_key:
#         # Set competition properties
#         competition_type = ["Binary Classification", "Multi Class Classification", "Regression",]
#         choosen_competition_type = st.selectbox("Select Competition Type",competition_type)
#         metric_type_dict = {"Binary Classification": ["Accuracy", "Precision", "Recall", "Auc", "F1"], 
#                             "Multi Class Classification" : ["Accuracy"], 
#                             "Regression" : ["MAE", "MSE", "r2"]}
#         metric_type = metric_type_dict[choosen_competition_type]
#         choosen_metric_type = st.selectbox("Select Metric Type",metric_type)

#         # Master Data Frame
#         uploaded_file_master = st.file_uploader("Upload Master CSV File",type='csv')
#         if uploaded_file_master is not None:
#             df_master_register = pd.read_csv(uploaded_file_master)
#             columns_master = list(df_master_register.columns)
#             # Choose required Columns
#             choosen_col_index  = st.selectbox("Select Index Column",columns_master)
#             choosen_col_target = st.selectbox("Select Target Column",[col for col in columns_master if col != choosen_col_index])
#             if st.checkbox('Show Master Data'):
#                 st.text(f"TOTAL ROW: {len(df_master_register)}")
#                 df_master_register.loc[:99, [choosen_col_index, choosen_col_target]]
#             # Change the master dataset
#             if st.button("CHANGE"):
#                 if df_master_register[choosen_col_index].value_counts().max() == 1:
#                     filename_master = "master/df_master.csv"
#                     filename_master_cfg = "master/cfg_master.json"
#                     df_master_register[[choosen_col_index, choosen_col_target]].to_csv(filename_master, index = False)
#                     st.text(f"Master data saved into {filename_master}")
#                     cfg_master_register = {"competition_type" : choosen_competition_type,
#                                             "metric_type" : choosen_metric_type,
#                                             "index_col" : choosen_col_index,
#                                             "target_col" : choosen_col_target}
#                     with open(filename_master_cfg, 'w') as outfile:
#                         json.dump(cfg_master_register, outfile)
#                     st.text(f"Master config saved into {filename_master_cfg}")
#                     # Change current master
#                     cfg_master = cfg_master_register.copy()
#                     df_master = df_master_register.copy()
#                 else:
#                     st.text("Index columns is not unique, cannot process")
    