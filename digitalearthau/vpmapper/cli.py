from pathlib import Path

import click

from datacube import Datacube
from digitalearthau.vpmapper.worker import D4


@click.group()
def cli():
    pass


@cli()
@click.option('environment')
@click.argument('config_file')
def run_many(config_file, environment=None):
    # Load Configuration file
    d4 = D4(config_file=config_file, dc_env=environment)

    tasks = d4.generate_tasks()

    d4.execute_with_dask(tasks)


@cli()
@click.argument('config_file')
@click.argument('input_dataset')
@click.option('environment')
def run_one(config_file, input_dataset, environment=None):
    d4 = D4(config_file=config_file, dc_env=environment)

    input_uri = Path(input_dataset).as_uri()
    dc = Datacube(env=environment)
    ds = dc.index.datasets.get_datasets_for_location(input_uri)

    task = d4.generate_task(ds)
    d4.execute_task(task)


if __name__ == '__main__':
    cli()
