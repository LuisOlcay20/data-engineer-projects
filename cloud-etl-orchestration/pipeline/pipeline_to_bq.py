import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition

def run(argv=None):
    pipeline_options = PipelineOptions(
        flags=argv,
        runner='DataflowRunner',
        project='cloud-etl-orchestration',
        job_name='dataflow-to-bigquery',
        temp_location='gs://chilean_football_bucket/temp',
        region='southamerica-east1'
    )

    schemas = {
        'chilean_teams_2024': [
            {'name': 'team_id', 'type': 'INTEGER'},
            {'name': 'country', 'type': 'STRING'},
            {'name': 'venue_city', 'type': 'STRING'},
            {'name': 'name', 'type': 'STRING'},
            {'name': 'founded', 'type': 'INTEGER'},
            {'name': 'venue_name', 'type': 'STRING'}
        ],
        'scorers_information_2024': [
            {'name': 'firstname', 'type': 'STRING'},
            {'name': 'lastname', 'type': 'STRING'},
            {'name': 'age', 'type': 'INTEGER'},
            {'name': 'nationality', 'type': 'STRING'},
            {'name': 'height', 'type': 'STRING'},
            {'name': 'weight', 'type': 'STRING'},
            {'name': 'injured', 'type': 'BOOLEAN'},
            {'name': 'team', 'type': 'STRING'}
        ],
        'scorers_statistics_2024': [
            {'name': 'firstname', 'type': 'STRING'},
            {'name': 'lastname', 'type': 'STRING'},
            {'name': 'goals', 'type': 'INTEGER'},
            {'name': 'assists', 'type': 'INTEGER'},
            {'name': 'conceded', 'type': 'INTEGER'},
            {'name': 'penalty_scored', 'type': 'INTEGER'},
            {'name': 'penalty_missed', 'type': 'INTEGER'},
            {'name': 'total_passes', 'type': 'INTEGER'},
            {'name': 'key_passes', 'type': 'INTEGER'},
            {'name': 'total_duels', 'type': 'INTEGER'},
            {'name': 'duels_won', 'type': 'INTEGER'}
        ]
    }

    with beam.Pipeline(options=pipeline_options) as p:
        for file_key, schema in schemas.items():
            file_path = f'gs://chilean_football_bucket/{file_key}.csv'
            table_schema = ','.join(f'{field["name"]}:{field["type"]}' for field in schema)
            # Read data
            lines = p | f'Read {file_key}' >> ReadFromText(file_path)
            # Write to BigQuery
            lines | f'Write {file_key} to BigQuery' >> WriteToBigQuery(
                f'chilean_premier_league_2024.{file_key}',
                schema=table_schema,
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=BigQueryDisposition.WRITE_APPEND
            )

if __name__ == '__main__':
    run()
