# from django_elasticsearch_dsl import Document, Index, fields
# from django_elasticsearch_dsl.registries import registry
# from hindu.models import Village

# villages_index = Index("villages")
# villages_index.settings(number_of_shards=1, number_of_replicas=0)


# @registry.register_document
# class VillageDocument(Document):

#     id = fields.KeywordField()
#     name = fields.TextField(
#         fields={
#             "raw": fields.KeywordField()
#         }
#     )

#     image_location = fields.KeywordField()

#     block_id = fields.KeywordField()
#     district_id = fields.KeywordField()
#     state_id = fields.KeywordField()
#     country_id = fields.KeywordField()

#     class Index:
#         name = "villages"

#     class Django:
#         model = Village
#         # ❌ REMOVE image_location from here
#         fields = []

#     # ---- prepare methods ----

#     def prepare_image_location(self, obj):
#         return str(obj.image_location) if obj.image_location else None

#     def prepare_block_id(self, obj):
#         return str(obj.block_id) if obj.block_id else None

#     def prepare_district_id(self, obj):
#         return str(obj.block.district_id) if obj.block else None

#     def prepare_state_id(self, obj):
#         return str(obj.block.district.state_id) if obj.block else None

#     def prepare_country_id(self, obj):
#         return str(obj.block.district.state.country_id) if obj.block else None
