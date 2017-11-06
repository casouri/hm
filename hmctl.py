#! venv/bin/python3
import click


@click.group()
def ctl():
    pass


@click.command()
@click.argument('obj')
@click.argument('status')
def switch(obj, status):
    '''switch something on or off.

    Args:
        obj (int): the id of the object
        status (str): "on" or "off".
    '''
    click.echo('{} is turned {}'.format(obj, status))


ctl.add_command(switch)

if __name__ == '__main__':
    ctl()
