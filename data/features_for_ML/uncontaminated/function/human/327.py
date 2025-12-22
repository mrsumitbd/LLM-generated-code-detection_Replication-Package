import asyncio
import click
from salmon.common import handle_scrape_errors, make_searchstrs, re_strip
from salmon.search import SEARCHSOURCES, run_metasearch
from salmon.tagger.combine import combine_metadatas
from salmon.tagger.sources import METASOURCES
from salmon.tagger.sources.base import generate_artists

def _select_choice(choices, rls_data):
    source_url = None
    """
    Allow the user to select a metadata choice. Then, if the metadata came from a scraper,
    run the scrape(s) and return combined metadata.
    """
    # Initialize rls_data if needed
    rls_data = rls_data or {}
    if "urls" not in rls_data:
        rls_data["urls"] = []

    while True:
        if choices:
            res = click.prompt(
                click.style(
                    "\nWhich metadata results would you like to use? Other "
                    'options: paste URLs, [m]anual, [a], prefix choice or URL with "*" to indicate source (WEB)',
                    fg="magenta",
                ),
                type=click.STRING,
            )
        else:
            res = click.prompt(
                click.style(
                    "\nNo metadata results were found. Options: paste URLs, "
                    '[m]anual, [a]bort, prefix URL with "*" to indicate source (WEB)',
                    fg="magenta",
                ),
                type=click.STRING,
            )

        if res.lower().startswith("m"):
            return _get_manual_metadata(rls_data), None
        elif res.lower().startswith("a"):
            raise click.Abort

        sources, tasks = [], []
        for r in res.split():
            # Handle starred items first
            stripped = r[1:] if r.startswith("*") else r

            # Handle URLs (both starred and unstarred)
            if stripped.lower().startswith("http"):
                # Add any URL to rls_data urls if not already there
                if stripped not in rls_data["urls"]:
                    rls_data["urls"].append(stripped)

                # Set source_url if this is a starred URL
                if r.startswith("*"):
                    source_url = stripped

                # Try to scrape if it matches a metadata source
                for name, source in METASOURCES.items():
                    if source.Scraper.regex.match(stripped):
                        sources.append(name)
                        tasks.append(source.Scraper().scrape_release(stripped))
                        break
            # Handle numeric choices
            elif stripped.strip().isdigit() and int(stripped) in choices:
                scraper = METASOURCES[choices[int(stripped)][0]].Scraper()
                sources.append(choices[int(stripped)][0])
                tasks.append(handle_scrape_errors(scraper.scrape_release_from_id(choices[int(stripped)][1])))
                # Set source_url if this is a starred choice
                if r.startswith("*"):
                    source_url = SEARCHSOURCES[choices[int(stripped)][0]].Searcher.format_url(choices[int(stripped)][1])

        if not tasks:
            # Go to manual mode only if we have any URLs
            if rls_data["urls"]:
                meta = _get_manual_metadata(rls_data)
                meta["urls"] = meta.get("urls", [])
                # If we have a source_url (from a starred URL), make sure it's included
                if source_url and source_url not in meta["urls"]:
                    meta["urls"].append(source_url)
                return meta, source_url
            continue

        metadatas = loop.run_until_complete(asyncio.gather(*tasks))
        meta = combine_metadatas(
            *((s, m) for s, m in zip(sources, metadatas, strict=False) if m), base=rls_data, source_url=source_url
        )
        meta = clean_metadata(meta)
        meta["artists"], meta["tracks"] = generate_artists(meta["tracks"])
        return meta, source_url