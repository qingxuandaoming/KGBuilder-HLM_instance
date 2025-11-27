# -*- coding: utf-8 -*-
import os
import sys

# Add project root to sys.path to allow importing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from neo_db.config import graph

def create_graph():
    """
    Read relation data and build the knowledge graph in Neo4j.
    Uses parameterized queries for safety and efficiency.
    """
    
    # Path to relation file
    relation_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "raw_data", "relation.txt")
    
    if not os.path.exists(relation_file):
        print(f"Error: File not found at {relation_file}")
        return

    print("Reading data...")
    relations = []
    with open(relation_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) < 5:
                continue
                
            # format: [person1, person2, relation, cate1, cate2]
            relations.append({
                "p1_name": parts[0],
                "p2_name": parts[1],
                "relation": parts[2],
                "p1_cate": parts[3],
                "p2_cate": parts[4]
            })

    print(f"Found {len(relations)} relations. Building graph...")
    
    # 1. Merge Persons
    # Collect unique persons to batch merge
    persons = {}
    for r in relations:
        persons[r['p1_name']] = r['p1_cate']
        persons[r['p2_name']] = r['p2_cate']
        
    person_list = [{"name": k, "cate": v} for k, v in persons.items()]
    
    # Batch merge persons
    merge_person_cypher = """
    UNWIND $persons AS p
    MERGE (n:Person {Name: p.name})
    SET n.cate = p.cate
    """
    graph.run(merge_person_cypher, persons=person_list)
    print(f"Merged {len(person_list)} persons.")

    # 2. Create Relationships
    # Since relationship types (labels) cannot be parameterized dynamically in standard Cypher (e.g. [: $type]),
    # we have to handle them carefully. However, since we know the relation types are safe or we want to use them as types,
    # we can group by relation type or just use a generic type and a property.
    # The original code used `CREATE (e)-[r:%s{relation: '%s'}]->(cc)` where %s is the relation name.
    # This implies the relationship TYPE is the Chinese relation name (e.g. "father"). 
    # While using non-ASCII types is supported, it's often better to use a generic type like "RELATED" and a property "type".
    # BUT, to preserve original logic/compatibility with queries, we stick to dynamic types but validate them.
    
    # Group by relation type to batch insert
    from collections import defaultdict
    rels_by_type = defaultdict(list)
    
    for r in relations:
        rels_by_type[r['relation']].append(r)
        
    for rel_type, rel_data in rels_by_type.items():
        # Sanitize rel_type just in case, though it comes from file
        safe_rel_type = rel_type.replace(" ", "_").replace("-", "_") # Basic sanitization
        
        create_rel_cypher = f"""
        UNWIND $rels AS r
        MATCH (p1:Person {{Name: r.p1_name}}), (p2:Person {{Name: r.p2_name}})
        MERGE (p1)-[rel:{safe_rel_type} {{relation: r.relation}}]->(p2)
        """
        graph.run(create_rel_cypher, rels=rel_data)
    
    graph.run("""
    MATCH (gm:Person)-[:外祖母 {relation:'外祖母'}]->(c:Person)
    MATCH (h:Person)-[:丈夫 {relation:'丈夫'}]->(gm)
    MERGE (h)-[:外祖父 {relation:'外祖父'}]->(c)
    """)
    graph.run("""
    MATCH (gm:Person)-[:外祖母 {relation:'外祖母'}]->(c:Person)
    MATCH (h:Person)<-[:妻 {relation:'妻'}]-(gm)
    MERGE (h)-[:外祖父 {relation:'外祖父'}]->(c)
    """)
    
    print("Graph construction completed.")

if __name__ == '__main__':
    create_graph()
