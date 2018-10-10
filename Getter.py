""" Abstract Class for Functional Interfaces that get [GET] information from APIs """


class InformationGetter:
	""" Retrieves information from the API as specified """
	def get_information(self) -> dict:
		pass

	""" Tests the API to ensure it is alive and happy. If not, it alerts the developer that something is wrong.
	Should be run periodically to ensure the health of the API and safely ensure it can continue to be used."""
	def test(self) -> bool:
		pass
