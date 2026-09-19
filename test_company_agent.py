import unittest
from company_agent import CompanyAgent, KnowledgeBase

class CompanyAgentTests(unittest.TestCase):
    def setUp(self): self.agent=CompanyAgent(KnowledgeBase.load())
    def test_grounded_answer(self):
        result=self.agent.answer("How many vacation days do I get?")
        self.assertIn("24 paid leave days",result["answer"])
        self.assertEqual(result["citations"],["handbook/leave-policy"])
    def test_refuses_unsupported_question(self):
        result=self.agent.answer("Who won the football match?")
        self.assertEqual(result["confidence"],0)
        self.assertEqual(result["citations"],[])

if __name__=="__main__": unittest.main()
