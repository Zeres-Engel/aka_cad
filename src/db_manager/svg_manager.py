from bson import ObjectId

class SVGManager:
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
