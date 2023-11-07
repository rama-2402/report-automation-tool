import pandas as pd
import numpy as np

user_id = "rramak2"

#paths
data_path = f"/Users/{user_id}/Documents/projects/pcr/data"
output_path = f"/Users/{user_id}/Documents/projects/pcr/output"

#template files
g_sheet_template = f"{data_path}/gsheet_template.xlsx"
tldr_template = f"{data_path}/tldr_template.docx"

#raw data files
campaign_incrementality_data = f"{data_path}/camp_incr.tsv"
ad_metrics_data = f"{data_path}/ad_metrics.tsv"
top_performers_cities_data = f"{data_path}/top_perf_cities.tsv"
top_performers_restaurants_data = f"{data_path}/top_perf_resto.tsv"
ads_manager_data = f"{data_path}/ads_manager.csv"
overall_perf_data = f"{data_path}/overall_performance.tsv"
eaters_data = f"{data_path}/new_and_repeat.tsv"
uber_one_data = f"{data_path}/uber_one.tsv"


#output data files
camp_incr_graph = f"{output_path}/camp_incr_graph.png"
top_cities_graph = f"{output_path}/top_cities_graph.png"
top_restos_graph = f"{output_path}/top_restos_graph.png"
impressions_graph = f"{output_path}/impressions_graph.png"
clicks_graph = f"{output_path}/clicks_graph.png"
orders_graph = f"{output_path}/orders_graph.png"
sales_graph = f"{output_path}/sales_graph.png"
conversion_graph = f"{output_path}/conversion_graph.png"
order_new_eater_graph = f"{output_path}/order_new_eater_graph.png"
abs_new_eater_graph = f"{output_path}/abs_new_eater_graph.png"
sales_new_eater_graph = f"{output_path}/sales_new_eater_graph.png"
tldr = f"{output_path}/tldr.docx"
gsheet = f"{output_path}/gsheet.xlsx"


pcr_summary_sheet = "AM data summary"
ads_manager_sheet = "ADS Manager"
ads_metrics_sheet = "Ads Metrics UUID"
camp_incr_sheet = "Campaign Incrementality"
top_perf_sheet = "Top Performers"
percent_total_sheet = "% of total"
uber_one_sheet = "UberOne Data"
eaters_sheet = "New and Repeat Eater"
overall_perf_sheet = "Overall performance"

#status
init_campaign_incrementality = "\nProcessing Campaign Incrementality..."
campaign_incrementality_validation = "Validating Campaign Incrementality PRE vs TEST..."
campaign_incrementality_test_pass = "Campaign Incrementality Test: PASS"
campaign_incrementality_test_fail = "Campaign Incrementality Test: FAIL"
campaign_incr_test_fail_error = "Check your Campaign Incrementality data and try again.!"
campaign_incrementality_graph_title = "Please provide a Title for the Campaign Incrementality Graph: \n"
campaign_incrementality_default_graph_title = "Campaign Incrementality"
campaign_incrementality_graph_x_label = "Performance Summary"
campaign_incrementality_graph_y_label = "Lift"
campaign_incrementality_complete = "Campaign Incrementality G-Sheet Complete!"
campaign_incrementality_tldr_complete = "Campaign Incrementality TLDR Complete!"

unique_restro_status = "Fetching Unique resto uuids..."
unique_restro_output_status = "Total unique resto_uuid: "

init_top_performers = "\nProcessing Top Performance Cities and Restaurants..."
top_perf_cities_graph_title = "Cities vs ROAS & Conversion Rate"
top_performers_sheet = "Top Performers"
top_perf_complete = "Top Performers Cities and Restos complete!"
top_perf_cities_graph_title = "Cities vs ROAS & Conversion Rate"
top_perf_restos_graph_title = "Store vs ROAS & Conversion Rate"

percent_sheet = "% of total"
init_percent_total = "\nPreparing % Total sheet..."
percent_total_complete = "\n% Total G-Sheet complete!"
percent_total_calc_complete = "\n% Total calculations complete!"

summary_sheet = "AM data summary"

init_ads_data_validation = "Initializing Data validation for Ads manager vs Ad metrics query..."
campaign_name_prompt = "Please provide the campaign name to filter. If the PCR is for all campaigns type all:\n"
none_campaign_name_prompt = "Please provide a valid Campaign Name!"
campaign_name_not_in_ad_metrics = "Campaign Name not found in Ad Metrics query data!"
campaign_name_not_in_ads_manager = "Campaign Name not found in Ads Manager data!"
output_confirmation = "If data looks good enter, \n1 -> continue\n2 -> exit\n\n"
eaters_complete = "Eaters data calculations complete!"

dict_camp_incr_data = "incr"
dict_pre_vs_test_table = "prevstest"
dict_top_restos_data = "toprestos"
dict_top_cities_data = "topcities"
dict_ads_manager_data = "adsmanager"
dict_ads_metrics_data = "admetrics"
dict_overall_perf_data = "overall"
dict_eaters_data = "eaters"
dict_uber_one_data = "uberone"
dict_eaters_table = "eaterstable"

dict_ad_gen_revenue = "revenue"
dict_roas = "roas"
dict_ad_order = "orders"
dict_cpo = "cpo"
dict_avb = "avb"
dict_conversion_rate = "convrate"
dict_impression = "impression"
dict_clicks = "clicks"
dict_ctr = "ctr"
dict_cpc = "cpc"
dict_ad_spend = "spend"
dict_campaign_name = "campaignname"



def check_df_for_errors(df: pd.DataFrame, columns) -> pd.DataFrame:
    for col in columns:
        df[pd.to_numeric(df[col], errors='coerce').isnull()][col].apply(lambda x: 0)
        df[col] = df[col].apply(lambda x: convert_zero(x))
        df[col] = df[col].astype(np.float64)
    return df

def convert_zero(val):
    try:
        float(val)
        return val
    except:
        return "0"

def convert_float(number: float):
    return "{:.2f}".format(number)

def convert_percentage(number: float):
    return "{:.2%}".format(number)
