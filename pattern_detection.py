import requests
import os
import json
from datetime import datetime, date, timedelta
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
    input_path, output_path = input_handler.get_input_files()
    communities = input_handler.get_input_communities(input_path)

    console.rule("GitHub Authentication")
    pat = oauth2.get_access_token()

    for community in communities:
        patterns = None
        while patterns is None:
            console.rule(
                "Community " + community.repo_name + " from " + community.repo_owner
            )

            repo = repository_manager.download_repo(
                community.repo_owner, community.repo_name
            )

            community.data.all_commits = list(repo.iter_commits())

            if not retrieve_data_and_check_validity(community):
                console.print("[bold red]Invalid repository")
            else:
                console.print("[bold green]Repository is valid")

                console.log("Retrieving data to compute community structure")
                retrieve_structure_data(community)
                console.log("[bold yellow] Computing COMMUNITY STRUCTURE")
                structure = structure_processor.compute_structure_data(community)
                if structure:
                    console.log(
                        "Retrieving data to compute community geodispersion, formality, engagement and longevity"
                    )
                    retrieve_miscellaneous_data(community)
                    console.log("[bold yellow] Computing COMMUNITY GEODISPERSION")
                    dispersion_processor.compute_distances(community)
                    console.log("[bold yellow] Computing COMMUNITY FORMALITY")
                    formality_processor.compute_formality_data(community)
                    console.log("[bold yellow] Computing COMMUNITY ENGAGEMENT")
                    engagement_processor.compute_engagement_data(community)
                    console.log("[bold yellow] Computing COMMUNITY LONGEVITY")
                    longevity_processor.compute_longevity_data(community)

                    console.print(community.metrics)
                    console.log("[bold purple] Computing COMMUNITY PATTERNS")
                    (
                        structure,
                        dispersion,
                        formality,
                        longevity,
                        engagement,
                        community_patterns,
                    ) = compute_community_patterns(community.metrics)
                    console.print(
                        {
                            "structure ": structure,
                            "dispersion ": dispersion,
                            "formality ": formality,
                            "longevity ": longevity,
                            "engagement ": engagement,
                        }
                    )
                    console.print(community_patterns)
                    console.print(community.data.start_date, community.data.end_date)
                    patterns = community_patterns
                    output_handler.save_results(
                        output_path, community, community_patterns
                    )

            community.data.start_date = community.data.start_date + timedelta(days=30)
            community.data.end_date = community.data.end_date + timedelta(days=30)
            if community.data.end_date > datetime.today():
                patterns = "None"


if __name__ == "__main__":
    main()
