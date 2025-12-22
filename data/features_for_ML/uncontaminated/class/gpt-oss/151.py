import json

class MellisaPipeline:
    def open_spider(self, spider):
        self.file_path = f"{spider.name}_items.jsonl"
        self.file = open(self.file_path, "w", encoding="utf-8")

    def close_spider(self, spider):
        if hasattr(self, "file") and not self.file.closed:
            self.file.close()

    def process_item(self, item, spider):
        # Convert the item to a plain dictionary
        data = dict(item) if not hasattr(item, "to_dict") else item.to_dict()
        json_line = json.dumps(data, ensure_ascii=False)
        self.file.write(json_line + "\n")
        return item