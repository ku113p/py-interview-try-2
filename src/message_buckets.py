from __future__ import annotations

from langchain_core.messages import BaseMessage

MessageBuckets = dict[float, list[BaseMessage]]


def merge_message_buckets(
    left: MessageBuckets | None,
    right: MessageBuckets | None,
) -> MessageBuckets:
    merged: MessageBuckets = {}
    for bucket in (left, right):
        if not bucket:
            continue
        for timestamp, messages in bucket.items():
            if timestamp in merged:
                merged[timestamp].extend(messages)
            else:
                merged[timestamp] = list(messages)
    return merged
