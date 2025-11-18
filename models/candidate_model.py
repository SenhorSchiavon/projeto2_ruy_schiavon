from bson.objectid import ObjectId

class CandidateModel:
    def __init__(self, db):
        self.collection = db["candidatos_teste_fisico"]

    def create_candidate(self, candidate_data):
        self.collection.insert_one(candidate_data)

    def list_candidates(self):
        return list(self.collection.find().sort("nome", 1))

    def count_by_status(self):
        aprovados = self.collection.count_documents({"status": "APROVADO"})
        reprovados = self.collection.count_documents({"status": "REPROVADO"})
        return {"APROVADO": aprovados, "REPROVADO": reprovados}

    def get_all_for_kmeans(self):
        cursor = self.collection.find(
            {
                "tempo_300": {"$ne": None},
                "tempo_2400": {"$ne": None},
            },
            {"tempo_300": 1, "tempo_2400": 1, "_id": 0},
        )
        return list(cursor)
    def get_candidate_by_id(self, candidate_id):
        return self.collection.find_one({"_id": ObjectId(candidate_id)})

    def update_candidate(self, candidate_id, candidate_data):
        self.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": candidate_data}
        )
