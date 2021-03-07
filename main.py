# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().update(
        part="snippet,status",
        body={
            "id": "LrfTkQUDlpg",
            "snippet": {
                "categoryId": 22,
                "defaultLanguage": "en",
                "description": "❤️ Subscribe for more videos like this one: "
                               "https://www.youtube.com/channel/UCRjhrVMfeAurqHm4BnTNgyw?sub_confirmation=1\n"
                               "👍 and please like my video!!!\n\n"
                               "☕ Support my channel by buying me a coffee - "
                               "https://www.buymeacoffee.com/FedericoT\n\n"
                               "🤝 Let’s connect:\n"
                               "🌍  My website - https://federicotartarini.github.io/\n"
                               "💻  GitHub - https://github.com/FedericoTartarini\n"
                               "Twitter - https://twitter.com/FedericoTartar1\n"
                               "LinkedIn – "
                               "https://www.linkedin.com/in/federico-tartarini/\n\n"
                               "🎥 Other playlists and videos you may find useful:\n"
                               "➜ Beamer LaTeX course:\n"
                               "https://www.youtube.com/playlist?list=PLY91jl6VVD7z8c6XM5CR9wzU5aZ2702nD",
                "tags": [
                    "new tags"
                    ],
                "title": "There is nothing to see here."
                },
            "status": {
                "privacyStatus": "unlisted"
                }
            }
        )
    response = request.execute()

    print(response)


if __name__ == "__main__":
    main()
