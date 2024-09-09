from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal

def deserialize(data):
  deserializer = TypeDeserializer()
  if isinstance(data, list):
        return [deserialize(v) for v in data]
  if isinstance(data, dict):
      try:
          return deserializer.deserialize(data)
      except TypeError:
          return {k: deserialize(v) for k, v in data.items()}
  else:
      return data
  
def convert_decimal(obj):
  if isinstance(obj, Decimal):
      return float(obj)
  raise TypeError