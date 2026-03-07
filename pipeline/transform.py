import luigi
import logging
import pandas as pd
import time
import sqlalchemy
from datetime import datetime
# from pipeline.extract import Extract
# from pipeline.load import Load
# from pipeline.utils.db_conn import db_connection
# from pipeline.utils.read_sql import read_sql_file
from utils.db_conn import db_connection
from utils.read_sql import read_sql_file
from extract import Extract
from load import Load
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define DIR
DIR_ROOT_PROJECT = os.getenv("DIR_ROOT_PROJECT")
DIR_TEMP_LOG = os.getenv("DIR_TEMP_LOG")
DIR_TEMP_DATA = os.getenv("DIR_TEMP_DATA")
DIR_TRANSFORM_QUERY = os.getenv("DIR_TRANSFORM_QUERY")
DIR_LOG = os.getenv("DIR_LOG")

class Transform(luigi.Task):
    
    def requires(self):
        return Load()
    
    def run(self):
         
        # Configure logging
        logging.basicConfig(filename = f'{DIR_TEMP_LOG}/logs.log', 
                            level = logging.INFO, 
                            format = '%(asctime)s - %(levelname)s - %(message)s')
        
        #----------------------------------------------------------------------------------------------------------------------------------------
        # Establish connections to DWH
        try:
            _, dwh_engine = db_connection()
            logging.info(f"Connect to DWH - SUCCESS")
            
        except Exception:
            logging.info(f"Connect to DWH - FAILED")
            raise Exception("Failed to connect to Data Warehouse")
        
        #----------------------------------------------------------------------------------------------------------------------------------------
        # Read query to be executed
        try:
            
            # Read transform query to final schema
            dim_product_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/dim_products.sql'
            )

            dim_order_status_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/dim_order_status.sql'
            )
 
            dim_reviews_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/dim_reviews.sql'
            )

            dim_word_values_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/dim_word_values.sql'
            )

            dim_word_values_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/dim_word_values.sql'
            )

            fct_item_ordered_per_day_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/fct_item_ordered_per_day.sql'
            )

            fct_item_ordered_per_month_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/fct_item_ordered_per_month.sql'
            )

            fct_order_status_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/fct_order_status.sql'
            )

            fct_review_rating_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/fct_review_rating.sql'
            )

            fct_review_value_query = read_sql_file(
                file_path = f'{DIR_TRANSFORM_QUERY}/fct_review_value.sql'
            )           

            logging.info("Read Transform Query - SUCCESS")
            
        except Exception:
            logging.error("Read Transform Query - FAILED")
            raise Exception("Failed to read Transform Query")        
        
        #----------------------------------------------------------------------------------------------------------------------------------------
        # Record start time for transform tables
        start_time = time.time()
        logging.info("==================================STARTING TRANSFROM DATA=======================================")  
               
        # Transform to dimensions tables
        try:
            # Create session
            Session = sessionmaker(bind = dwh_engine)
            session = Session()
            
            # populate product_dimension
            query = sqlalchemy.text(dim_product_query)
            session.execute(query)
            logging.info("Transform to 'final.dim_product' - SUCCESS")
            
            # populate order status dimension
            query = sqlalchemy.text(dim_order_status_query)
            session.execute(query)
            logging.info("Transform to 'final.dim_order_status' - SUCCESS")

            # populate review dimension
            query = sqlalchemy.text(dim_reviews_query)
            session.execute(query)
            logging.info("Transform to 'final.dim_reviews' - SUCCESS")            

            # populate word value dimension
            query = sqlalchemy.text(dim_word_values_query)
            session.execute(query)
            logging.info("Transform to 'final.dim_word_values' - SUCCESS")  

            # populate fct item ordered per day
            query = sqlalchemy.text(fct_item_ordered_per_day_query)
            session.execute(query)
            logging.info("Transform to 'final.fct_item_ordered_per_day' - SUCCESS")              

            # populate fct item ordered per month
            query = sqlalchemy.text(fct_item_ordered_per_month_query)
            session.execute(query)
            logging.info("Transform to 'final.fct_item_ordered_per_month' - SUCCESS")

            # populate fct order status
            query = sqlalchemy.text(fct_order_status_query)
            session.execute(query)
            logging.info("Transform to 'final.fct_order_status' - SUCCESS")            

            # populate fct review rating
            query = sqlalchemy.text(fct_review_rating_query)
            session.execute(query)
            logging.info("Transform to 'final.fct_review_rating' - SUCCESS")       

            # populate fct review value
            query = sqlalchemy.text(fct_review_value_query)
            session.execute(query)
            logging.info("Transform to 'final.fct_review_value' - SUCCESS") 

            # Commit transaction
            session.commit()
            
            # Close session
            session.close()

            logging.info(f"Transform to All Dimensions and Fact Tables - SUCCESS")
            
            # Record end time for loading tables
            end_time = time.time()  
            execution_time = end_time - start_time  # Calculate execution time
            
            # Get summary
            summary_data = {
                'timestamp': [datetime.now()],
                'task': ['Transform'],
                'status' : ['Success'],
                'execution_time': [execution_time]
            }

            # Get summary dataframes
            summary = pd.DataFrame(summary_data)
            
            # Write Summary to CSV
            summary.to_csv(f"{DIR_TEMP_DATA}/transform-summary.csv", index = False)
            
        except Exception:
            logging.error(f"Transform to All Dimensions and Fact Tables - FAILED")
        
            # Get summary
            summary_data = {
                'timestamp': [datetime.now()],
                'task': ['Transform'],
                'status' : ['Failed'],
                'execution_time': [0]
            }

            # Get summary dataframes
            summary = pd.DataFrame(summary_data)
            
            # Write Summary to CSV
            summary.to_csv(f"{DIR_TEMP_DATA}/transform-summary.csv", index = False)
            
            logging.error("Transform Tables - FAILED")
            raise Exception('Failed Transforming Tables')   
        
        logging.info("==================================ENDING TRANSFROM DATA=======================================") 

    #----------------------------------------------------------------------------------------------------------------------------------------
    def output(self):
        return [luigi.LocalTarget(f'{DIR_TEMP_LOG}/logs.log'),
                luigi.LocalTarget(f'{DIR_TEMP_DATA}/transform-summary.csv')]
    
if __name__ == '__main__':
    luigi.build([Transform()])    
        