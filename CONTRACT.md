# Batch contract
schema maps field names to string, integer, number or boolean. Every listed field is required and extra fields indicate drift. key names a string or integer column that must be unique within a batch. Rows are numbered from one. All rows sharing a duplicate key are flagged. Verdict is release or quarantine. Input contract errors exit 2.
