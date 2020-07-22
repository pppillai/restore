import click
import boto3

@click.command(help="restore objects")
@click.option("-p", "--profile", required=True, type=str)
@click.option("-b", "--bucket", required=True, type=str)
@click.option("-k", "--prefix", required=True, type=str)
def cli(profile, bucket, prefix):
    try:
        session = boto3.session.Session(profile_name=profile)
    
        client = session.client('s3')

        list_of_objects = client.list_object_versions(Bucket=bucket, Prefix=prefix)

        while True:
            
            for item in list_of_objects['DeleteMarkers']:
                if item['IsLatest']:
                    client.delete_object(Bucket=bucket, Key=item['Key'], VersionId=item['VersionId'])

            if not list_of_objects['IsTruncated']:
                break
            next_ = list_of_objects['NextKeyMarker']
            list_of_objects = client.list_object_versions(Bucket=bucket, Prefix=prefix, KeyMarker=next_)
    except Exception as e:
        if isinstance(e, KeyError):
            click.secho("No more Deleted files found...", fg=green, bold=True)
            pass
        else:
            click.secho(e, fg="red", bold=True)
    click.secho("Done", fg="green", bold=True)
    