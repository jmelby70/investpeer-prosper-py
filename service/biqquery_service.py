import logging

from google.cloud import bigquery
from google.api_core.exceptions import NotFound


class BigQueryService:
    def __init__(self):
        self.client = bigquery.Client()
        self.logger = logging.getLogger(__name__)

    def get_notes_table_id(self, prosper_config):
        table_id = f"{prosper_config.project_id}.{prosper_config.dataset_name}.{prosper_config.notes_table_name}"
        return table_id

    def create_notes_table(self, prosper_config):
        """
        Create the p2p_loans table in BigQuery if it does not already exist.
        The table has two columns: loan_note_id (STRING) and note_data (JSON).
        """
        table_id = self.get_notes_table_id(prosper_config)

        try:
            # Get the table object to check for its existence
            self.client.get_table(table_id)
            print(f"Table {table_id} already exists.")

        except NotFound:
            # If the table is not found, define the schema and create it
            print(f"Table {table_id} not found, creating it now.")

            schema = [
                bigquery.SchemaField("loan_note_id", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("note_data", "JSON", mode="REQUIRED")
            ]

            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")

    def insert_notes(self, prosper_config, notes):
        """
        Insert a list of notes into the BigQuery table.
        Each note is expected to be a dictionary with 'loan_note_id' as a json field.
        The 'note_data' field will store the entire note as JSON.
        """
        table_id = self.get_notes_table_id(prosper_config)
        rows_to_insert = []
        for note in notes:
            self.logger.debug(f"Processing note: {note}")
            if not isinstance(note, dict):
                self.logger.error(f"Invalid note type: {type(note)}. Skipping: {note}")
                continue
            rows_to_insert.append({
                "loan_note_id": note.get("loan_note_id"),
                "note_data": note
            })
        errors = self.client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            self.logger.error(f"Encountered errors while inserting rows: {errors}")
        else:
            self.logger.info(f"Inserted {len(rows_to_insert)} rows into {table_id}.")
