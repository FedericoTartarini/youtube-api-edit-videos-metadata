# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import sys

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]


def authenticate():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )
    return youtube


def update_videos(id_video, title, description, tags):

    videos_list_response = youtube.videos().list(id=id_video, part="snippet").execute()

    # If the response does not contain an array of 'items' then the video was
    # not found.
    if not videos_list_response["items"]:
        print('Video "%s" was not found.' % id_video)
        sys.exit(1)

    # Since the request specified a video ID, the response only contains one
    # video resource. This code extracts the snippet from that resource.
    videos_list_snippet = videos_list_response["items"][0]["snippet"]

    # Set video title, description, default language if specified in args.
    videos_list_snippet["title"] = title
    videos_list_snippet["description"] = description
    videos_list_snippet["tags"] = tags

    videos_update_response = (
        youtube.videos()
        .update(part="snippet", body=dict(snippet=videos_list_snippet, id=id_video))
        .execute()
    )

    print(
        "The updated video metadata is:\n"
        + "Title: "
        + videos_update_response["snippet"]["title"]
        + "\n"
    )
    if videos_update_response["snippet"]["description"]:
        print("Description: " + videos_update_response["snippet"]["description"] + "\n")
    if videos_update_response["snippet"]["tags"]:
        print("Tags: " + ",".join(videos_update_response["snippet"]["tags"]) + "\n")


if __name__ == "__main__":

    with open("video_info.json", "r", encoding="utf-8") as file:
        dict_videos = json.load(file)

    for video_id in list(dict_videos.keys()):

        try:
            if len(dict_videos[video_id]["title"]) > 100:
                print(
                    f"Title too long -- {video_id} current length "
                    "{len(dict_videos[video_id]['title'])}"
                )
                exit()

            if len("\n".join(dict_videos[video_id]["description"])) > 5000:
                print(
                    f"Description too long -- {video_id} current length {len(' '.join(dict_videos[video_id]['description']))}"
                )
                exit()

            if len(", ".join(list(set(dict_videos[video_id]["tags"])))) > 500:
                print(
                    f"Tags too long -- {video_id} current length {len(' '.join(dict_videos[video_id]['tags']))}"
                )
                exit()

        except KeyError:
            pass

    youtube = authenticate()

    for video_id in list(dict_videos.keys())[:1]:
        print(video_id)
        update_videos(
            id_video=video_id,
            title=dict_videos[video_id]["title"],
            description="\n".join(dict_videos[video_id]["description"]),
            tags=list(set(dict_videos[video_id]["tags"])),
        )
