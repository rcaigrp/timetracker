#!/usr/bin/env python3
"""
CLI interface for JiraSync-Time-CLI tool.
"""

import click
from .tracker import TimeTracker
from .sync import JiraSync
from .storage import TimeStorage


@click.group()
@cli.command()
def cli():
    """JiraSync-Time-CLI: Track time spent on Jira issues."""
    pass


@cli.command()
click.argument('issue_key')
def start(issue_key):
    """Start tracking time for a Jira issue."""
    tracker = TimeTracker()
    try:
        tracker.start_tracking(issue_key)
        click.echo(f"Started tracking time for issue {issue_key}")
    except Exception as e:
        click.echo(f"Error starting tracking: {e}", err=True)


@cli.command()
def stop():
    """Stop current time tracking."""
    tracker = TimeTracker()
    try:
        tracker.stop_tracking()
        click.echo("Stopped tracking time")
    except Exception as e:
        click.echo(f"Error stopping tracking: {e}", err=True)


@cli.command()
def log():
    """Show local time logs."""
    storage = TimeStorage()
    try:
        logs = storage.get_logs()
        if not logs:
            click.echo("No time logs found.")
        else:
            for log in logs:
                click.echo(f"{log[0]}: {log[1]} - {log[2]} ({log[3]})")
    except Exception as e:
        click.echo(f"Error retrieving logs: {e}", err=True)


@cli.command()
def sync():
    """Sync time logs to Jira."""
    storage = TimeStorage()
    syncer = JiraSync()
    try:
        logs = storage.get_logs()
        if not logs:
            click.echo("No logs to sync.")
            return
        
        success_count = 0
        for log in logs:
            # log format: (id, issue_key, start_time, end_time, source)
            try:
                syncer.sync_log(log[1], log[2], log[3])
                success_count += 1
            except Exception as e:
                click.echo(f"Failed to sync log {log[0]}: {e}", err=True)
        
        click.echo(f"Successfully synced {success_count} out of {len(logs)} logs.")
    except Exception as e:
        click.echo(f"Error syncing logs: {e}", err=True)


if __name__ == '__main__':
    cli()
