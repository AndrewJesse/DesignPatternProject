from abc import ABC, abstractmethod

# Port
class ForConvertingKphToMph(ABC):
    @abstractmethod
    def convert(self, kph: float) -> float:
      pass

# Port
class ForGettingConversionRate(ABC):
    @abstractmethod
    def conversion_rate(self, kph: float) -> float:
      pass

# Service
class SpeedConverter(ForConvertingKphToMph):
    def __init__(self, fixed_conversion_rate_repository: ForGettingConversionRate):
      self.fixed_conversion_rate_repository = fixed_conversion_rate_repository

    def convert(self, kph: float) -> float:
      return self.fixed_conversion_rate_repository.conversion_rate() * kph

# Adapter
class FixedConversionRateRepository(ForGettingConversionRate):
    def conversion_rate(self) -> float:
      return 0.621371

# Composition root
if __name__ == "__main__":
  conversion_rate_repository = ForGettingConversionRate = FixedConversionRateRepository()
  my_conversion = SpeedConverter(conversion_rate_repository)
  print(my_conversion.convert(100))
