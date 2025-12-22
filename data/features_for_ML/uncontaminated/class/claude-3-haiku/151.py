class MellisaPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def open_spider(self, spider):
        self.items = []

    def close_spider(self, spider):
        with open(f"{spider.name}.json", "w", encoding="utf-8") as f:
            json.dump(self.items, f, ensure_ascii=False, indent=4)