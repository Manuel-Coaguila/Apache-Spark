from pyspark.sql.types import StructType, StructField, StringType


def get_employee_schema() -> StructType:
    return StructType(
        [
            StructField("Education", StringType(), True),
            StructField("JoiningYear", StringType(), True),
            StructField("City", StringType(), True),
            StructField("PaymentTier", StringType(), True),
            StructField("Age", StringType(), True),
            StructField("Gender", StringType(), True),
            StructField("EverBenched", StringType(), True),
            StructField("ExperienceInCurrentDomain", StringType(), True),
            StructField("LeaveOrNot", StringType(), True)
        ]
    )
