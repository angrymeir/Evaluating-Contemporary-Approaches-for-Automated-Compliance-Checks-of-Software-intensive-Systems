import csv

# Get the papers from the respective database files
def retrieve_paper_details(resource_dir, resource_files):
    all_papers = []
    for resource_file in resource_files:
        with open(resource_dir + resource_file, 'r') as f:
            papers = csv.DictReader(f)
            for p in papers:
                paper = Paper(p)
                paper.set_source(resource_file.replace('.csv', ''))
                all_papers.append(paper)
    return all_papers

class Paper:
    def __init__(self, characteristics):
        self.__set_author(characteristics)
        self.__set_title(characteristics)
        self.__set_publication_year(characteristics)
        self.__set_doi(characteristics)
        self.__set_abstract(characteristics)
        self.__set_publication_title(characteristics)
        if 'source' in characteristics.keys():
            self.set_source(characteristics['source'])
        
    def __set_author(self, characteristics):
        patterns = ['Authors', 'authors']
        for pattern in patterns:
            if pattern in characteristics.keys():
                self.authors = characteristics[pattern]
                return
        raise Exception('Authors attribute not available for paper:', characteristics)
        
    def __set_title(self, characteristics):
        patterns = ['Title', 'Document Title', 'titel'] 
        for pattern in patterns:
            if pattern in characteristics.keys():
                self.titel = characteristics[pattern]
                return
        raise Exception('Title attribute not available for paper:', characteristics)
           
    def __set_publication_year(self, characteristics):
        patterns = ['Publication year', 'Publication Year', 'Year', 'year']
        for pattern in patterns:
            if pattern in characteristics.keys():
                self.year = characteristics[pattern]
                return 
        raise Exception('Publication year attribute not available for paper:', characteristics)
        
    def __set_doi(self, characteristics):
        patterns = ['DOI', 'doi']
        for pattern in patterns:
            if pattern in characteristics.keys():
                self.doi = characteristics[pattern]
                return
        raise Exception('DOI attribute not available for paper:', characteristics)
            
    def __set_abstract(self, characteristics):
        patterns = ['Abstract', 'abstract']
        for pattern in patterns:
            if pattern in characteristics.keys():
                self.abstract = characteristics[pattern]
                return
        raise Exception('DOI attribute not available for paper:', characteristics)
            
    def __set_publication_title(self, characteristics):
        patterns = ['Proceedings title', 'Publication Title', 'Journal', 'Source title', 'pub_title']
        for pattern in patterns:
            if pattern in characteristics.keys():
                self.pub_title = characteristics[pattern]
                return 
        raise Exception('Publication title attribute not available for paper:', characteristics)
        
    def set_source(self, source):
        self.source = source
        
    def __hash__(self):
        return hash(self.__dict__.values())
        
    def __eq__(self, other):
        try:
            if self.titel.lower() == other.titel.lower() and self.year == other.year and self.source == other.source:
                return True
        except AttributeError:
            if self.titel.lower() == other.titel.lower() and self.year == other.year:
                return True
        return False