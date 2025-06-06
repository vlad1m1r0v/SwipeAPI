"""create complexes table

Revision ID: 74d390042f99
Revises: 05c17c582bb5
Create Date: 2025-06-04 13:38:30.437375

"""

from alembic import op
import sqlalchemy as sa
import advanced_alchemy
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "74d390042f99"
down_revision = "05c17c582bb5"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "complexes",
        sa.Column(
            "user_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("longitude", sa.Numeric(precision=6, scale=3), nullable=True),
        sa.Column("latitude", sa.Numeric(precision=6, scale=3), nullable=True),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_complexes_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_complexes")),
        sa.UniqueConstraint("user_id", name=op.f("uq_complexes_user_id")),
    )
    op.create_table(
        "advantages",
        sa.Column(
            "complex_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("has_children_playground", sa.Boolean(), nullable=True),
        sa.Column("has_sports_field", sa.Boolean(), nullable=True),
        sa.Column("has_parking", sa.Boolean(), nullable=True),
        sa.Column("has_landscaped_area", sa.Boolean(), nullable=True),
        sa.Column("has_on_site_shops", sa.Boolean(), nullable=True),
        sa.Column("has_individual_heating", sa.Boolean(), nullable=True),
        sa.Column("has_balcony_or_loggia", sa.Boolean(), nullable=True),
        sa.Column("has_bicycle_field", sa.Boolean(), nullable=True),
        sa.Column("has_panoramic_windows", sa.Boolean(), nullable=True),
        sa.Column("is_close_to_sea", sa.Boolean(), nullable=True),
        sa.Column("is_close_to_school", sa.Boolean(), nullable=True),
        sa.Column("is_close_to_transport", sa.Boolean(), nullable=True),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["complex_id"],
            ["complexes.id"],
            name=op.f("fk_advantages_complex_id_complexes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_advantages")),
        sa.UniqueConstraint("complex_id", name=op.f("uq_advantages_complex_id")),
    )
    op.create_table(
        "complexes_gallery",
        sa.Column(
            "complex_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("photo", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["complex_id"],
            ["complexes.id"],
            name=op.f("fk_complexes_gallery_complex_id_complexes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_complexes_gallery")),
        sa.UniqueConstraint("complex_id", name=op.f("uq_complexes_gallery_complex_id")),
    )
    op.create_table(
        "documents",
        sa.Column(
            "complex_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("file", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["complex_id"],
            ["complexes.id"],
            name=op.f("fk_documents_complex_id_complexes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_documents")),
        sa.UniqueConstraint("complex_id", name=op.f("uq_documents_complex_id")),
    )
    op.create_table(
        "formalization_and_payment_settings",
        sa.Column(
            "complex_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column(
            "formalization",
            sa.Enum(
                "NOTARY",
                "LEGAL_AGREEMENT",
                "STATE_REGISTRATION",
                "PRIVATE_AGREEMENT",
                name="formalization_and_payment_settings_formalization_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "billing_options",
            sa.Enum(
                "MORTGAGE",
                "CASH",
                "INSTALLMENT",
                "LEASING",
                "STATE_PROGRAM",
                name="formalization_and_payment_settings_billing_options_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "property_type",
            sa.Enum(
                "RESIDENTIAL",
                "COMMERCIAL",
                "INDUSTRIAL",
                "LAND",
                name="formalization_and_payment_settings_property_type_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "sum_in_contract",
            sa.Enum(
                "FULL",
                "PARTIAL",
                name="formalization_and_payment_settings_sum_in_contract_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["complex_id"],
            ["complexes.id"],
            name=op.f("fk_formalization_and_payment_settings_complex_id_complexes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "id", name=op.f("pk_formalization_and_payment_settings")
        ),
        sa.UniqueConstraint(
            "complex_id", name=op.f("uq_formalization_and_payment_settings_complex_id")
        ),
    )
    op.create_table(
        "infrastructures",
        sa.Column(
            "complex_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum(
                "UNDER_CONSTRUCTION",
                "BUILT",
                "COMMISSIONED",
                name="infrastructure_status_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "type",
            sa.Enum(
                "MULTI_APARTMENT",
                "TOWNHOUSE",
                "COTTAGE",
                "VILLA",
                name="infrastructure_type_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "infrastructure_class",
            sa.Enum(
                "ECONOMY",
                "COMFORT",
                "BUSINESS",
                "PREMIUM",
                "ELITE",
                name="infrastructure_class_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "technology",
            sa.Enum(
                "BRICK",
                "PANEL",
                "AERATED_CONCRETE",
                "FRAME",
                name="infrastructure_technology_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "territory",
            sa.Enum(
                "CLOSED_GUARDED",
                "CLOSED",
                "GUARDED",
                "OPEN",
                name="infrastructure_territory_enum",
            ),
            nullable=True,
        ),
        sa.Column("sea_distance", sa.Numeric(precision=6, scale=3), nullable=True),
        sa.Column(
            "utility_bills",
            sa.Enum(
                "INDIVIDUAL_METERS",
                "FIXED_RATE",
                "INCLUDED_IN_RENT",
                "SEPARATE_RECEIPTS",
                "CENTRALIZED",
                name="infrastructure_utility_bills_enum",
            ),
            nullable=True,
        ),
        sa.Column("ceiling_height", sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column("has_gas", sa.Boolean(), nullable=True),
        sa.Column(
            "heating",
            sa.Enum(
                "CENTRAL",
                "INDIVIDUAL_GAS",
                "INDIVIDUAL_ELECTRIC",
                "AUTONOMOUS",
                name="infrastructure_heating_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "sewerage",
            sa.Enum(
                "CENTRAL",
                "SEPTIC_TANK",
                "AUTONOMOUS",
                name="infrastructure_sewerage_enum",
            ),
            nullable=True,
        ),
        sa.Column(
            "water_supply",
            sa.Enum("CENTRAL", "WELL", name="infrastructure_water_supply_enum"),
            nullable=True,
        ),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["complex_id"],
            ["complexes.id"],
            name=op.f("fk_infrastructures_complex_id_complexes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_infrastructures")),
        sa.UniqueConstraint("complex_id", name=op.f("uq_infrastructures_complex_id")),
    )
    op.create_table(
        "news",
        sa.Column(
            "complex_id",
            sa.BigInteger().with_variant(sa.Integer(), "sqlite"),
            nullable=False,
        ),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False
        ),
        sa.Column(
            "created_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            advanced_alchemy.types.datetime.DateTimeUTC(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["complex_id"],
            ["complexes.id"],
            name=op.f("fk_news_complex_id_complexes"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_news")),
        sa.UniqueConstraint("complex_id", name=op.f("uq_news_complex_id")),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("news")
    op.drop_table("infrastructures")
    op.drop_table("formalization_and_payment_settings")
    op.drop_table("documents")
    op.drop_table("complexes_gallery")
    op.drop_table("advantages")
    op.drop_table("complexes")
    # ### end Alembic commands ###
