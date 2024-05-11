import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition

class ApplyTransformation(beam.DoFn):
    def __init__(self, schema):
        self.schema = schema

    def process(self, element):
        data = element.split(',')
        result = {}
        for idx, field in enumerate(self.schema):
            if field['type'] == int:
                result[field['name']] = int(data[idx].strip()) if data[idx].strip().isdigit() else None
            elif field['type'] == bool:
                result[field['name']] = (data[idx].strip().lower() == 'true')
            else:
                result[field['name']] = data[idx].strip()
        yield result

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
            {'name': 'team_id', 'type': int},
            {'name': 'country', 'type': str},
            {'name': 'venue_city', 'type': str},
            {'name': 'name', 'type': str},
            {'name': 'founded', 'type': int},
            {'name': 'venue_name', 'type': str}
        ],
        'scorers_information_2024': [
            {'name': 'firstname', 'type': str},
            {'name': 'lastname', 'type': str},
            {'name': 'age', 'type': int},
            {'name': 'nationality', 'type': str},
            {'name': 'height', 'type': str},
            {'name': 'weight', 'type': str},
            {'name': 'injured', 'type': bool},
            {'name': 'team', 'type': str}
        ],
        'scorers_statistics_2024': [
            {'name': 'firstname', 'type': str},
            {'name': 'lastname', 'type': str},
            {'name': 'goals', 'type': int},
            {'name': 'assists', 'type': int},
            {'name': 'conceded', 'type': int},
            {'name': 'penalty_scored', 'type': int},
            {'name': 'penalty_missed', 'type': int},
            {'name': 'total_passes', 'type': int},
            {'name': 'key_passes', 'type': int},
            {'name': 'total_duels', 'type': int},
            {'name': 'duels_won', 'type': int}
        ]
    }

    with beam.Pipeline(options=pipeline_options) as p:
        for file_key, schema in schemas.items():
            file_path = f'gs://chilean_football_bucket/{file_key}.csv'
            # Read data
            lines = p | f'Read {file_key}' >> ReadFromText(file_path)
            # Apply transformations
            transformed = lines | f'Transform {file_key}' >> beam.ParDo(ApplyTransformation(schema))
            # Write to BigQuery
            transformed | f'Write {file_key} to BigQuery' >> WriteToBigQuery(
                f'chilean_premier_league_2024.{file_key}',
                schema=','.join(f'{field["name"]}:{field["type"].__name__.upper()}' for field in schema),
                create_disposition=BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=BigQueryDisposition.WRITE_APPEND
            )

if __name__ == '__main__':
    run()
