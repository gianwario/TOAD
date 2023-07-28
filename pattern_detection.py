import requests
import os
import json
from auth import oauth2
from io_module import input_handler, repository_manager
from data_retriever.data_retriever import (
    retrieve_data_and_check_validity,
    retrieve_structure_data,
    retrieve_miscellaneous_data,
)
from console import console
from community.data import Data
from community.metrics import Metrics
from data_processor import (
    dispersion_processor,
    structure_processor,
    formality_processor,
    engagement_processor,
)


def main():
    console.rule("Input information")
    input_path, output_path, start_date, end_date = input_handler.get_input_files()
    communities = input_handler.get_input_communities(input_path)

    console.rule("GitHub Authentication")
    pat = oauth2.get_access_token()

    for community in communities:
        console.rule(
            "Community " + community.repo_name + " from " + community.repo_owner
        )

        data = Data()
        data.start_date = start_date
        data.end_date = end_date
        community.add_data(data)

        metrics = Metrics()
        community.add_metrics(metrics)

        repo = repository_manager.download_repo(
            community.repo_owner, community.repo_name
        )

        community.data.all_commits = list(repo.iter_commits())

        if not retrieve_data_and_check_validity(community):
            console.print("[bold red]Invalid repository")
            raise SystemExit(0)
        console.print("[bold green]Repository is valid")
        """
        TODO
        if the community exhibits a structure (community_structure = true)
            # dispersion_processor.compute_distances(community)
            retrieve data for formality, cohesion, engagement, longevity
            compute remaining characteristics
            compute patterns
        """
        retrieve_structure_data(community)

        # structure_processor.compute_structure_data(community)
        retrieve_miscellaneous_data(community)
        # formality_processor.compute_formality_data(community)
        engagement_processor.compute_engagement_data(community)


if __name__ == "__main__":
    main()
