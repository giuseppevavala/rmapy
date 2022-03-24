import json
from os.path import expanduser
from typing import Dict, List

DIRECTORY = 0
DOCUMENT= 1

class Blob:
    """Remarkable's file
    """

    def __init__(self, file_uuid, blob_components, metadata) -> None:
        self.file_uuid = file_uuid
        self.blob_components = blob_components
        self.metadata = metadata
        self.parent = None
        self.type = DOCUMENT if metadata["type"] == "DocumentType" else DIRECTORY
        self.childs = []

    def __repr__(self) -> str:
        return (f"UUID: {self.file_uuid}\nMETADATA: {self.metadata}")


class Tree:
    """All remarkable's files
    """
    __cache_file_path = expanduser("~") + "/.cache/rmapy_tree"

    def __init__(self) -> None:
        self.__blobs: Dict[str, Blob] = {}
        self.root_blobs = []
        self.trash_blobs = []

    def add_blob(self, blob: Blob):
        """Add blob to tree

        Args:
            blob (Blob): blob to add
        """
        self.__blobs[blob.file_uuid] = blob

    def save_to_file(self, file_path=__cache_file_path):
        """Create cache file to save tree

        Args:
            file_path: cache file
        """
        with open(file_path, "w") as file_cache:
            for file_uuid, blob in self.__blobs.items():
                data = {
                    "file_uuid": file_uuid,
                    "blob_components": blob.blob_components,
                    "metadata": blob.metadata
                }
                file_cache.write(json.dumps(data) + "\n")

    @staticmethod
    def load_cache_file(file_path: str = __cache_file_path):
        """Load cache file and create Tree

        Args:
            file_path: cache file

        Return:
            Tree
        """
        tree = Tree()
        with open(file_path, "r") as cache_file:
            for line in cache_file:
                blob_json = json.loads(line)

                blob = Blob(
                    blob_json["file_uuid"],
                    blob_json["blob_components"],
                    blob_json["metadata"]
                )

                tree.add_blob(blob)
        tree.__organize_all_blob()
        return tree

    def __organize_all_blob(self):
        def parent_filter(parent):
            return lambda blob: blob.metadata["parent"] == parent

        blob_set = set(self.__blobs.values())

        # Reset blob parent and child
        for blob in blob_set:
            blob.parent = None
            blob.childs = []

        self.trash_blobs: List[Blob] = list(filter(parent_filter("trash"), blob_set))
        blob_set = blob_set.difference(self.trash_blobs)

        self.root_blobls: List[Blob] = list(filter(parent_filter(""), blob_set))
        blob_set = blob_set.difference(self.root_blobls)

        for blob in blob_set:
            parent_blob = self.__blobs[blob.metadata["parent"]]
            parent_blob.childs.append(blob)
            blob.parent = parent_blob
