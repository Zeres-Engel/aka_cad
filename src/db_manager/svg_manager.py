from bson import ObjectId

class SVGeditorManager:
    def __init__(self, db):
        self.collection = db['svg_sources']

    def create_svg(self, user_id, svg_url):
        svg = {
            'user_id': ObjectId(user_id),
            'svg_url': svg_url
        }
        result = self.collection.insert_one(svg)
        return str(result.inserted_id)

    def get_svg(self, svg_id):
        return self.collection.find_one({'_id': ObjectId(svg_id)})

    def get_user_svgs(self, user_id):
        return list(self.collection.find({'user_id': ObjectId(user_id)}))

    def clear_collection(self):
        self.collection.delete_many({})

    def save_svg_content(self, user_id, svg_content):
        result = self.collection.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': {'svg_content': svg_content}},
            upsert=True
        )
        return str(result.upserted_id) if result.upserted_id else None

    def get_svg_content(self, user_id):
        svg_doc = self.collection.find_one({'user_id': ObjectId(user_id)})
        return svg_doc['svg_content'] if svg_doc else None