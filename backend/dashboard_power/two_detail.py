from backend.db_connection import connect_aep_DB
import random

def fetch_Sum_Cust(smcode):
    total_customers = random.randint(100, 300)

    return total_customers

def fetch_Sum_Active(smcode):
    total_Cust = 123

    return int(total_Cust)

def get_topic_data_sale(smcode):
    simulated_result = [
        {"End_Customer_Type": "Airline", "total_customers_no_sales": 50},
        {"End_Customer_Type": "Restaurant", "total_customers_no_sales": 120},
        {"End_Customer_Type": "Supermarket", "total_customers_no_sales": 75},
        {"End_Customer_Type": "Hotel", "total_customers_no_sales": 30},
        {"End_Customer_Type": "Bakery Shop", "total_customers_no_sales": 40},
        {"End_Customer_Type": "Factory", "total_customers_no_sales": 10}
    ]

    return simulated_result