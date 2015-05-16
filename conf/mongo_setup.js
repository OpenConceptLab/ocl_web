db.mappings_mapping.createIndex({map_type:1, from_concept_id:1, to_concept_id:1});
db.mappings_mapping.createIndex({map_type:1, from_concept_id:1, to_source_id:1, to_concept_code:1});
db.mappings_mapping.getIndexes()