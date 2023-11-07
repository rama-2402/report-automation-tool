import pandas as pd
import constants as const
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

percent_total_dict = dict()

final_ad_gen_revenue = 0
final_roas = 0
final_ad_order = 0
final_cpo = 0
final_avb = 0
final_conversion_rate = 0
final_impression = 0
final_clicks = 0
final_ctr = 0
final_cpc = 0
final_ad_spend = 0

final_campaign_name = ""

ad_metrics_data = pd.DataFrame()
ads_manager_data = pd.DataFrame()
overall_perf_data = pd.DataFrame()

def summary_and_total_percent():
    print(const.init_percent_total)
    global ad_metrics_data 
    ad_metrics_data = pd.read_csv(const.ad_metrics_data, sep="\t")
    global ads_manager_data
    ads_manager_data = pd.read_csv(const.ads_manager_data)
    global overall_perf_data
    overall_perf_data = pd.read_csv(const.overall_perf_data, sep="\t")
    ad_metrics_data["campaign_name"] = ad_metrics_data["campaign_name"].astype('string')
    ads_manager_data["Campaign name"] =  ads_manager_data["Campaign name"].astype('string')
    get_campaign_name()

    return percent_total_dict

def get_campaign_name():
    inp = str(input(const.campaign_name_prompt))
    # inp = "ML_NEWUSER_LCT_JUN23"
    check_campaign_name(inp)

def check_campaign_name(name: str):
    if name.lower() == "all":
        data_validation(name)
    elif name is None or name == "":
        print(const.none_campaign_name_prompt)
        get_campaign_name()
    elif name not in ad_metrics_data["campaign_name"].tolist():
        print(const.campaign_name_not_in_ad_metrics)
        get_campaign_name()  
    elif name not in ads_manager_data["Campaign name"].tolist():
        print(const.campaign_name_not_in_ads_manager)
        get_campaign_name()
    else:
        data_validation(name)

def data_validation(camp_name: str):

    global final_ad_gen_revenue
    global final_roas
    global final_ad_order
    global final_cpo
    global final_avb
    global final_conversion_rate
    global final_impression
    global final_clicks
    global final_ctr
    global final_cpc
    global final_ad_spend

    global final_campaign_name
    final_campaign_name = camp_name

    if camp_name != "all":
        c_ads_metrics = ad_metrics_data[ad_metrics_data["campaign_name"] == camp_name]
        c_ads_manager = ads_manager_data[ads_manager_data["Campaign name"] == camp_name]

    man_rev = c_ads_manager['Sales (MXN)'].sum()
    met_rev = c_ads_metrics['revenue_local'].sum()
    man_spend = c_ads_manager['Ad spend (MXN)'].sum()
    met_spend = c_ads_metrics['spend_local'].sum()
    man_orders = c_ads_manager['Orders'].sum()
    met_orders = c_ads_metrics['orders'].sum()
    man_clicks = c_ads_manager['Clicks'].sum()
    met_clicks = c_ads_metrics['clicks'].sum()
    man_imp = c_ads_manager['Impressions'].sum()
    met_imp = c_ads_metrics['impressions'].sum()

    final_ad_gen_revenue = const.convert_float(man_rev)
    final_roas = const.convert_float(man_rev/man_spend)
    final_ad_order = man_orders
    final_cpo = const.convert_float(man_spend/man_orders)
    final_avb = const.convert_float(man_rev/man_orders)
    final_conversion_rate = const.convert_float(man_orders/man_clicks)
    final_impression = man_imp
    final_clicks = man_clicks
    final_ctr = const.convert_float(man_clicks/man_imp)
    final_cpc = const.convert_float(man_spend/man_clicks)
    final_ad_spend = const.convert_float(man_spend)

    print("+------------------------+-----------------+-----------------+---------------+")
    print(f"|    Campaign Metrics    |   Ads Manager   |    Ad Metrics   |   Difference  |")
    print("+------------------------+-----------------+-----------------+---------------+")
    print(f"|  Ads Generated Revenue |    ${const.convert_float(man_rev)}   |    ${const.convert_float(met_rev)}   |     ${const.convert_float(man_rev - met_rev)}     |")
    print(f"|          ROAS          |    {const.convert_float(man_rev/man_spend)}%       |     {const.convert_float(met_rev/met_spend)}%      |      {const.convert_float((man_rev/man_spend) - (met_rev/met_spend))}     |")
    print(f"|  Ads Generated Orders  |     {man_orders}        |     {met_orders}        |        {const.convert_float(man_orders - met_orders)}      |")
    print(f"|     Cost per Order     |    ${const.convert_float(man_spend/man_orders)}       |    ${const.convert_float(met_spend/met_orders)}       |     {const.convert_float((man_spend/man_orders) - (met_spend/met_orders))}     |")
    print(f"|   Average Basket Size  |    ${const.convert_float(man_rev/man_orders)}      |    ${const.convert_float(met_rev/met_orders)}      |      {const.convert_float((man_rev/man_spend) - (met_rev/met_spend))}     |")
    print(f"|     Conversion Rate    |     {const.convert_float(man_orders/man_clicks)}%       |     {const.convert_float(met_orders/met_clicks)}%       |      {const.convert_float((man_rev/man_spend) - (met_rev/met_spend))}     |")
    print(f"|       Impression       |     {man_imp}      |     {met_imp}      |      {man_imp - met_imp}    |")
    print(f"|         Clicks         |       {man_clicks}      |      {met_clicks}       |        {man_clicks - met_clicks}      |")
    print(f"|          CTR           |     {const.convert_float(man_clicks/man_imp)}%       |     {const.convert_float(met_clicks/met_imp)}%       |      {const.convert_float((man_clicks/man_imp) - (met_clicks/met_imp))}     |")
    print(f"|          CPC           |      ${const.convert_float(man_spend/man_clicks)}      |     ${const.convert_float(met_spend/met_clicks)}       |      {const.convert_float((man_spend/man_clicks) - (met_spend/met_clicks))}    |")
    print(f"|       Ads Spend        |    ${const.convert_float(man_spend)}    |    ${const.convert_float(met_spend)}    |       ${const.convert_float(man_spend - met_spend)}  |")
    print("+------------------------+-----------------+-----------------+---------------+")

    confirmation = str(input(f"\n{const.output_confirmation}"))
    if confirmation == "1":
        create_percent_total()
    else:
        print("Script is terminated!")
        exit()

