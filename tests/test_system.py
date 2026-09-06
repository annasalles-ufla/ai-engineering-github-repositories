import tempfile
import unittest
from pathlib import Path
from core.analysis import RepositoryAnalysis
from core.classification import RelativeVisibilityClassifier
from core.loader import CsvRepositoryLoader
from trabalho1_procedural import classify
from trabalho2_csv import selection_sort

CSV = """full_name,owner,repo_name,description,html_url,language,stars,forks,open_issues,size_kb,license,license_family,ai_category,maintenance_status
org/a,org,a,first,https://x,Python,100,20,5,10,MIT,Permissive,Agents,Active
org/b,org,b,second,https://y,Java,-1,2,1,,,,RAG,Inactive
org/c,org,c,python text,https://z,Python,10,2,1,,Apache-2.0,Permissive,RAG,Active
"""
class SystemTests(unittest.TestCase):
    def setUp(self):
        self.directory=tempfile.TemporaryDirectory(); self.path=Path(self.directory.name)/"base.csv"; self.path.write_text(CSV,encoding="utf-8")
        repositories,self.invalid,self.missing=CsvRepositoryLoader().load(self.path); self.repositories=repositories; self.analysis=RepositoryAnalysis(repositories)
    def tearDown(self): self.directory.cleanup()
    def test_loader_validates_negative_metric_and_counts_missing(self):
        self.assertEqual(len(self.repositories),2); self.assertEqual(len(self.invalid),1); self.assertEqual(self.invalid[0].reason,"stars é negativo"); self.assertEqual(self.missing["size_kb"],2)
    def test_search_filter_ranking_and_statistics(self):
        self.assertEqual([r.full_name for r in self.analysis.search("python","description")],["org/c"]); self.assertEqual(len(self.analysis.filter(language="python",star_range=(50,200))),1); self.assertEqual(self.analysis.ranking()[0].full_name,"org/a"); self.assertEqual(self.analysis.statistics()["stars"]["mean"],55)
    def test_strategy_classifies_repository(self): self.assertEqual(RelativeVisibilityClassifier(20,80,5,15).classify(self.repositories[0]),"Alta visibilidade relativa")
    def test_work_1_rule_and_work_2_manual_sort(self):
        self.assertEqual(classify({"stars": 100, "forks": 20, "open_issues": 1, "license": "MIT"}), "Alta visibilidade relativa")
        self.assertEqual(selection_sort([{"stars": 2}, {"stars": 9}], "stars")[0]["stars"], 9)
if __name__ == "__main__": unittest.main()
