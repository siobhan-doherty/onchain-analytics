import os
import pandas as pd
import logging
import duckdb
from dune_client.client import DuneClient
from dune_client.query import QueryBase

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

DUNE_API_KEY = os.getenv("DUNE_API_KEY")
DUNE_QUERY_ID = int(os.environ.get("DUNE_QUERY_ID", "7494336"))
DB_PATH = "./data/dex_analytics.duckdb"
TABLE_NAME = "raw_dex_trades"


def get_last_run_timestamp(conn):
    """Get latest block_time from existing data for incremental logging only."""
    try:
        result = conn.execute(f"SELECT MAX(block_time) FROM {TABLE_NAME}").fetchone()
        if result and result[0]:
            return result[0]
    except Exception:
        logger.info("No existing table, will perform full fetch.")
    return None


def fetch_data():
    """Fetch data from Dune API using valid performance tier."""
    logger.info("Executing query on Dune API...")
    dune = DuneClient(DUNE_API_KEY)
    query = QueryBase(query_id = DUNE_QUERY_ID)    

    try:
        df = dune.run_query_dataframe(query, performance = "small")
        logger.info(f"Successfully fetched {len(df)} rows")
        return df

    except Exception as e:
        logger.error(f"Dune API query failed: {e}")
        raise


def load_to_duckdb(df, conn, table_name):
    """Load or merge DataFrame into DuckDB, deduplicating by tx_hash + evt_index."""
    if df.empty:
        logger.info("No data to load.")
        return
    
    conn.register("new_data", df)
    table_exists = conn.execute(f"""
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_name = '{table_name}'
    """).fetchone()[0] > 0

    if not table_exists:
        conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM new_data")
        logger.info(f"Created new table {table_name} with {len(df)} rows.")
        conn.execute("DROP VIEW new_data")
        return

    # use tx_hash + evt_index as unique key
    # if evt_index missing, fallback to tx_hash + block_time
    try:
        # first attempt with evt_index
        conn.execute(f"""
            INSERT INTO {table_name}
            SELECT n.* FROM new_data n
            LEFT JOIN {table_name} t 
                ON n.tx_hash = t.tx_hash AND n.evt_index = t.evt_index
            WHERE t.tx_hash IS NULL
        """)
        inserted_count = conn.execute("""
            SELECT COUNT(*) FROM new_data n
            LEFT JOIN raw_dex_trades t 
                ON n.tx_hash = t.tx_hash AND n.evt_index = t.evt_index
            WHERE t.tx_hash IS NULL
        """).fetchone()[0]
    except Exception:
        # fallback if evt_index column does not exist
        logger.warning("evt_index column missing, falling back to tx_hash + block_time")
        conn.execute(f"""
            INSERT INTO {table_name}
            SELECT n.* FROM new_data n
            LEFT JOIN {table_name} t 
                ON n.tx_hash = t.tx_hash AND n.block_time = t.block_time
            WHERE t.tx_hash IS NULL
        """)
        inserted_count = conn.execute("""
            SELECT COUNT(*) FROM new_data n
            LEFT JOIN raw_dex_trades t 
                ON n.tx_hash = t.tx_hash AND n.block_time = t.block_time
            WHERE t.tx_hash IS NULL
        """).fetchone()[0]

    logger.info(f"Merged {len(df)} rows into {table_name} (inserted {inserted_count} new rows, skipped {len(df)-inserted_count} duplicates).")
    conn.execute("DROP VIEW new_data")


def main():
    conn = duckdb.connect(DB_PATH)
    last_ts = get_last_run_timestamp(conn)
    if last_ts:
        logger.info(f"Existing data found. Latest block_time: {last_ts}. Fetching all data (deduplication will handle incrementality).")
    else:
        logger.info("No existing data. Fetching full dataset.")

    df = fetch_data()
    load_to_duckdb(df, conn, TABLE_NAME)
    conn.close()


if __name__ == "__main__":
    main()