def create_percent_total():
    for i in range(5):
        if i == 1:
            create_data_and_graph("Impression", const.impressions_graph, final_impression, overall_perf_data["marketplace_impressions"].sum() + overall_perf_data["search_impressions"].sum() + overall_perf_data["carousel_impressions"].sum())
        elif i == 2:
            create_data_and_graph("Clicks", const.clicks_graph, final_clicks, overall_perf_data["clicks_from_marketplace"].sum() + overall_perf_data["clicks_from_search"].sum() + overall_perf_data["clicks_from_carousel"].sum())
        elif i == 3:
            create_data_and_graph("Orders", const.orders_graph, final_ad_order, overall_perf_data["orders_from_marketplace"].sum() + overall_perf_data["orders_from_search"].sum() + overall_perf_data["orders_from_carousel"].sum())
        elif i == 4:
            create_data_and_graph("Sales", const.sales_graph, final_ad_gen_revenue, overall_perf_data["food_sales_from_marketplace"].sum() + overall_perf_data["food_sales_from_search"].sum() + overall_perf_data["food_sales_from_carousel"].sum())
        else:
            create_data_and_graph_for_conversion("Conversion Rate", const.conversion_graph, (overall_perf_data["orders_from_marketplace"].sum() + overall_perf_data["orders_from_search"].sum() + overall_perf_data["orders_from_carousel"].sum()) / (overall_perf_data["clicks_from_marketplace"].sum() + overall_perf_data["clicks_from_search"].sum() + overall_perf_data["clicks_from_carousel"].sum()), final_ad_order/final_clicks)
    
    summary_df = pd.DataFrame.from_dict(
        {       
            "metric" : ["Ads Generated Revenue", "ROAS", "Ads Generated Orders", "Cost Per Order", "Average Basket Size", "Conversion Rate", "Impression", "Clicks", "CTR", "CPC", "Ads Spend"],
            "value" : [f"${final_ad_gen_revenue}", final_roas, final_ad_order, f"${final_cpo}", f"${final_avb}", f"{final_conversion_rate}%", final_impression, final_clicks, f"{final_ctr}%", f"${final_cpc}", f"${final_ad_spend}"]
        }
    )

    percent_total_dict[const.summary_sheet] = summary_df
    percent_total_dict[const.dict_campaign_name] = final_campaign_name

    percent_total_dict[const.dict_ads_manager_data] = ads_manager_data
    percent_total_dict[const.dict_ads_metrics_data] = ad_metrics_data
    percent_total_dict[const.dict_overall_perf_data] = overall_perf_data

    print(const.percent_total_calc_complete)

    return percent_total_dict
 

