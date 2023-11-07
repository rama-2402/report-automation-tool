import pandas as pd
import constants as const
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import save_file as op
from textwrap import wrap


final_top_cities = pd.DataFrame()
final_top_restos = pd.DataFrame()

top_performers_dict = dict()

def top_performers():
    print(const.init_top_performers)
    perf_cities = pd.read_csv(const.top_performers_cities_data, sep="\t")
    perf_restos = pd.read_csv(const.top_performers_restaurants_data, sep="\t")

    perf_cities = const.check_df_for_errors(perf_cities, ["CVR", "ROAS"])
    perf_restos = const.check_df_for_errors(perf_restos, ["CVR", "ROAS"])

    generate_resto_graph(perf_restos)
    generate_cities_graph(perf_cities)

    top_performers_dict[const.dict_top_cities_data] = perf_cities
    top_performers_dict[const.dict_top_restos_data] = perf_restos

    print(const.top_perf_complete)

    return top_performers_dict

def generate_cities_graph(cities: pd.DataFrame):
    plt.clf()
    cities["ROAS"] = cities["ROAS"].round(2)
    cities["CVR"] = cities["CVR"]*100
    ax_c = cities['ROAS'].plot(kind='bar', title=const.top_perf_cities_graph_title, color="#93c47d",figsize=(9,7), width=0.8,ylim=(0 ,max(cities["ROAS"].tolist()) + 10), label="ROAS")
    ax2_c = cities['CVR'].plot(kind='line', secondary_y=True,figsize=(9,7), ylim=(0 ,max(cities["CVR"].tolist()) + 10 ), linewidth=1, label="CVR", linestyle='-.', color='black')
    labels = [ '\n'.join(wrap(l, 8)) for l in cities['city_name']]
    ax_c.set_xticklabels(labels)
    ax2_c.yaxis.set_major_formatter(mtick.PercentFormatter())

    for p in ax_c.containers:
        ax_c.bar_label(p, label_type="center",color='w', fontweight='bold')

    count = 0
    for p in cities["CVR"].tolist():
        ax2_c.text(count, p+0.01, f'{str(p)[0:5]}%' ,
        color='k', fontsize=10, visible=True,horizontalalignment='left',
        verticalalignment='bottom')
        count = count+1

    ax_c.set_label("ROAS")
    ax2_c.set_label("CVR")

    h1, l1 = ax_c.get_legend_handles_labels()
    h2, l2 = ax2_c.get_legend_handles_labels()
    ax_c.legend(h1+h2, l1+l2)

    figure = ax_c.get_figure()
    figure.savefig(const.top_cities_graph)

    # top_performers_dict[const.dict_top_cities_data] = cities

def generate_resto_graph(restos: pd.DataFrame):
    plt.clf()
    restos["ROAS"] = restos["ROAS"].round(2)
    restos["CVR"] = restos["CVR"]*100
    ax = restos['ROAS'].plot(kind='bar', title=const.top_perf_cities_graph_title, color="#93c47d",figsize=(10,8), width=0.8,ylim=(0 ,max(restos["ROAS"].tolist()) + 10 ), label="ROAS")
    ax2 = restos['CVR'].plot(kind='line',secondary_y=True,figsize=(10,8), ylim=(0 ,max(restos["CVR"].tolist()) + 10 ), linewidth=1, linestyle='-.', color='black', label="CVR")
    labels = [ '\n'.join(wrap(l, 8)) for l in restos['restaurant_name']]
    ax.set_xticklabels(labels)

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())

    for p in ax.containers:
        ax.bar_label(p, label_type="center",color='w', fontweight='bold')

    count = 0
    for p in restos["CVR"].tolist():
        ax2.text(count, p+0.01, f'{str(p)[0:5]}%' ,
        color='k', fontsize=10, visible=True,horizontalalignment='left',
        verticalalignment='bottom')
        count = count+1

    ax.set_label("ROAS")
    ax2.set_label("CVR")

    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1+h2, l1+l2)

    fig = ax.get_figure()
    fig.savefig(const.top_restos_graph)

    # top_performers_dict[const.dict_top_restos_data] = restos


# if __name__ == "__main__":
#     top_performers()