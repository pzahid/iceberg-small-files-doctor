# Iceberg Small Files Doctor

Small data files are one of the most common causes of slow lakehouse queries and heavy metadata work. This tool reads a file listing, reports how bad the situation is, and suggests a Dremio compaction statement.

```bash
python -m doctor examples/files.csv --table lake.sales.orders
# files=5 small=4 (80%) median=3.0MB severity=high
# OPTIMIZE TABLE lake.sales.orders REWRITE DATA USING BIN_PACK;
```

A file counts as small when it is under 25% of the target size (default 128 MB). Run the tests with pip install pytest, then pytest.

Background: Dremio supports OPTIMIZE TABLE on Apache Iceberg tables. Check the Dremio documentation for options available in your version before running it in production.
