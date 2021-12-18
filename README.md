# ClassHound
## Description
Monitor and store class usage events and values.

## Classes
### classhound/monitor -> Monitor
#### **Usage example:**

 ```python
from delta import *
from classhound import Monitor

monitor_table_writes = Monitor()
readwriter.DataFrameWriter.save = monitor_table_writes.internal_function_parameter(
    func=readwriter.DataFrameWriter.save,
    param_details=(0, "path")
)
DeltaTable.forPath = monitor_table_writes.function_parameter(
    func=DeltaTable.forPath,
    param_details=(1, "path")
    )

df = spark.createDataFrame([(1, "John"), (2, "Bob")], ["id", "name"])
df.write.format("delta").save("/path/table1", mode="append")
...
(
    DeltaTable.forPath(spark, path="/path/table2").alias("dest")
    .merge(
        df.alias("src"),
        condition="src.id = dest.id"
    )
)
monitor_table_writes.values
# ["/path/table1", "/path/table2"]
```

#### **Example of why would you use this?**
Instead of manually searching/updating a list of dependencies (potentially missing something or making a mistake)
as you develop. You can automate the updating of these lists / configs etc.

This monitor class does not alter or break the actuall functionality of the functions it monitors. Allowing the
program to work as intended and not getting in the way of development, having to remember to build out logic to caputer those values or having to do it manually.

This is a set and forget if you configured all the functions that you are intersted in checking for those types of value updates or addons.
