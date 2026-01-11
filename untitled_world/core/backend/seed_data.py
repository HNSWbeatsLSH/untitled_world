"""
Sample data seeding script for demo purposes.
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import SessionLocal, engine, Base
from app.models.ontology import EntityType, Entity, RelationshipType, Relationship

def seed_data():
    """Seed the database with sample data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Clear existing data
        db.query(Relationship).delete()
        db.query(Entity).delete()
        db.query(RelationshipType).delete()
        db.query(EntityType).delete()
        db.commit()

        print("Creating entity types...")

        # Create Entity Types
        person_type = EntityType(
            name="person",
            display_name="Person",
            description="An individual person",
            icon="user",
            color="#3b82f6",
            property_schema={
                "email": {"type": "string", "required": False},
                "phone": {"type": "string", "required": False},
                "age": {"type": "integer", "required": False},
            }
        )

        company_type = EntityType(
            name="company",
            display_name="Company",
            description="A business organization",
            icon="building",
            color="#10b981",
            property_schema={
                "industry": {"type": "string", "required": False},
                "founded_year": {"type": "integer", "required": False},
                "employees": {"type": "integer", "required": False},
            }
        )

        location_type = EntityType(
            name="location",
            display_name="Location",
            description="A geographic location",
            icon="map-pin",
            color="#f59e0b",
            property_schema={
                "address": {"type": "string", "required": False},
                "city": {"type": "string", "required": False},
                "country": {"type": "string", "required": False},
            }
        )

        event_type = EntityType(
            name="event",
            display_name="Event",
            description="A notable event or occurrence",
            icon="calendar",
            color="#8b5cf6",
            property_schema={
                "date": {"type": "string", "required": False},
                "type": {"type": "string", "required": False},
            }
        )

        db.add_all([person_type, company_type, location_type, event_type])
        db.commit()

        print("Creating relationship types...")

        # Create Relationship Types
        works_for = RelationshipType(
            name="works_for",
            display_name="Works For",
            description="Employment relationship",
            forward_label="works for",
            reverse_label="employs",
            color="#3b82f6",
        )

        located_in = RelationshipType(
            name="located_in",
            display_name="Located In",
            description="Location relationship",
            forward_label="located in",
            reverse_label="contains",
            color="#10b981",
        )

        attended = RelationshipType(
            name="attended",
            display_name="Attended",
            description="Event attendance",
            forward_label="attended",
            reverse_label="was attended by",
            color="#f59e0b",
        )

        knows = RelationshipType(
            name="knows",
            display_name="Knows",
            description="Personal connection",
            forward_label="knows",
            reverse_label="knows",
            color="#ec4899",
        )

        db.add_all([works_for, located_in, attended, knows])
        db.commit()

        print("Creating sample entities...")

        # Create Sample Entities

        # People
        alice = Entity(
            entity_type_id=person_type.id,
            title="Alice Johnson",
            description="Senior Software Engineer",
            properties={
                "email": "alice@example.com",
                "age": 32,
                "phone": "+1-555-0101"
            }
        )

        bob = Entity(
            entity_type_id=person_type.id,
            title="Bob Smith",
            description="Product Manager",
            properties={
                "email": "bob@example.com",
                "age": 28,
            }
        )

        carol = Entity(
            entity_type_id=person_type.id,
            title="Carol Williams",
            description="Data Scientist",
            properties={
                "email": "carol@example.com",
                "age": 35,
            }
        )

        # Companies
        tech_corp = Entity(
            entity_type_id=company_type.id,
            title="TechCorp Inc.",
            description="Leading technology company",
            properties={
                "industry": "Technology",
                "founded_year": 2010,
                "employees": 5000,
            }
        )

        data_solutions = Entity(
            entity_type_id=company_type.id,
            title="Data Solutions Ltd.",
            description="Data analytics and consulting",
            properties={
                "industry": "Data Analytics",
                "founded_year": 2015,
                "employees": 200,
            }
        )

        # Locations
        san_francisco = Entity(
            entity_type_id=location_type.id,
            title="San Francisco",
            description="City in California",
            properties={
                "city": "San Francisco",
                "country": "USA",
            }
        )

        new_york = Entity(
            entity_type_id=location_type.id,
            title="New York",
            description="City in New York",
            properties={
                "city": "New York",
                "country": "USA",
            }
        )

        # Events
        conference = Entity(
            entity_type_id=event_type.id,
            title="Tech Summit 2024",
            description="Annual technology conference",
            properties={
                "date": "2024-03-15",
                "type": "Conference",
            }
        )

        db.add_all([alice, bob, carol, tech_corp, data_solutions, san_francisco, new_york, conference])
        db.commit()

        print("Creating relationships...")

        # Create Relationships
        alice_works_at_techcorp = Relationship(
            relationship_type_id=works_for.id,
            from_entity_id=alice.id,
            to_entity_id=tech_corp.id,
            properties={"position": "Senior Engineer", "since": "2020"}
        )

        bob_works_at_techcorp = Relationship(
            relationship_type_id=works_for.id,
            from_entity_id=bob.id,
            to_entity_id=tech_corp.id,
            properties={"position": "Product Manager", "since": "2021"}
        )

        carol_works_at_data_solutions = Relationship(
            relationship_type_id=works_for.id,
            from_entity_id=carol.id,
            to_entity_id=data_solutions.id,
            properties={"position": "Data Scientist", "since": "2019"}
        )

        techcorp_in_sf = Relationship(
            relationship_type_id=located_in.id,
            from_entity_id=tech_corp.id,
            to_entity_id=san_francisco.id,
            properties={"headquarters": True}
        )

        data_solutions_in_ny = Relationship(
            relationship_type_id=located_in.id,
            from_entity_id=data_solutions.id,
            to_entity_id=new_york.id,
            properties={"headquarters": True}
        )

        alice_attended_conference = Relationship(
            relationship_type_id=attended.id,
            from_entity_id=alice.id,
            to_entity_id=conference.id,
            properties={"role": "Speaker"}
        )

        bob_attended_conference = Relationship(
            relationship_type_id=attended.id,
            from_entity_id=bob.id,
            to_entity_id=conference.id,
            properties={"role": "Attendee"}
        )

        carol_attended_conference = Relationship(
            relationship_type_id=attended.id,
            from_entity_id=carol.id,
            to_entity_id=conference.id,
            properties={"role": "Attendee"}
        )

        alice_knows_bob = Relationship(
            relationship_type_id=knows.id,
            from_entity_id=alice.id,
            to_entity_id=bob.id,
            properties={"since": "2021", "context": "Colleagues"}
        )

        alice_knows_carol = Relationship(
            relationship_type_id=knows.id,
            from_entity_id=alice.id,
            to_entity_id=carol.id,
            properties={"since": "2024", "context": "Met at conference"}
        )

        db.add_all([
            alice_works_at_techcorp,
            bob_works_at_techcorp,
            carol_works_at_data_solutions,
            techcorp_in_sf,
            data_solutions_in_ny,
            alice_attended_conference,
            bob_attended_conference,
            carol_attended_conference,
            alice_knows_bob,
            alice_knows_carol,
        ])
        db.commit()

        print("✓ Sample data created successfully!")
        print(f"  - {db.query(EntityType).count()} entity types")
        print(f"  - {db.query(Entity).count()} entities")
        print(f"  - {db.query(RelationshipType).count()} relationship types")
        print(f"  - {db.query(Relationship).count()} relationships")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
