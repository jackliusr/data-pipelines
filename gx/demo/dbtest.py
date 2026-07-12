import great_expectations as gx

context = gx.get_context()

connection_string = "postgresql+psycopg2://try_gx:try_gx@localhost/gx"

data_source = context.data_sources.add_postgres(
    "postgres db", connection_string=connection_string
)
data_asset = data_source.add_table_asset(name="taxi data", table_name="nyc_taxi_data")

batch_definition = data_asset.add_batch_definition_whole_table("batch definition")
batch = batch_definition.get_batch()


suite = context.suites.add(
    gx.core.expectation_suite.ExpectationSuite(name="expectations")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="passenger_count", min_value=1, max_value=6, severity="warning"
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="fare_amount", min_value=0, severity="critical"
    )
)

validation_definition = context.validation_definitions.add(
    gx.core.validation_definition.ValidationDefinition(
        name="validation definition",
        data=batch_definition,
        suite=suite,
    )
)

checkpoint = context.checkpoints.add(
    gx.checkpoint.checkpoint.Checkpoint(
        name="checkpoint", validation_definitions=[validation_definition]
    )
)

checkpoint_result = checkpoint.run()
print(checkpoint_result.describe())