def create_data_and_graph(title: str, save_path:str, ads_data, organic_data):
    ads_data = float(ads_data)
    organic_data = float(organic_data)
    data_dict = {
        "metric":["Ads", "Organic", "Total", "% of Total"],
        "values":[const.convert_float(ads_data), const.convert_float(organic_data), const.convert_float(ads_data + organic_data), const.convert_percentage(ads_data/(ads_data + organic_data))]
        }
    data_df = pd.DataFrame.from_dict(data_dict)
    # print(data_df.head())

    percent_dict = {
        "Impression": [".", "%"],
        "Organic": [const.convert_float(organic_data), const.convert_percentage(organic_data/(ads_data + organic_data))],
        "Ads": [const.convert_float(ads_data), const.convert_percentage(ads_data/(ads_data + organic_data))]
    }

    percent_df = pd.DataFrame.from_dict(percent_dict)

    percent_total_dict[f"{title}_data"] = data_df
    percent_total_dict[title] = percent_df

    y = float(percent_df.loc[1].tolist()[1][:-1])
    z = float(percent_df.loc[1].tolist()[2][:-1])

    graph_df = pd.DataFrame.from_dict({
        "Organic": [y],
        "Ads": [z]
    })

    plt.clf()
    ax = graph_df.plot.bar(stacked = True, title=title, color={"#ff9900", "#cccccc"}, fig = (3,2))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xticklabels("%", rotation = 180)
    for p in ax.containers:
        ax.bar_label(p, label_type="center", fontweight='normal')
    fig = ax.get_figure()
    fig.savefig(save_path)
    # plt.clf()
    # plt.figure(figsize=(10,8))
    # plt.bar(x, y, color = "#cccccc")
    # plt.bar(x, z, bottom=y, color = "#ff9900")
    # plt.title(filter, fontdict={"fontsize":18,"fontweight":"bold","color":"#872410"}, pad=15)
    # plt.xlabel("Ads vs Organic", labelpad=20)
    # plt.ylabel(filter, labelpad=5)
    # #setting ylimit value
    # plt.ylim(0, 100)
    # #setting y ticks as percentage
    # # plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    # #customizing grid lines
    # plt.grid(axis='y',which = "major", linewidth = 0.5)
    # plt.grid(axis='y',which = "minor", linewidth = 0.2)
    # plt.minorticks_on()
    # # data label value for each bars
    # x = percent_df.loc[1].tolist()[1:]
    # count = 0
    # for p in pps:
    #     height = p.get_height()
    #     plt.annotate("{:.2%}".format(x[count]),
    #         xy=(p.get_x() + p.get_width() / 2, height),
    #         xytext=(0, 3), # 3 points vertical offset
    #         textcoords="offset points",
    #         ha='center', va='bottom')
    #     count = count + 1
    # #saving the graph as image
    # plt.savefig("imp.png")

def create_data_and_graph_for_conversion(title: str, save_path:str, organic, ads):
    organic = float(const.convert_float(organic * 100))
    ads = float(const.convert_float(ads * 100))
    graph_df = pd.DataFrame.from_dict({
        "Organic": [organic],
        "Ads": [ads]
    })
    print(graph_df.head())


    ax = graph_df.plot.bar(stacked = False, fig = (20,3), linewidth=1, title=title, color={"#cccccc", "#ff9900"})
    ax.set_ylim(0, max(graph_df["Organic"].loc[0], graph_df["Ads"].loc[0]) + 10)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_xticklabels("%", rotation = 180)
    for p in ax.containers:
            ax.bar_label(p, label_type="center", fontweight='normal')
    fig = ax.get_figure()
    fig.savefig(save_path)

    graph_df = pd.DataFrame.from_dict({
            "Organic": [f"{organic}%"],
            "Ads": [f"{ads}%"]
        })
    percent_total_dict[title] = graph_df

def calculate_roas(revenue, spend):
    return revenue/spend

def calculate_cpo(spend, orders):
    return spend/orders

def calculate_avb(revenue, orders):
    return revenue/orders

def calculate_conversion_rate(orders, clicks):
    return orders/clicks

def calculate_ctr(clicks, impression):
    return clicks/impression

def calculate_cpc(spend, clicks):
    return spend/clicks


if __name__ == "__main__":
    summary_and_total_percent()