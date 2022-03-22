import json
from os.path import expanduser

class Blob:
    """Remarkable's file
    """

    def __init__(self, file_uuid, blob_components, metadata) -> None:
        self.file_uuid = file_uuid
        self.blob_components = blob_components
        self.metadata = metadata

    def __repr__(self) -> str:
        return (f"UUID: {self.file_uuid}\nMETADATA: {self.metadata}")


class Tree:
    """All remarkable's files
    """
    __cache_file_path = expanduser("~") + "/.cache/rmapy_tree"

    def __init__(self) -> None:
        self.__blob_list = []

    def get_root_blob(self) -> Blob:
        return self.__blob_list[0]

    def add_blob(self, blob: Blob):
        """Add blob to tree

        Args:
            blob (Blob): blob to add
        """
        self.__blob_list.append(blob)

    def save_to_file(self, file_path = __cache_file_path):
        """Create cache file to save tree

        Args:
            file_path: cache file
        """
        with open(file_path, "w") as file_cache:
            for blob in self.__blob_list:
                data = {
                    "file_uuid": blob.file_uuid,
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
                tree.add_blob(Blob(
                    blob_json["file_uuid"], blob_json["blob_components"], blob_json["metadata"]))
        return tree
