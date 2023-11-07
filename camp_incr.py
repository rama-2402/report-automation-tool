import pandas as pd
import constants as const
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from datetime import datetime
import save_file as op

camp_incr_dict = dict()

def camp_incr_check():
    print(const.init_campaign_incrementality)
    print(const.campaign_incrementality_validation)
    camp_incr = pd.read_csv(const.campaign_incrementality_data, sep="\t")

    camp_incr = const.check_df_for_errors(camp_incr, ["orders", "ABS", "food_sales_local", "eaters", "new_eaters"] )

    pre = camp_incr["cohort"] == "PRE"
    test = camp_incr["cohort"] == "TEST"

    start_pre = camp_incr[camp_incr["cohort"] == "PRE"]["daylabel"].min()
    end_pre = camp_incr[camp_incr["cohort"] == "PRE"]["daylabel"].max()
    start_test = camp_incr[camp_incr["cohort"] == "TEST"]["daylabel"].min()
    end_test = camp_incr[camp_incr["cohort"] == "TEST"]["daylabel"].max()

    camp_incr_dict["prestart"] = start_pre
    camp_incr_dict["preend"] = end_pre
    camp_incr_dict["teststart"] = start_test
    camp_incr_dict["testend"] = end_test
    
    if len(camp_incr[pre]) == len(camp_incr[test]):
        print(f"pre({len(camp_incr[pre])}) = TEST({len(camp_incr[test])})")
        print(const.campaign_incrementality_test_pass)
        prep_incr(camp_incr)
        return camp_incr_dict
    else:
        print(const.campaign_incrementality_test_fail)
        print(f"pre({len(camp_incr[pre])}) != TEST({len(camp_incr[test])})")
        print(const.campaign_incr_test_fail_error)
        exit()


