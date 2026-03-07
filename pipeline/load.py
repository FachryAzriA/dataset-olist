import luigi
import logging
import pandas as pd
import time
import sqlalchemy
from datetime import datetime
from extract import Extract
from utils.db_conn import db_connection
from utils.read_sql import read_sql_file
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Define DIR
DIR_ROOT_PROJECT = os.getenv("DIR_ROOT_PROJECT")
DIR_TEMP_LOG = os.getenv("DIR_TEMP_LOG")
DIR_TEMP_DATA = os.getenv("DIR_TEMP_DATA")
DIR_LOAD_QUERY = os.getenv("DIR_LOAD_QUERY")
DIR_LOG = os.getenv("DIR_LOG")

class Load(luigi.Task):   
    
    def requires(self):
        return Extract()
    
    def run(self):
        
        # Configure logging
        logging.basicConfig(filename = f'{DIR_TEMP_LOG}/logs.log', 
                            level = logging.INFO, 
                            format = '%(asctime)s - %(levelname)s - %(message)s')
        
        # Read query to be executed
        try:
            # Read query to truncate stg schema in dwh
            truncate_query = read_sql_file(
                file_path = f'{DIR_LOAD_QUERY}/staging-truncate_tables.sql'
                )        
            
        except Exception:
            logging.error("Read Load Query - FAILED")
            raise Exception("Failed to read Load Query")
        
        #----------------------------------------------------------------------------------------------------------------------------------------
        # read csv file
        try:
            product_category_translation = pd.read_csv(self.input()[0].path)
            products = pd.read_csv(self.input()[1].path)
            orders = pd.read_csv(self.input()[2].path)
            order_items = pd.read_csv(self.input()[3].path)
            order_reviews = pd.read_csv(self.input()[4].path)
            
            logging.info(f"Read Extracted Data - SUCCESS")
            # logging.info(product_category_translation)
            
        except Exception:
            logging.error(f"Read Extracted Data  - FAILED")
            raise Exception("Failed to Read Extracted Data")
        
        #----------------------------------------------------------------------------------------------------------------------------------------
        # Establish connections to DWH
        try:
            _, dwh_engine = db_connection()
            logging.info(f"Connect to DWH - SUCCESS")
            
        except Exception:
            logging.info(f"Connect to DWH - FAILED")
            raise Exception("Failed to connect to Data Warehouse")        

        #----------------------------------------------------------------------------------------------------------------------------------------
        # Truncate all tables before load
        # This puropose to avoid errors because duplicate key value violates unique constraint
        try:            
            # Split the SQL queries if multiple queries are present
            truncate_query = truncate_query.split(';')

            # Remove newline characters and leading/trailing whitespaces
            truncate_query = [query.strip() for query in truncate_query if query.strip()]
            
            # Create session
            Session = sessionmaker(bind = dwh_engine)
            session = Session()

            # Execute each query
            for query in truncate_query:
                query = sqlalchemy.text(query)
                session.execute(query)
                
            session.commit()
            
            # Close session
            session.close()
            logging.info(f"Truncate staging Schema in DWH - SUCCESS")
        
        except Exception:
            logging.error(f"Truncate staging Schema in DWH - FAILED")        
            raise Exception("Failed to Truncate staging Schema in DWH")
        
        #----------------------------------------------------------------------------------------------------------------------------------------
        # Record start time for loading tables
        start_time = time.time()  
        logging.info("==================================STARTING LOAD DATA=======================================")
        # Load to tables
        try:
            
            try:
                # Load to stg schema
                # Load category tables    
                product_category_translation.to_sql('product_category_name_translation', 
                                                    con = dwh_engine, 
                                                    if_exists = 'append', 
                                                    index = False, 
                                                    schema = 'stg')

                products.to_sql('products', 
                                con = dwh_engine, 
                                if_exists = 'append', 
                                index = False, 
                                schema = 'stg')
                 
                orders.to_sql('orders', 
                              con = dwh_engine, 
                              if_exists = 'append', 
                              index = False, 
                              schema = 'stg')  
                
                order_items.to_sql('order_items', 
                                    con = dwh_engine, 
                                    if_exists = 'append', 
                                    index = False, 
                                    schema = 'stg')                              
                
                order_reviews.to_sql('order_reviews', 
                                     con = dwh_engine, 
                                     if_exists = 'append', 
                                     index = False, 
                                     schema = 'stg') 
                

                logging.info(f"LOAD All Tables To DWH - SUCCESS")
                
            except Exception:
                logging.error(f"LOAD All Tables To DWH - FAILED")
                raise Exception('Failed Load Tables To DWH {e}')
        
            # Record end time for loading tables
            end_time = time.time()  
            execution_time = end_time - start_time  # Calculate execution time
            
            # Get summary
            summary_data = {
                'timestamp': [datetime.now()],
                'task': ['Load'],
                'status' : ['Success'],
                'execution_time': [execution_time]
            }

            # Get summary dataframes
            summary = pd.DataFrame(summary_data)
            
            # Write Summary to CSV
            summary.to_csv(f"{DIR_TEMP_DATA}/load-summary.csv", index = False)
            
                        
        #----------------------------------------------------------------------------------------------------------------------------------------
        except Exception:
            # Get summary
            summary_data = {
                'timestamp': [datetime.now()],
                'task': ['Load'],
                'status' : ['Failed'],
                'execution_time': [0]
            }

            # Get summary dataframes
            summary = pd.DataFrame(summary_data)
            
            # Write Summary to CSV
            summary.to_csv(f"{DIR_TEMP_DATA}/load-summary.csv", index = False)
            
            logging.error("LOAD All Tables To DWH - FAILED")
            raise Exception('Failed Load Tables To DWH')   
        
        logging.info("==================================ENDING LOAD DATA=======================================")
           
    #----------------------------------------------------------------------------------------------------------------------------------------
    def output(self):
        return [luigi.LocalTarget(f'{DIR_TEMP_LOG}/logs.log'),
                luigi.LocalTarget(f'{DIR_TEMP_DATA}/load-summary.csv')]

if __name__ == '__main__':
    luigi.build([Load()])    
    