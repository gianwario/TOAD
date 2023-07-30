import requests
import os
import json
from auth import oauth2
from compute_community_pattern import compute_community_patterns
from io_module import input_handler, repository_manager, output_handler
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
    longevity_processor,
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
        metrics.dispersion = {}
        metrics.structure = {}
        metrics.engagement = {}
        metrics.formality = {}
        metrics.longevity = 0
        community.add_metrics(metrics)

        repo = repository_manager.download_repo(
            community.repo_owner, community.repo_name
        )

        community.data.all_commits = list(repo.iter_commits())

        if not retrieve_data_and_check_validity(community):
            console.print("[bold red]Invalid repository")
            raise SystemExit(0)
        console.print("[bold green]Repository is valid")

        retrieve_structure_data(community)
        structure = structure_processor.compute_structure_data(community)
        if structure:
            retrieve_miscellaneous_data(community)
            dispersion_processor.compute_distances(community)
            formality_processor.compute_formality_data(community)
            engagement_processor.compute_engagement_data(community)
            longevity_processor.compute_longevity_data(community)

        console.print(community.metrics)
        community_patterns = compute_community_patterns(community.metrics)
        print(community_patterns)
        output_handler.save_results(output_path, community, community_patterns)


if __name__ == "__main__":
    main()
