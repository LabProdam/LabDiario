class FacetManager(object):
	def ProcessText(self, baseUrl, text):
		self.facets = []
		
		facetLists = re.finditer("data-no-turbolink[^\>]*.([^\<]*).*?\<ul\s*class=\"facet-values[^\>]*.(.*?)\</ul\>", text, re.S)		
		for facetList in facetLists:
			facetData = FacetData(facetList.group(1))
			moreFacets = re.search("more_facets_link.*?href=\".([^\"]*)", facetList.group(2), re.S)
			if moreFacets:				
				sd = urllib.urlopen(baseUrl + "/" + moreFacets.group(1))
				contents = sd.read()
				sd.close()
				self.ProcessFacetList(facetData, contents)
			
			else:
				self.ProcessFacetList(facetData, facetList.group(2))
			self.facets.append(facetData)
		return self.facets
		
	def ProcessFacetList(self, facetData, facetList):
		facets = re.finditer("facet_select\"\s*href=\"([^\"]*).*?\>([^\<]*).*?facet-count[^\>]*.([^\<]*)", facetList)
		for facet in facets:
			number = facet.group(3).replace(",", "")
			if (int(number) > 0):
				link = facet.group(1)
				name = facet.group(2)
				facetElement = FacetElementData(name, link)
				facetData.AddElement(facetElement)

class FacetData(object):
	def __init__(self, name):
		self.name = name
		self.elements = []
		
	def __str__(self):
		str = self.name + "\n"
		for el in self.elements:
			str += "\t" + el.__str__() + "\n"
		return str
		
	def GetName(self):
		return self.name
		
	def GetElements(self):
		return self.elements
		
	def AddElement(self, element):
		self.elements.append(element)
		
class FacetElementData(object):
	def __init__(self, name, link):
			self.name = name
			self.link = link
			self.index = 0
	
	def __str__(self):
		return self.name + ":" + self.link
