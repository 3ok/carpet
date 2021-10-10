import json
import re
from typing import List, Optional, Tuple, TypedDict

import requests  # anthonk-rage: ignore
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound

from carpet.constants import CARPET_CACHE_FILE, EXPLAINS_README, REGEX_VIDEO


class Caption(TypedDict):
    text: str
    start: float
    duration: float


Transcript = List[Caption]


class VideoDict(TypedDict):
    id: str
    title: str
    transcript: Transcript


class Video:
    def __init__(self, id: str, title: str, transcript: Transcript) -> None:
        self.id = id
        self.title = title
        self.transcript = transcript

    @property
    def url(self) -> str:
        return f"https://youtu.be/{self.id}"

    def url_starts_at(self, start: float) -> str:
        return f"https://youtu.be/{self.id}?t={int(start)}"

    @property
    def transcript_text(self) -> str:
        return " ".join(caption["text"].strip() for caption in self.transcript)

    def to_dict(self) -> VideoDict:
        return {"id": self.id, "title": self.title, "transcript": self.transcript}

    @classmethod
    def from_dict(self, video_dict: VideoDict) -> "Video":
        return Video(**video_dict)


def fetch_videos(save: bool = True) -> List[Video]:
    videos: List[Video] = []

    # Fetch video IDs and title from Anthonk's explains' README
    # It's an easier way than using Youtube's API (thus needing a key)
    response = requests.get(EXPLAINS_README)
    content_lines = response.text.strip().splitlines()
    for content_line in content_lines:
        match = REGEX_VIDEO.search(content_line)
        if match is not None and {"title", "video_id"} <= match.groupdict().keys():
            # We found a video, let's get the transcript
            video_id, title = match.groupdict()["video_id"], match.groupdict()["title"]
            try:
                # I want to do this myself with httpx, but couldn't manage
                # to make it work. Funnily enough, the Youtube API which
                # gives the captions text (timedtext) is not documented
                # on their website
                transcript: Transcript = YouTubeTranscriptApi.get_transcript(
                    video_id, languages=("en",)
                )
                video = Video(id=video_id, title=title, transcript=transcript)
                videos.append(video)
            except NoTranscriptFound:
                # Question : is it bad that I imported "NoTranscriptFound"
                # from a _private_ location (youtube_transcript_api._errors) ?

                # Some videos might have no english subtitles (or not at all)
                # For example, weirdly enough Youtube picks the #058 explains
                # video (about deadsnakes) as a dutch video. These kind of
                # videos will be skipped by Carpet
                # Note : From the current 344 explains videos, only 2 have
                # this issue
                pass

    if save:
        # Optionally save for later use
        video_dicts = [video.to_dict() for video in videos]
        with open(CARPET_CACHE_FILE, "w") as f:
            json.dump(video_dicts, f)

    return videos


def load_videos_from_json(json_file: str = CARPET_CACHE_FILE) -> List[Video]:
    with open(json_file, "r") as f:
        video_dicts: List[VideoDict] = json.load(f)
    videos = [Video.from_dict(video_dict) for video_dict in video_dicts]
    return videos


def find_video_from_text(
    text: str, videos: List[Video]
) -> Optional[Tuple[Video, float]]:
    # I finally decided to use simple regex instead
    # of some fancy fuzzy search because it was
    # super slow if you search across all videos.
    # Therefore now it will only find
    # the video if there is an exact match, which
    # is not very practical
    regex_text = re.compile(fr"({text.lower()})")
    for video in videos:
        transcript = video.transcript_text.lower()
        match = regex_text.search(transcript)
        if match is not None:
            # We found the video, now we go through
            # the transcript to find an approximate
            # timestamp of the text
            n_captions = len(video.transcript)
            for i in range(n_captions):
                transcript_text_so_far = " ".join(
                    c["text"] for c in video.transcript[i:]
                ).lower()
                match = regex_text.search(transcript_text_so_far)
                if match is None:
                    # We no longer match, that means the previous
                    # caption is a good approximation of the start
                    # timestamp of the input text
                    start = video.transcript[i - 1]["start"]
                    return video, start
