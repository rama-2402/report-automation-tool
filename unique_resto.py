import pandas as pd
import constants as const
import clipboard

ad_metrics = pd.read_csv(const.ad_metrics_data, sep="\t")

def get_unique_restos(ad_data: pd.DataFrame):
    unique_uuid = ad_data["restaurant_uuid"].unique()
    print(const.unique_restro_status)
    print(f"{const.unique_restro_output_status}{len(unique_uuid)}")
    formatted_uuid = ""
    for id in unique_uuid:
        new_str = f"'{id}',"
        formatted_uuid = f"{formatted_uuid}{new_str}"
    print(f"Copied {len(unique_uuid)} unique UUIDs")
    clipboard.copy(formatted_uuid[:-1])

if __name__ == "__main__":
    get_unique_restos(ad_data= ad_metrics)