def prep_incr(incr: pd.DataFrame):

    # startpre = min(incr[incr["cohort"] == "PRE"]["daylabel"])[:10]
    # endpre = max(incr[incr["cohort"] == "PRE"]["daylabel"])[:10]

    t_camp_incr: pd.DataFrame = pd.DataFrame([])
    t_camp_incr["Performance Summary"] = ["Pre", "Test", "Lift"]

    #orders
    p_order_sum = incr[incr["cohort"] == "PRE"]["orders"].sum()
    t_order_sum = incr[incr["cohort"] == "TEST"]["orders"].sum()
    t_camp_incr["Orders"] = [p_order_sum, t_order_sum, (t_order_sum-p_order_sum)/p_order_sum]

    #Avg basked size
    p_abs_sum = incr[incr["cohort"] == "PRE"]["ABS"].mean()
    t_abs_sum = incr[incr["cohort"] == "TEST"]["ABS"].mean()
    t_camp_incr["Avg Basket Size"] = [p_abs_sum, t_abs_sum, (t_abs_sum-p_abs_sum)/p_abs_sum]

    #food_sales_local
    p_sales_sum = incr[incr["cohort"] == "PRE"]["food_sales_local"].sum()
    t_sales_sum = incr[incr["cohort"] == "TEST"]["food_sales_local"].sum()
    t_camp_incr["Food Sales"] = [p_sales_sum, t_sales_sum, (t_sales_sum-p_sales_sum)/p_sales_sum]

    #eaters
    p_eaters_sum = incr[incr["cohort"] == "PRE"]["eaters"].sum()
    t_eaters_sum = incr[incr["cohort"] == "TEST"]["eaters"].sum()
    t_camp_incr["Eaters"] = [p_eaters_sum, t_eaters_sum, (t_eaters_sum-p_eaters_sum)/p_eaters_sum]

    #new_eaters
    p_neweaters_sum = incr[incr["cohort"] == "PRE"]["new_eaters"].sum()
    t_neweaters_sum = incr[incr["cohort"] == "TEST"]["new_eaters"].sum()
    t_camp_incr["New Eaters"] = [p_neweaters_sum, t_neweaters_sum, (t_neweaters_sum-p_neweaters_sum)/p_neweaters_sum]

    temp_df = t_camp_incr.drop([t_camp_incr.index[0], t_camp_incr.index[1]])

    plt.clf()
    plt.figure(figsize=(10,8))
    pps = plt.bar(temp_df.columns.tolist()[1:], temp_df.loc[2].tolist()[1:], color = "#93c47d", width=0.5)
    plt.title(const.campaign_incrementality_default_graph_title, fontdict={"fontsize":18,"fontweight":"bold","color":"#872410"}, pad=15)
    plt.xlabel(const.campaign_incrementality_graph_x_label, labelpad=20)
    plt.ylabel(const.campaign_incrementality_graph_y_label, labelpad=5)
    #setting ylimit value
    plt.ylim(min(temp_df.loc[2].tolist()[1:]) - 0.005, max(temp_df.loc[2].tolist()[1:]) + 0.005)
    #setting y ticks as percentage
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    #customizing grid lines
    plt.grid(axis='y',which = "major", linewidth = 0.5)
    plt.grid(axis='y',which = "minor", linewidth = 0.2)
    plt.minorticks_on()
    #data label value for each bars
    x = temp_df.loc[2].tolist()[1:]
    count = 0
    for p in pps:
        height = p.get_height()
        plt.annotate("{:.2%}".format(x[count]),
            xy=(p.get_x() + p.get_width() / 2, height),
            xytext=(0, 3), # 3 points vertical offset
            textcoords="offset points",
            ha='center', va='bottom')
        count = count + 1
    #saving the graph as image
    plt.savefig(const.camp_incr_graph)

    camp_incr_dict[const.dict_camp_incr_data] = t_camp_incr
    camp_incr_dict[const.dict_pre_vs_test_table] = incr

    print(const.campaign_incrementality_complete)

    #saving campaign incrementality to excel
    # op.write_excel(t_camp_incr, const.campaign_incrementality_default_graph_title, 5, 1, const.camp_incr_graph, "I5")
    # #campaign incrementality data for TLDR
    # content = {
    #     "liftsales": "{:.2%}".format(t_camp_incr.iat[2,3]),
    #     "liftorder": "{:.2%}".format(t_camp_incr.iat[2,1]),
    #     "lifteater": "{:.2%}".format(t_camp_incr.iat[2,4]),
    #     "liftne": "{:.2%}".format(t_camp_incr.iat[2,5]),
    #     "liftavb": "{:.2%}".format(t_camp_incr.iat[2,2]),

    #     # "pliftsales": "{:,}".format("{:.2f}".format(t_camp_incr.iat[0,3])),
    #     "pliftsales": "{:,}".format(int(t_camp_incr.iat[0,3])),
    #     "pliftorder": "{:,}".format(int(t_camp_incr.iat[0,1])),
    #     "plifteater": "{:,}".format(int(t_camp_incr.iat[0,4])),
    #     "pliftne": "{:,}".format(int(t_camp_incr.iat[0,5])),
    #     "pliftavb": "{:.2f}".format(t_camp_incr.iat[0,2]),

    #     "tliftsales": "{:,}".format(int(t_camp_incr.iat[1,3])),
    #     "tliftorder": "{:,}".format(int(t_camp_incr.iat[1,1])),
    #     "tlifteater": "{:,}".format(int(t_camp_incr.iat[1,4])),
    #     "tliftne": "{:,}".format(int(t_camp_incr.iat[1,5])),
    #     "tliftavb": "{:.2f}".format(t_camp_incr.iat[1,2]),

    #     "startpre": startpre,
    #     "endpre": endpre
    # }
    # #saving campaign incrementality to TLDR
    # op.write_doc(content=content, img=const.camp_incr_graph, height=5.3, width=6.7)
    # print(const.campaign_incrementality_tldr_complete)

 