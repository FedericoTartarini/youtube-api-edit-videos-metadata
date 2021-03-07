# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import mysecrets
import pandas as pd

import googleapiclient.discovery


def authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=mysecrets.developer_key
    )

    return youtube


def get_video_ids(channel_id):
    youtube = authenticate()

    more_than_50_results = True
    next_page_token = ""

    while more_than_50_results:

        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type="video",
        )

        response = request.execute()

        if "nextPageToken" in response.keys():
            next_page_token = response["nextPageToken"]
        else:
            more_than_50_results = False

        video_ids = [
            x["id"]["videoId"]
            for x in response["items"]
            if x["id"]["kind"] == "youtube#video"
        ]

        df_ids = pd.DataFrame(columns=["video-ids"])
        try:
            df_ids = pd.read_csv(file_video_ids)
        except FileNotFoundError:
            pass

        df_ids.append(
            pd.DataFrame(video_ids, columns=["video-ids"])
        ).drop_duplicates().to_csv(file_video_ids, index=False)


def get_video_description():
    youtube = authenticate()

    df_ids = pd.read_csv(file_video_ids)

    dict_videos = {}

    for video_id in df_ids["video-ids"].unique():

        request = youtube.videos().list(part="snippet", id=video_id)

        response = request.execute()

        # change this code if you want to save more info from a video
        if "tags" in response["items"][0]["snippet"].keys():
            dict_video = {
                "title": response["items"][0]["snippet"]["title"],
                "description": response["items"][0]["snippet"]["description"].split(
                    "\n"
                ),
                "tags": response["items"][0]["snippet"]["tags"],
            }
        else:
            dict_video = {
                "title": response["items"][0]["snippet"]["title"],
                "description": response["items"][0]["snippet"]["description"].split(
                    "\n"
                ),
            }

        dict_videos[response["items"][0]["id"]] = dict_video

    with open("video_info.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(dict_videos, indent=2))


if __name__ == "__main__":

    file_video_ids = "video_ids.csv"

    # download ids of all the videos in your channel
    get_video_ids(channel_id="UCRjhrVMfeAurqHm4BnTNgyw")

    # get info from the video you uploaded on your channel
    get_video_description()
