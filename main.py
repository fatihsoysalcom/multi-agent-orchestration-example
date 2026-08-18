import time

class Agent:
    """Base class for an agent."""
    def __init__(self, name):
        self.name = name

    def communicate(self, message, sender):
        """Simulates receiving a message."""
        print(f"[{self.name}] received message from {sender.name}: '{message}'")
        time.sleep(0.05) # Simulate processing time

class SummarizerAgent(Agent):
    """Specialized agent for summarizing text."""
    def __init__(self):
        super().__init__("Summarizer")

    def summarize(self, text):
        """Simulates an LLM summarizing text. (No actual LLM call)"""
        self.communicate(f"Please summarize: '{text[:50]}...'", self) # Self-communication for logging
        # In a real scenario, this would call an LLM API.
        # For this example, we'll just take the first few sentences.
        sentences = text.split('.')
        summary = ". ".join(sentences[:2]) + ("..." if len(sentences) > 2 else "")
        print(f"[{self.name}] produced summary: '{summary}'")
        return summary

class QuestionAnswererAgent(Agent):
    """Specialized agent for answering questions based on context."""
    def __init__(self):
        super().__init__("QuestionAnswerer")

    def answer_question(self, question, context):
        """Simulates an LLM answering a question based on context. (No actual LLM call)"""
        self.communicate(f"Answer '{question}' based on context: '{context[:50]}...'", self) # Self-communication for logging
        # In a real scenario, this would call an LLM API.
        # For this example, we'll check for keywords in the context.
        question_lower = question.lower()
        context_lower = context.lower()

        if "swarm" in question_lower and "rust" in context_lower:
            answer = "Swarm is a Rust-based platform for multi-agent orchestration."
        elif "orchestration" in question_lower and "agents" in context_lower:
            answer = "Multi-agent orchestration involves coordinating specialized agents to achieve a common goal."
        elif "llm" in question_lower and "gateway" in context_lower:
            answer = "Swarm also offers LLM gateway features."
        else:
            answer = "Based on the provided context, I can't give a precise answer to that question."

        print(f"[{self.name}] produced answer: '{answer}'")
        return answer

class OrchestratorAgent(Agent):
    """Main agent that orchestrates other agents to fulfill a complex request."""
    def __init__(self):
        super().__init__("Orchestrator")
        self.summarizer = SummarizerAgent()
        self.qa_agent = QuestionAnswererAgent()

    def handle_request(self, document, question):
        """
        Orchestrates the workflow:
        1. Delegates summarization.
        2. Delegates question answering using the summary.
        3. Synthesizes the final response.
        """
        print(f"\n[{self.name}] Starting to handle request...")
        self.communicate("Received document and question. Delegating tasks.", self)

        # Step 1: Delegate summarization to the SummarizerAgent
        # This illustrates task distribution and inter-agent communication.
        print(f"\n[{self.name}] Delegating summarization to {self.summarizer.name}...")
        summary = self.summarizer.summarize(document)
        self.communicate(f"Received summary from {self.summarizer.name}.", self.summarizer)

        # Step 2: Delegate question answering to the QuestionAnswererAgent, using the summary as context
        # This illustrates agents building upon each other's outputs and sequential processing.
        print(f"\n[{self.name}] Delegating question answering to {self.qa_agent.name} using the summary...")
        answer = self.qa_agent.answer_question(question, summary)
        self.communicate(f"Received answer from {self.qa_agent.name}.", self.qa_agent)

        # Step 3: Synthesize the final response from the outputs of the specialized agents.
        final_response = (
            f"--- Final Orchestrated Report ---\n"
            f"Summary of Document: {summary}\n"
            f"Answer to '{question}': {answer}\n"
            f"---------------------------------"
        )
        print(f"\n[{self.name}] Final response synthesized.")
        return final_response

# --- Main execution --- 
if __name__ == "__main__":
    # Example document (simulating a complex article or data source)
    example_document = (
        "Yapay zeka sistemleri gün geçtikçe daha karmaşık hale geliyor ve tekil, devasa modeller yerine, "
        "belirli görevleri üstlenen çoklu ajanların işbirliği yapması ihtiyacı ortaya çıkıyor. "
        "Bu makalede, Rust dilinde geliştirilen Swarm adlı yenilikçi bir platformu ve bu platformun "
        "çoklu ajan orkestrasyonunu ile Büyük Dil Modelleri (LLM) ağ geçidi özelliklerini derinlemesine inceleyeceğiz. "
        "Swarm, yapay zeka uygulamalarınızı daha modüler, ölçeklenebilir ve yönetilebilir kılmak için güçlü bir altyapı sunuyor. "
        "Çoklu ajan sistemleri, otonom araçlardan akıllı şehir yönetimine, finansal piyasa analizlerinden "
        "kişiselleştirilmiş müşteri hizmetlerine kadar geniş bir yelpazede uygulama alanı bulur. "
        "Peki, bu ajanların uyumlu bir şekilde çalışmasını sağlamak, görevleri dağıtmak, iletişimlerini yönetmek "
        "ve olası çakışmaları çözmek nasıl mümkün olur? İşte tam bu noktada çoklu ajan orkestrasyonu devreye girer."
    )

    # Example question 1
    example_question_1 = "What is Swarm and what language is it developed in?"

    # Initialize the Orchestrator
    orchestrator = OrchestratorAgent()

    # Handle the first request
    final_output_1 = orchestrator.handle_request(example_document, example_question_1)
    print("\n" + final_output_1)

    print("\n" + "="*40 + "\n")

    # Example question 2
    example_question_2 = "What is multi-agent orchestration?"
    final_output_2 = orchestrator.handle_request(example_document, example_question_2)
    print("\n" + final_output_2)

    print("\n" + "="*40 + "\n")

    # Example question 3 (less specific, demonstrating limitations of simple simulation)
    example_question_3 = "What are the benefits of this approach?"
    final_output_3 = orchestrator.handle_request(example_document, example_question_3)
    print("\n" + final_output_3)
