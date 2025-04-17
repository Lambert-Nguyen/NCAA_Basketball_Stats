import os
from google.cloud import bigquery
from google.oauth2 import service_account

class ConfigureBigQuery:
    """
    Configures and executes BigQuery queries, returning results as Pydantic models.

    This class provides a generic way to execute BigQuery queries and automatically 
    convert the results into instances of a specified Pydantic model. This promotes 
    code reusability and simplifies data handling.

    Attributes:
        project_id (str, optional): The Google Cloud project ID. If None, the 
            project ID is inferred from the environment.
    """

    def __init__(self, project_id: str = None, credential_file_path : str = None):
        """
        Initializes the ConfigureBigQuery class.

        Args:
            project_id (str, optional): The Google Cloud project ID. 
                Defaults to None.
        """
        self.project_id = project_id
        self.credentials_path = credential_file_path
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_path)
        self.client = bigquery.Client(credentials=self.credentials, project=self.project_id)


    # TODO: fix this method to return generic response model 
    def execute_query(self, query: str, job_config: bigquery.QueryJobConfig = None):
        """
        Executes a BigQuery query and converts the results into a list of Pydantic models.

        Args:
            query (str): The SQL query to execute.
            job_config (bigquery.QueryJobConfig, optional): Configuration for the 
                query job. Defaults to None.

        Returns:
            Currently None
            # List[BaseModel]: A list of Pydantic model instances representing the query results.

        # doesn't work right now 
        Raises:
            ValueError: If a row from BigQuery cannot be converted to the specified response model.
        """
        query_job = self.client.query(query, job_config=job_config)
        results = query_job.result()
        '''
        resp = []
        for row in results:
            try:
                resp.append(response_model(**dict(row)))
            except Exception as e:
                raise ValueError(f"Failed to convert row to {response_model.__name__}: {e}")
        '''
        return results
