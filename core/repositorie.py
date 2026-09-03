class Repository:
    
    def __init__(self, name: str, url: str, owner: str, language: str, quantity_stars: int, quantity_forks: int, quantity_open_issues: int, license: str, repositorie_size: int, description: str):
        self.name = name
        self.url = url
        self.owner = owner
        self.language = language
        self.quantity_stars = quantity_stars
        self.quantity_forks = quantity_forks
        self.quantity_open_issues = quantity_open_issues
        self.license = license
        self.repositorie_size = repositorie_size
        self.description = description

    def __repr__(self):
        return f"Repository(name={self.name}, url={self.url}, owner={self.owner}, language={self.language}, quantity_stars={self.quantity_stars}, quantity_forks={self.quantity_forks}, quantity_open_issues={self.quantity_open_issues}, license={self.license}, repositorie_size={self.repositorie_size}, description={self.description})"