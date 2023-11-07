import pandas as pd
import matplotlib.pyplot as plt
import constants as const
import numpy as np

eaters_df = pd.DataFrame()
final_eaters_dict = dict()

def new_eaters_analysis():
    global eaters_df
    eaters_raw_data = pd.read_csv(const.eaters_data, sep="\t")
    uber_one_raw = pd.read_csv(const.uber_one_data, sep="\t", header=1)

    eaters_raw_data = const.check_df_for_errors(eaters_raw_data, ["new_eaters_to_resto_orders", "new_eaters_to_resto_sales", "return_eaters_to_resto_orders", "return_to_resto_sales"])
    uber_one_raw = const.check_df_for_errors(uber_one_raw, ["pass_food_sales", "pass_orders"])

    eaters_dict = {
            "Eaters": ["New Eater", "Repeat Eater", "Uber One Eater"],
            "Order": [eaters_raw_data["new_eaters_to_resto_orders"].sum(), eaters_raw_data["return_eaters_to_resto_orders"].sum(), uber_one_raw["pass_orders"].sum()],
            "Sales": [eaters_raw_data["new_eaters_to_resto_sales"].sum(), eaters_raw_data["return_to_resto_sales"].sum(), uber_one_raw["pass_food_sales"].sum()]
    }
    eaters_dict["ABS"] = [float(eaters_dict["Sales"][0])/float(eaters_dict["Order"][0]), float(eaters_dict["Sales"][1])/float(eaters_dict["Order"][1]), float(eaters_dict["Sales"][2])/float(eaters_dict["Order"][2])]

    eaters_df = pd.DataFrame.from_dict(eaters_dict)

    draw_graph(eaters_df["Order"], "Order", const.order_new_eater_graph)
    draw_graph(eaters_df["ABS"].astype("int64"), "ABS", const.abs_new_eater_graph)
    draw_graph(eaters_df["Sales"].apply(lambda x: round(x)), "Sales", const.sales_new_eater_graph)

    final_eaters_dict[const.dict_eaters_data] = eaters_raw_data
    final_eaters_dict[const.dict_uber_one_data] = uber_one_raw
    final_eaters_dict[const.dict_eaters_table] = eaters_df

    print(const.eaters_complete)

    return final_eaters_dict

def draw_graph(df, title: str, save_file_path: str):
    plt.clf()
    plt.ticklabel_format(style='plain')
    ax = df.plot(kind='bar', title=title,ylim=(0 ,max(df) + min(df)/2), color="#ff9900",figsize=(7,5), width=0.8, label=title)
    ax.set_xticklabels(eaters_df["Eaters"].tolist(), rotation=1)
    ax.set_ylabel(title)
    ax.minorticks_on()
    ax.bar_label(ax.containers[0], fmt = '%d')
    figure = ax.get_figure()
    figure.savefig(save_file_path)
