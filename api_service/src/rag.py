from src.task_qa import get_answer


def call_llm_service(query, instructions, context, previous_questions):
    prompt = f"""Answer the question as truthfully as possible using the provided context, and if the answer is not contained within the text below, say "I don't know".
        \n\nInstructions for answer: {instructions}
        \n\nContext: {context}
        \n\nQuestion: {str(query)}
        """
    llm_response = get_answer(prompt)
    return llm_response
