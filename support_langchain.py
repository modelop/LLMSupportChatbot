import json
from langchain import PromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain  # import LangChain libraries
from langchain.llms import OpenAI  # import OpenAI model
from langchain.prompts import load_prompt

def answer_question(question: str):
	llm = OpenAI(temperature=0.7)

	# Chain 1: Generating a rephrased version of the user's question
	prompt_template = load_prompt("rephrase_prompt.json")
	question_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="statement")

	# Chain 2: Generating assumptions made in the statement
	prompt_template = load_prompt("assumptions_prompt.json")
	assumptions_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="assertions")

	# Chain 3: Fact checking the assumptions
	prompt_template = load_prompt("fact_check_prompt.json")
	fact_checker_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="facts")

	# Final Chain: Generating the final answer to the user's question based on the facts and assumptions
	prompt_template = load_prompt("answer_prompt.json")
	answer_chain = LLMChain(llm=llm, prompt=prompt_template, output_key="answer")
	overall_chain = SequentialChain(
		chains=[question_chain, assumptions_chain, fact_checker_chain, answer_chain],
		input_variables=["question"],
		output_variables=["answer", "assertions", "facts"],
		verbose=True
	)
	results = overall_chain({"question": question})

	print(f"Facts: \n{results['facts']}")
	print(f"\n\nAnswer:{results['answer']}\n\n")

	return results


# modelop.score
def action(data: dict):
	result = answer_question(data['question'])
	yield {'facts': result['facts'], 'answer': result['answer']}


def main():
	# generate_prompt_files()
	print(json.dumps(next(action({'question': 'What was the town of tomichi in colorado like?'})), indent=2))


if __name__ == '__main__':
	main()