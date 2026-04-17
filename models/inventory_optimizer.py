import pandas as pd


def calculate_inventory_recommendation(predicted_demand: float,
                                       demand_std: float = 5,
                                       service_level_factor: float = 1.65):
    """
    Calculate recommended inventory level using safety stock formula.
    """

    safety_stock = demand_std * service_level_factor

    recommended_stock = predicted_demand + safety_stock

    inventory_gap = recommended_stock - predicted_demand

    restock_alert = predicted_demand > recommended_stock * 0.8

    return {
        "predicted_demand": float(predicted_demand),
        "safety_stock": float(safety_stock),
        "recommended_stock": float(recommended_stock),
        "inventory_gap": float(inventory_gap),
        "restock_alert": bool(restock_alert)
    }
